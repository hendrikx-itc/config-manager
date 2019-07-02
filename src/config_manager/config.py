import argparse

from config_manager import dot_command, rst_command, doc_init_command


def main():
    parser = argparse.ArgumentParser(
        description='Utility for managing network configuration descriptions'
    )

    subparsers = parser.add_subparsers()

    doc_init_command.setup_command_parser(subparsers)
    dot_command.setup_command_parser(subparsers)
    rst_command.setup_command_parser(subparsers)

    args = parser.parse_args()

    if hasattr(args, 'cmd'):
        args.cmd(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
