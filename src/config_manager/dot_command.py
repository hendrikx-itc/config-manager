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

    for node in data['nodes']:
        out_file.write('    "{name}" [\n'.format(**node))
        out_file.write('    ];\n')

    for node in data['nodes']:
        for data_stream in node.get('data_streams', []):
            out_file.write(
                '    "{name}" -> "{dst_name}" [ label = "{label}" ]'.format(
                    name=node['name'],
                    dst_name=data_stream['other'],
                    label=data_stream['protocol']
                )
            )

    out_file.write('}\n')
