from config_manager.rst import render_rst_head


def render_rst(data):
    yield from render_rst_head(data['title'], '-')
    yield '\n'

    for host in data['hosts']:
        yield from render_host(host)


def render_host(host_data):
    services = host_data.get('services', [])
    connections = host_data.get('connections', [])

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
            columns = [
                service['name'],
                ', '.join(map(str, service['ports']))
            ]

            yield '   {}\n'.format(
                ','.join('"{}"'.format(column) for column in columns)
            )

    yield '\n'

    if len(connections):
        yield from render_rst_head('Streams', '`')

        yield '.. csv-table::\n'

        headers = [
            'Direction', 'Other', 'Port', 'Transport Protocol',
            'Application Protocol', 'Description'
        ]

        yield '   :header: {}\n'.format(
            ','.join('"{}"'.format(header) for header in headers)
        )
        yield '   :widths: {}\n'.format(
            ','.join(map(str, [1, 12, 2, 2, 2, 24]))
        )
        yield '\n'

        for data_stream in connections:
            direction_str = data_stream['direction']

            if direction_str == '->':
                direction = '→'
            elif direction_str == '<-':
                direction = '←'

            columns = [
                direction,
                data_stream['other'],
                data_stream.get('port', ''),
                data_stream.get('transport_protocol', ''),
                data_stream.get('application_protocol', ''),
                data_stream.get('description', '')
            ]

            yield '   {}\n'.format(
                ','.join('"{}"'.format(column) for column in columns)
            )

        yield '\n'
