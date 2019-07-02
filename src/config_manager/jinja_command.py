import argparse
import sys
from io import TextIOWrapper

import yaml

from jinja2 import Template


def setup_command_parser(subparsers):
    jinja_cmd = subparsers.add_parser(
        'jinja', help='Render configuration using a Jinja template'
    )

    jinja_cmd.add_argument(
        'template', type=argparse.FileType('r', encoding='utf-8'),
        help='template for rendering output'
    )

    jinja_cmd.add_argument(
        'infile', type=argparse.FileType('r', encoding='utf-8')
    )

    jinja_cmd.add_argument(
        '--output-file', '-o', help='write output to file'
    )

    jinja_cmd.add_argument(
        '--out-encoding', default='utf-8', help='encoding of output file'
    )

    jinja_cmd.add_argument(
        '--filter-hosts', help='filter host specific data'
    )

    jinja_cmd.set_defaults(cmd=rst_command)


def configure_out_file(file_path, encoding):
    if file_path:
        out_file = open(file_path, 'wb')
    else:
        out_file = sys.stdout.buffer

    return TextIOWrapper(out_file, encoding)


def rst_command(args):
    out_file = configure_out_file(args.output_file, args.out_encoding)

    data = load(args.infile)

    template = Template(args.template.read())

    if args.filter_hosts:
        data_to_render = filter_hosts(args.filter_hosts, data)
    else:
        data_to_render = data

    out_file.write(template.render(**data_to_render))


def load(infile):
    return yaml.load(infile, Loader=yaml.Loader)


def filter_hosts(filter_def, data):
    return {
        'nodes': [
            node for node in data['nodes'] if node['name'] in filter_def
        ]
    }
