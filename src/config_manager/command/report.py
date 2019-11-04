import os

import git
import yaml
from jinja2 import Template


def setup_command_parser(subparsers):
    show_cmd = subparsers.add_parser(
        'report', help='Generate report'
    )

    show_cmd.add_argument('report', nargs='?')

    show_cmd.set_defaults(cmd=report_command)


def report_command(args):
    path = os.getcwd()

    try:
        git_repo = git.Repo(path, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError as exc:
        print("No git repository found at {}".format(path))
    else:
        config_file_path = os.path.join(git_repo.working_dir, '.config_manager')

        with open(config_file_path) as config_file:
            config = load_config(config_file)

        if args.report:
            with open(config['config_path']) as infile:
                data = load_config(infile)

            for report in config['reports']:
                if report['name'] == args.report:
                    render_template(report, data)
        else:
            print('Available reports:')
            for report in config['reports']:
                print(' - {}'.format(report['name']))


def load_config(infile):
    return yaml.load(infile, Loader=yaml.Loader)


def render_template(template, data):
    with open(template['file']) as template_file:
        template = Template(template_file.read())

    print(template.render(**data))
