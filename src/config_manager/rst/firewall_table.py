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

    host_map = {host['name']: host for host in context_data['hosts']}

    column_names = [
        'Source', 'IP Addr', 'Direction', 'Target', 'IP Addr', 'Port',
        'Transport Protocol', 'Application Protocol', 'Description'
    ]

    def get_connections_for(host_name):
        return [c for c in data['connections'] if c['source'] == host_name or c['target'] == host_name]

    rows = list(chain(*(
        firewall_rows(host_map, get_connections_for(host_data['name']))
        for host_data in data['hosts']
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


def get_attr(host_data, name):
    try:
        return host_data[name]
    except KeyError as e:
        raise Exception("Missing {} for host {}".format(name, host_data['name']))


def firewall_rows(host_map, connections):
    def make_row(connection):
        try:
            source = host_map[connection['source']]
        except KeyError:
            raise Exception('Missing information target of connection: {}'.format(connection['source']))

        try:
            target = host_map[connection['target']]
        except KeyError:
            raise Exception('Missing information target of connection: {}'.format(connection['target']))

        source_addr = source.get('ip_addresses', ['?'])[0]
        target_addr = target.get('ip_addresses', ['?'])[0]

        return (
            connection['source'],
            source_addr,
            '->',
            connection['target'],
            target_addr,
            connection['port'],
            connection['transport_protocol'],
            connection['application_protocol'],
            connection.get('description', '')
        )

    return [make_row(connection) for connection in connections]


def get_incoming_connections_for(data, host_name):
    return [
        c for c in data['connections']
        if c['target'] == host_name
    ]


def get_outgoing_connections_for(data, host_name):
    return [
        c for c in data['connections']
        if c['source'] == host_name
    ]


def render_rst_per_host(data, context_data):
    host_map = {host['name']: host for host in context_data['hosts']}

    for host_data in data['hosts']:
        incoming_connections = get_incoming_connections_for(context_data, host_data['name'])
        outgoing_connections = get_outgoing_connections_for(context_data, host_data['name'])

        if incoming_connections or outgoing_connections:
            yield '{}\n'.format(host_data['name'])

            column_names = [
                'Host', 'IP Addr', 'Direction', 'Other', 'IP Addr', 'Port',
                'Transport Protocol', 'Application Protocol', 'Description'
            ]

            rows = [
                (
                    host_data['name'],
                    host_data['ip_addresses'][0],
                    '->',
                    connection['target'],
                    host_map.get(connection['target']).get('ip_addresses', ['?'])[0],
                    connection['port'],
                    connection['transport_protocol'],
                    connection['application_protocol'],
                    connection.get('description', '')
                )
                for connection in outgoing_connections
            ]

            rows.extend(
                (
                    host_data['name'],
                    host_data['ip_addresses'][0],
                    '<-',
                    connection['source'],
                    host_map.get(connection['source']).get('ip_addresses', ['?'])[0],
                    connection['port'],
                    connection['transport_protocol'],
                    connection['application_protocol'],
                    connection.get('description', '')
                )
                for connection in incoming_connections
            )

            table_lines = render_rst_table(
                column_names,
                ['<' for _ in column_names],
                ['max' for _ in column_names],
                rows
            )

            for line in table_lines:
                yield '{}\n'.format(line)

            yield '\n'
