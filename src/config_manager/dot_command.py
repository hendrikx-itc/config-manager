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

    render_dot(data, out_file)


def load(infile):
    return yaml.load(infile)


def render_dot(data, out_file):
    out_file.write('digraph d {\n')

    out_file.write('    graph [ fontname="Helvetica" ]\n')

    out_file.write('    node [ fontname="Helvetica", shape=none, margin=0 ]\n')

    out_file.write('    edge [ fontname="Helvetica" ]\n')

    for node in data['hosts']:
        out_file.write('    "{name}" [\n'.format(**node))
        out_file.write('        label=<\n')
        out_file.write('        {}\n'.format(render_node_label(node)))
        out_file.write('        >\n')
        out_file.write('    ];\n')

    for node in data['hosts']:
        out_streams = [
            data_stream
            for data_stream in node.get('data_streams', [])
            if data_stream.get('direction', '->') == '->'
        ]

        for data_stream in out_streams:
            out_file.write(
                '    "{name}" -> "{dst_name}" [ label = "{label}" ]\n'.format(
                    name=node['name'],
                    dst_name=data_stream['other'],
                    label=data_stream['application_protocol']
                )
            )

    out_file.write('}\n')


def render_node_label(node):
    return (
        '<table border="0" cellborder="1" cellspacing="0">'
        '<tr>'
        '<td colspan="2" bgcolor="lightblue">{name}</td>'
        '</tr>'
        '<tr>'
        '<td>IP Address</td>'
        '<td>{ip_address}</td>'
        '</tr>'
        '</table>'
    ).format(
        name=node['name'],
        ip_address=node['ip_addresses'][0]
    )
