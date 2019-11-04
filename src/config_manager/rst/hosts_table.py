from config_manager.tabulate import render_rst_table
from config_manager.rst import render_rst_head


def render_rst_single_list(data, context_data):
    yield from render_rst_head('Hosts')

    yield '\n'

    column_names = [
        'Host', 'IP Address', 'Description'
    ]

    rows = [
        (
            host_data['name'],
            host_data.get('ip_addresses', ['?'])[0],
            host_data.get('description', '').strip()
        )
        for host_data in data['hosts']
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
