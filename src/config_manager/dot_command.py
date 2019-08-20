import argparse
import sys
from io import TextIOWrapper

import yaml


def setup_command_parser(subparsers):
    dot_cmd = subparsers.add_parser(
        'dot', help='generate Graphviz DOT output'
    )

    dot_cmd.add_argument(
        'infile', type=argparse.FileType('r', encoding='utf-8')
    )

    dot_cmd.add_argument(
        '--output-file', '-o', help='write output to file'
    )

    dot_cmd.add_argument(
        '--out-encoding', default='utf-8', help='encoding of output file'
    )

    dot_cmd.set_defaults(cmd=dot_command)


def configure_out_file(filepath, encoding):
    if filepath:
        out_file = open(filepath, 'wb')
    else:
        out_file = sys.stdout.buffer

    return TextIOWrapper(out_file, encoding)


def dot_command(args):
    out_file = configure_out_file(args.output_file, args.out_encoding)

    data = load(args.infile)

    out_file.writelines(render_dot(Indentation(0), data))


def load(infile):
    return yaml.load(infile, Loader=yaml.Loader)


def render_dot(indent, data):
    yield indent('digraph d {\n')

    if 'name' in data:
        yield indent('    label="{}";'.format(data['name']))

    yield indent('    {};\n'.format(dot_config(
        'graph',
        {'fontname': 'Helvetica', 'pad': '0.5', 'ranksep': '1', 'nodesep': '1'}
    )))

    yield indent('    {};\n'.format(dot_config(
        'node',
        {'fontname': 'Helvetica', 'shape': 'none', 'margin': '0'}
    )))

    yield indent('    {};\n'.format(dot_config(
        'edge',
        {'fontname': 'Helvetica'}
    )))

    yield from render_nodes(indent.increase(), data)

    yield from render_edges(indent.increase(), data)

    yield indent('}\n')


def dot_config(obj_type, config):
    return '{obj_type} [ {attrs} ]'.format(
        obj_type=obj_type,
        attrs=', '.join([
            '{}="{}"'.format(name, value) for name, value in config.items()
        ])
    )


def render_nodes(indent, data):
    non_tagged_hosts = [
        host for host in data['nodes']
        if 'hitc-managed' not in host.get('tags', tuple())
    ]

    for host in non_tagged_hosts:
        yield from render_host(indent.increase(), host)

    yield from render_tagged_hosts_cluster(indent, data, 'hitc-managed')


def render_tagged_hosts_cluster(indent, data, tag_name):
    yield indent('subgraph cluster_{} {{\n'.format(tag_name.replace('-', '_')))

    tagged_hosts = [
        host
        for host in data['nodes']
        if tag_name in host.get('tags', tuple())
    ]

    for host in tagged_hosts:
        yield from render_host(indent.increase(), host)

    yield indent('}\n')


def render_host(indent, host):
    yield indent('"{name}" [\n'.format(**host))
    yield indent('    label=<\n')
    yield indent('    {}\n'.format(render_node_label(host)))
    yield indent('    >\n')
    yield indent('];\n')


class Indentation:
    def __init__(self, level, indent_str='    '):
        self._level = level
        self._indent_str = indent_str

    def increase(self):
        return Indentation(self._level + 1, self._indent_str)

    def decrease(self):
        return Indentation(self._level + 1, self._indent_str)

    def __call__(self, line):
        return (self._level * self._indent_str) + line


def render_edges(indent, data):
    for host in data['nodes']:
        connections = host.get('connections', [])
        out_streams = [
            data_stream
            for data_stream in connections
            if data_stream.get('direction', '->') == '->'
        ]

        for data_stream in out_streams:
            yield indent(
                '"{name}" -> "{dst_name}" [ xlabel = "{label}" ];\n'.format(
                    name=host['name'],
                    dst_name=data_stream['other'],
                    label=data_stream.get('application_protocol', '')
                )
            )

        in_streams = [
            data_stream
            for data_stream in connections
            if data_stream.get('direction', '->') == '<-'
        ]

        for data_stream in in_streams:
            yield indent(
                '"{name}" -> "{dst_name}" [ xlabel = "{label}" ];\n'.format(
                    name=data_stream['other'],
                    dst_name=host['name'],
                    label='{} ({})'.format(data_stream['application_protocol'], data_stream['port'])
                )
            )


def render_node_label(node):
    ip_addresses = node.get('ip_addresses')

    if ip_addresses is not None and len(ip_addresses) > 0:
        ip_address_text = ip_addresses[0]
    else:
        ip_address_text = 'unknown'

    return (
        '<table border="0" cellborder="1" cellspacing="0">'
        '<tr>'
        '<td bgcolor="lightblue">{name}</td>'
        '</tr>'
        '<tr>'
        '<td>{ip_address}</td>'
        '</tr>'
        '</table>'
    ).format(
        name=node['name'],
        ip_address=ip_address_text
    )
