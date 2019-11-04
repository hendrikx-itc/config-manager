import argparse
import sys
from io import TextIOWrapper

import yaml

from config_manager.rst import detailed, hosts_table, firewall_table
from config_manager.filter import filter_hosts, include_filter


output_map = {
    'detailed': detailed.render_rst,
    'hosts': hosts_table.render_rst_single_list,
    'firewall-rules': firewall_table.render_rst_single_list,
    'firewall-rules-per-host': firewall_table.render_rst_per_host
}


def setup_command_parser(subparsers):
    rst_cmd = subparsers.add_parser(
        'rst', help='generate RestructuredText output'
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

    rst_cmd.add_argument(
        '--type', default='detailed', help='type of output',
        choices=output_map.keys()
    )

    rst_cmd.add_argument(
        '--filter-hosts', help='filter host specific data'
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

    renderer = output_map[args.type]

    if args.filter_hosts:
        data_to_render = filter_hosts(include_filter(args.filter_hosts), data)
    else:
        data_to_render = data

    out_file.writelines(renderer(data_to_render, data))


def load(infile):
    return yaml.load(infile, Loader=yaml.Loader)
