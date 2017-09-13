import argparse
import sys
from io import TextIOWrapper

import yaml


def setup_command_parser(subparsers):
    rst_cmd = subparsers.add_parser(
        'rst', help='command for generating RestructuredText output'
    )

    rst_cmd.add_argument(
        'infile', type=argparse.FileType('r', encoding='utf-8')
    )

    rst_cmd.add_argument(
        '--output-file', '-o', help='write output to file'
    )

    rst_cmd.add_argument(
        '--out-encoding', default='utf-8', help='encoding of output file'
    )

    rst_cmd.set_defaults(cmd=rst_command)


def configure_out_file(file_path, encoding):
    if file_path:
        out_file = open(file_path, 'wb')
    else:
        out_file = sys.stdout.buffer

    return TextIOWrapper(out_file, encoding)


def rst_command(args):
    out_file = configure_out_file(args.output_file, args.out_encoding)

    data = load(args.infile)

    out_file.writelines(render_rst(data))


def load(infile):
    return yaml.load(infile)


def render_rst(data):
    yield 'Report\n'
