import fassword.cli as cli
from fassword.utils import load_data
from sys import exit
import argparse

parser = argparse.ArgumentParser(
    description="A password storage program powered by Fernet",
    prog="fass"
)

parser.add_argument(
    'entry',
    nargs="?",
    default=False,
    type=str,
    help='Desired password entry'
)

parser.add_argument(
    '-a',
    '--add',
    action="store_true",
    help="Add an entry to your storage"
)

parser.add_argument(
    '-u',
    '--update',
    action="store_true",
    help="Update an entry"
)

parser.add_argument(
    '-r',
    '--remove',
    action="store_true",
    help="Remove an entry"
)

parser.add_argument(
    '-l',
    '--list',
    action="store_true",
    help="List passwords for a given user."
)


def main():
    args = parser.parse_args()
    data = load_data()

    if not data:
        cli.init_data()

    if cli.unlock_entries():
        if not args.entry and args.list:
            cli.list_entries()
        elif not args.entry:
            parser.print_help()
            exit('\n Error: No entry specified')

        if args.add:
            cli.add_entry(args.entry)
        elif args.update:
            cli.update_entry(args.entry)
        elif args.remove:
            cli.delete_entry(args.entry)
        else:
            if args.entry:
                cli.decrypt_entry(args.entry)

    else:
        print('Invalid Master Password')


main()
