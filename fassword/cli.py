from getpass import getpass
from fassword.utils import (
    load_data,
    save_data,
    decrypt,
    encrypt,
    create_storage
)
import pyperclip
from sys import exit


def choose_password():
    passwords_match = False

    while not passwords_match:
        password = getpass(f'Enter new password: ')
        confirm = getpass(f'Confirm password: ')

        if password == confirm:
            passwords_match = True
            break
        print('\nPasswords do not match.\n')

    return password


def init_data():
    data = load_data()
    print('\nInitializing Fassword\n')

    print('You must choose a master password\n')
    password = choose_password()
    master, key = encrypt(password)

    data = create_storage(master, key)

    save_data(data)
    exit('\nFassword is ready. Type fass -h for options\n')


def add_entry(entry):
    data = load_data()

    if entry in data['entry']:
        exit('\nEntry already exists')

    print(f'\nChoose a password for {entry}')
    password = choose_password()
    encrypted = encrypt(password, data['key'])[0]

    data['entry'][entry] = encrypted
    save_data(data)

    print(f'\nEntry for {entry} created!')


def decrypt_entry(entry):
    data = load_data()
    if entry not in data['entry']:
        exit(f'Entry for {entry} does not yet exist')

    password = decrypt(data['entry'][entry], data['key'])

    pyperclip.copy(password)
    print(f'Password for {entry} copied to the clipboard')


def update_entry(entry):
    data = load_data()

    if entry not in data['entry']:
        exit(f'Entry for {entry} does not yet exist')

    print(f'\nEnter the new password for {entry}')
    password = choose_password()
    encrypted = encrypt(password, data['key'])[0]
    data['entry'][entry] = encrypted
    print('\nPassword Updated')

    save_data(data)


def delete_entry(entry):
    data = load_data()

    if entry not in data['entry']:
        exit(f'\nCannot delete {entry} because it does not exist')

    message = (
        f'WARNING! You are about to delete your entry for {entry}!\n'
        f'If you are sure about this, please type "{entry}" to confirm'
    )

    print(message)
    confirm = input('Confirm: ')

    if confirm == entry:
        del data['entry'][entry]
        save_data(data)
        print(f'\n{entry} deleted')
    else:
        print('\nBacking out...')


def list_entries():
    data = load_data()
    print('Entries:')
    for entry in data['entry'].keys():
        print(entry)


def unlock_entries():
    data = load_data()
    attempt = getpass('Enter your master password: ')
    master = decrypt(data['master'], data['key'])

    if attempt == master:
        return True
    return False
