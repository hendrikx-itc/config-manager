

def include_filter(includes):
    def filter_fn(value):
        return value in includes

    return filter_fn


def exclude_filter(includes):
    def filter_fn(value):
        return value in includes

    return filter_fn


def filter_hosts(filter_fn, data):
    # Copy everything except the 'hosts' key
    result = {
        key: value
        for key, value in data.items() if key != 'hosts'
    }

    # Add filtered hosts list
    result['hosts'] = [
        host for host in data['hosts'] if filter_fn(host['name'])
    ]

    return result
