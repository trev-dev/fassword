import fassword.entries as entries
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
        entries.init_data()

    if entries.unlock_entries():
        if not args.entry and args.list:
            entries.list_entries()
        elif not args.entry:
            parser.print_help()
            exit('\n Error: No entry specified')

        if args.add:
            entries.add_entry(args.entry)
        elif args.update:
            entries.update_entry(args.entry)
        elif args.remove:
            entries.delete_entry(args.entry)
        else:
            if args.entry:
                entries.decrypt_entry(args.entry)

    else:
        print('Invalid Master Password')


main()
