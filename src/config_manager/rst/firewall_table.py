from itertools import chain

from config_manager.rst import render_rst_head
from config_manager.tabulate import render_rst_table


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
