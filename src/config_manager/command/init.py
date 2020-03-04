import os
from collections import OrderedDict

import git
import yaml
from jinja2 import Template


def setup_command_parser(subparsers):
    init_cmd = subparsers.add_parser(
        'init', help='Initialize configuration project'
    )

    init_cmd.add_argument('dir', nargs='?')

    init_cmd.set_defaults(cmd=init_command)


def init_command(args):
    if args.dir:
        path = args.dir
    else:
        path = os.getcwd()

    try:
        git_repo = git.Repo(path, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError as exc:
        print(f"No git repository found at {path}")
    else:
        print(f"Initializing configuration project in {git_repo.working_dir} ...")

        initialize_project(git_repo.working_dir)


def initialize_project(project_root):
    config_data_file_path = os.path.join(project_root, 'configuration.yaml')

    create_config_data_file(config_data_file_path)

    print(f"Created configuration data file {config_data_file_path}")

    template_dir = os.path.join(project_root, 'templates')

    os.mkdir(template_dir)

    print(f"Created template directory {template_dir}")

    template_file_path = os.path.join(project_root, 'templates', 'services.jinja')

    create_template_file(template_file_path)

    print(f"Created template file {template_file_path}")

    config_file_path = os.path.join(project_root, '.config_manager')

    create_config_file(config_file_path)

    print(f"Created project config file {config_file_path}")


def create_config_data_file(file_path):
    sample_config_data = OrderedDict([
        ('title', 'Example configuration data file'),
        ('networks', [
            OrderedDict([
                ('name', 'core'),
                ('description', 'The description of this core network that explains its purpose'),
                ('range', '172.168.1.0/24')
            ])
        ]),
        ('hosts', [
            OrderedDict([
                ('name', 'first_host'),
                ('description', 'Serves the web application on the local network.'),
                ('fqdn', 'first_host.core.network.local'),
                ('ip_addresses', [
                    '172.168.1.100'
                ]),
                ('tags', ['managed', 'physical', 'rack1']),
                ('roles', ['web_server', 'postgres_db'])
            ])
        ])
    ])

    with open(file_path, 'w') as out_file:
        ordered_dump(
            sample_config_data, out_file, Dumper=yaml.SafeDumper, indent=2
        )


def create_template_file(file_path):
    with open(file_path, 'w') as out_file:
        out_file.write("""\
{%- for host in hosts if 'roles' in host -%}
# {{ host['name'] }}

{{ host['description'] }}

## Services
{%- for role in host['roles'] %}
  - {{ role }}
{%- endfor %}

{% endfor %}
""")


def create_config_file(file_path):
    sample_config = OrderedDict([
        ('config_path', 'configuration.yaml'),
        ('reports', [
            OrderedDict([
                ('name', 'services'),
                ('file', 'templates/services.jinja'),
                ('engine', 'jinja')
            ])
        ])
    ])

    with open(file_path, 'w') as out_file:
        ordered_dump(
            sample_config, out_file, Dumper=yaml.SafeDumper, indent=2
        )


def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items()
        )

    OrderedDumper.add_representer(OrderedDict, _dict_representer)

    return yaml.dump(data, stream, OrderedDumper, **kwds)


