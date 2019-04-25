import argparse
import sys
from io import TextIOWrapper
from itertools import chain

import yaml

from config_manager.tabulate import render_rst_table


def setup_command_parser(subparsers):
    fw_cmd = subparsers.add_parser(
        'fw', help='command for generating firewall rules matrix'
    )

    fw_cmd.add_argument(
        'infile', type=argparse.FileType('r', encoding='utf-8')
    )

    fw_cmd.add_argument(
        '--output-file', '-o', help='write output to file'
    )

    fw_cmd.add_argument(
        '--out-encoding', default='utf-8', help='encoding of output file'
    )

    fw_cmd.add_argument(
        '--render-method', default='single-list',
        choices=['single-list', 'per-node']
    )

    fw_cmd.set_defaults(cmd=fw_command)


def configure_out_file(file_path, encoding):
    if file_path:
        out_file = open(file_path, 'wb')
    else:
        out_file = sys.stdout.buffer

    return TextIOWrapper(out_file, encoding)


def fw_command(args):
    out_file = configure_out_file(args.output_file, args.out_encoding)

    data = load_yaml(args.infile)

    render_fn = render_methods[args.render_method]

    out_file.writelines(render_fn(data))


def load_yaml(infile):
    return yaml.load(infile, Loader=yaml.Loader)


def render_rst_head(title, underline_char='='):
    yield '{}\n'.format(title)
    yield '{}\n'.format(len(title) * underline_char)


def render_rst_single_list(data):
    title = data.get('title')

    if title:
        rst_title = '{} Firewall Matrix'.format(title)
    else:
        rst_title = 'Firewall Matrix'

    yield from render_rst_head(rst_title)

    node_map = {node['name']: node for node in data['nodes']}

    column_names = [
        'Host', 'IP Addr', 'Direction', 'Other', 'IP Addr', 'Port',
        'Transport Protocol', 'Application Protocol', 'Description'
    ]

    rows = list(chain(*(
        firewall_rows(node_map, node_data)
        for node_data in data['nodes']
    )))

    table_lines = render_rst_table(
        column_names,
        ['<' for _ in column_names],
        ['max' for _ in column_names],
        rows
    )

    for line in table_lines:
        yield '{}\n'.format(line)

    yield '\n'


def firewall_rows(node_map, node_data):
    data_streams = node_data.get('data_streams', [])

    return [
        (
            node_data['name'],
            node_data['ip_addresses'][0],
            stream['direction'],
            stream['other'],
            node_map.get(stream['other'], {}).get('ip_addresses', ['?'])[0],
            stream['port'],
            stream['transport_protocol'],
            stream['application_protocol'],
            stream.get('description', '')
        )
        for stream in data_streams
    ]


def render_rst_per_node(data):
    node_map = {node['name']: node for node in data['nodes']}

    for node_data in data['nodes']:
        data_streams = node_data.get('data_streams')

        if data_streams:
            yield '{}\n'.format(node_data['name'])

            column_names = [
                'Host', 'IP Addr', 'Direction', 'Other', 'IP Addr', 'Port',
                'Transport Protocol', 'Application Protocol', 'Description'
            ]

            rows = [
                (
                    node_data['name'],
                    node_data['ip_addresses'][0],
                    stream['direction'],
                    stream['other'],
                    node_map.get(stream['other']).get('ip_addresses', ['?'])[0],
                    stream['port'],
                    stream['transport_protocol'],
                    stream['application_protocol'],
                    stream.get('description', '')
                )
                for stream in data_streams
            ]

            table_lines = render_rst_table(
                column_names,
                ['<' for _ in column_names],
                ['max' for _ in column_names],
                rows
            )

            for line in table_lines:
                yield '{}\n'.format(line)

            yield '\n'

render_methods = {
    'single-list': render_rst_single_list,
    'per-node': render_rst_per_node
}