

def include_filter(includes):
    def filter_fn(value):
        return value in includes

    return filter_fn


def exclude_filter(includes):
    def filter_fn(value):
        return value in includes

    return filter_fn


def filter_hosts(filter_fn, data):
    # Copy everything except the 'nodes' key
    result = {
        key: value
        for key, value in data.items() if key != 'nodes'
    }

    # Add filtered nodes list
    result['nodes'] = [
        node for node in data['nodes'] if filter_fn(node['name'])
    ]

    return result
