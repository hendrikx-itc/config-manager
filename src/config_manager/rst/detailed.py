from config_manager.rst import render_rst_head


def render_rst(data_to_render, context_data):
    yield from render_rst_head(context_data['title'], '-')
    yield '\n'

    for host in context_data['hosts']:
        yield from render_host(host, context_data)


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


def render_host(host_data, context_data):
    services = host_data.get('services', [])

    yield from render_rst_head(host_data['name'], '~')

    yield '\n'

    yield '{}\n\n'.format(host_data.get('description', 'No description'))

    alternative_names = host_data.get('alternative_names')

    if alternative_names:
        yield 'Alternate Names:\n\n'

        for alternative_name in alternative_names:
            yield '- {}\n'.format(alternative_name)

        yield '\n'

    ip_addresses = host_data.get('ip_addresses')

    if ip_addresses:
        yield 'IP Addresses:\n\n'

        for ip_address in ip_addresses:
            yield '- {}\n'.format(ip_address)

        yield '\n'

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
            rows = [
                service['name'],
                ', '.join(map(str, service['ports']))
            ]

            yield '   {}\n'.format(
                ','.join('"{}"'.format(column) for column in rows)
            )

    yield '\n'

    outgoing_connections = get_outgoing_connections_for(context_data, host_data['name'])
    incoming_connections = get_incoming_connections_for(context_data, host_data['name'])

    if len(outgoing_connections) or len(incoming_connections):
        yield from render_rst_head('Connections', '`')

        def render_connection_table(headers, rows):
            yield '.. csv-table::\n'

            yield '   :header: {}\n'.format(
                ','.join('"{}"'.format(header) for header in headers)
            )
            yield '   :widths: {}\n'.format(
                ','.join(map(str, [12, 1, 12, 2, 2, 2, 24]))
            )
            yield '\n'

            for row in rows:
                yield '   {}\n'.format(
                    ','.join('"{}"'.format(value) for value in row)
                )

            yield '\n'

        if len(outgoing_connections):
            yield from render_rst_head('Outgoing', ',')

            headers = [
                'Source', 'Direction', 'Target', 'Port', 'Transport Protocol',
                'Application Protocol', 'Description'
            ]

            yield from render_connection_table(headers, [
                [
                    c['source'],
                    '→',
                    c['target'],
                    c.get('port', ''),
                    c.get('transport_protocol', ''),
                    c.get('application_protocol', ''),
                    c.get('description', '')
                ]
                for c in outgoing_connections
            ])

        if len(incoming_connections):
            yield from render_rst_head('Incoming', ',')

            headers = [
                'Target', 'Direction', 'Source', 'Port', 'Transport Protocol',
                'Application Protocol', 'Description'
            ]

            yield from render_connection_table(headers, [
                [
                    c['target'],
                    '←',
                    c['source'],
                    c.get('port', ''),
                    c.get('transport_protocol', ''),
                    c.get('application_protocol', ''),
                    c.get('description', '')
                ]
                for c in incoming_connections
            ])
