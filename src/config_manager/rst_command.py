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


def render_field_list_item(name, value):
    indentation = (len(name) + 3) * ' '

    if hasattr(value, '__iter__') and not isinstance(value, str):
        it = iter(value)
        first = next(it)
        yield ':{}: - {}\n'.format(name, first)

        try:
            while True:
                next_value = next(it)

                yield '{}- {}\n'.format(indentation, next_value)
        except StopIteration:
            pass
    else:
        yield ':{}: {}\n'.format(name, value)


def render_rst_head(title, underline_char='='):
    yield '{}\n'.format(title)
    yield '{}\n'.format(len(title) * underline_char)


def render_rst(data):
    yield from render_rst_head('Nodes', '-')
    yield '\n'

    for host in data['nodes']:
        services = host.get('services', [])
        data_streams = host.get('data_streams', [])

        yield from render_rst_head(host['name'], '~')

        alternative_names = host.get('alternative_names', [])

        yield from render_field_list_item('Alternate Names', alternative_names)

        ip_addresses = host.get('ip_addresses', [])

        yield from render_field_list_item('IP Addresses', ip_addresses)

        yield '\n'

        if len(services):
            yield from render_rst_head('Services', '`')

            yield '.. csv-table::\n'

            headers = [
                'Name', 'Ports'
            ]

            yield '   :header: {}\n'.format(
                ','.join('"{}"'.format(header) for header in headers)
            )
            yield '\n'

            for service in services:
                columns = [
                    service['name'],
                    ', '.join(map(str, service['ports']))
                ]

                yield '   {}\n'.format(
                    ','.join('"{}"'.format(column) for column in columns)
                )

        yield '\n'

        if len(data_streams):
            yield from render_rst_head('Streams', '`')

            yield '.. csv-table::\n'

            headers = [
                'Other', 'Direction', 'Port', 'Transport Protocol',
                'Application Protocol', 'Description'
            ]

            yield '   :header: {}\n'.format(
                ','.join('"{}"'.format(header) for header in headers)
            )
            yield '\n'

            for data_stream in data_streams:
                direction_str = data_stream['direction']

                if direction_str == '->':
                    direction = '→'
                elif direction_str == '<-':
                    direction = '←'

                columns = [
                    data_stream['other'],
                    direction,
                    data_stream.get('port', ''),
                    data_stream.get('transport_protocol', ''),
                    data_stream.get('application_protocol', ''),
                    data_stream.get('description', '')
                ]

                yield '   {}\n'.format(
                    ','.join('"{}"'.format(column) for column in columns)
                )

            yield '\n'
