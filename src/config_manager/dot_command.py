import argparse
import sys
from io import TextIOWrapper

import yaml


def setup_command_parser(subparsers):
    dot_cmd = subparsers.add_parser(
        'dot', help='command for generating Graphviz DOT output'
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
    return yaml.load(infile)


def render_dot(indent, data):
    yield indent('digraph d {\n')

    yield indent('    graph [ fontname="Helvetica", pad="0.5", ranksep="2", nodesep="2" ];\n')

    yield indent('    node [ fontname="Helvetica", shape=none, margin=0 ];\n')

    yield indent('    edge [ fontname="Helvetica" ];\n')

    yield from render_nodes(indent.increase(), data)

    yield from render_edges(indent.increase(), data)

    yield indent('}\n')


def render_nodes(indent, data):
    non_tagged_hosts = [
        host for host in data['hosts']
        if 'hitc_managed' not in host.get('tags', tuple())
    ]

    for host in non_tagged_hosts:
        yield from render_host(indent.increase(), host)

    yield from render_tagged_hosts_cluster(indent, data, 'hitc_managed')


def render_tagged_hosts_cluster(indent, data, tag_name):
    yield indent('subgraph cluster_{} {{\n'.format(tag_name))

    tagged_hosts = [
        host
        for host in data['hosts']
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
    for host in data['hosts']:
        data_streams = host.get('data_streams', [])
        out_streams = [
            data_stream
            for data_stream in data_streams
            if data_stream.get('direction', '->') == '->'
        ]

        for data_stream in out_streams:
            yield indent(
                '"{name}" -> "{dst_name}" [ xlabel = "{label}" ];\n'.format(
                    name=host['name'],
                    dst_name=data_stream['other'],
                    label=data_stream['application_protocol']
                )
            )

        in_streams = [
            data_stream
            for data_stream in data_streams
            if data_stream.get('direction', '->') == '<-'
        ]

        for data_stream in in_streams:
            yield indent(
                '"{name}" -> "{dst_name}" [ xlabel = "{label}" ];\n'.format(
                    name=data_stream['other'],
                    dst_name=host['name'],
                    label=data_stream['application_protocol']
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
