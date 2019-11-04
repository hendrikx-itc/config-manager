import argparse

from config_manager.command import doc_init, dot, jinja, \
    rst, report


def main():
    parser = argparse.ArgumentParser(
        description='Utility for managing network configuration descriptions'
    )

    subparsers = parser.add_subparsers()

    doc_init.setup_command_parser(subparsers)
    dot.setup_command_parser(subparsers)
    rst.setup_command_parser(subparsers)
    jinja.setup_command_parser(subparsers)
    report.setup_command_parser(subparsers)

    args = parser.parse_args()

    if hasattr(args, 'cmd'):
        args.cmd(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
