from itertools import chain

from config_manager.rst import render_rst_head
from config_manager.tabulate import render_rst_table


def render_rst_single_list(data, context_data):
    title = data.get('title')

    if title:
        rst_title = '{} Firewall Matrix'.format(title)
    else:
        rst_title = 'Firewall Matrix'

    yield from render_rst_head(rst_title)

    node_map = {node['name']: node for node in context_data['nodes']}

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


def get_attr(node_data, name):
    try:
        return node_data[name]
    except KeyError as e:
        raise Exception("Missing {} for node {}".format(name, node_data['name']))


def firewall_rows(node_map, node_data):
    connections = node_data.get('connections', [])

    def make_row(connection):
        try:
            other = node_map[connection['other']]
        except KeyError:
            raise Exception('Missing information for other side of connection: {}'.format(connection['other']))

        return (
            get_attr(node_data, 'name'),
            get_attr(node_data, 'ip_addresses')[0],
            connection['direction'],
            connection['other'],
            get_attr(other, 'ip_addresses')[0],
            connection['port'],
            connection['transport_protocol'],
            connection['application_protocol'],
            connection.get('description', '')
        )

    return [make_row(connection) for connection in connections]


def render_rst_per_node(data):
    node_map = {node['name']: node for node in data['nodes']}

    for node_data in data['nodes']:
        connections = node_data.get('connections')

        if connections:
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
                for stream in connections
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
