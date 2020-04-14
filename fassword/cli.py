from getpass import getpass
from fassword.utils import load_data, save_data, choose_password
from cryptography.fernet import Fernet
import pyperclip
from sys import exit


def init_data():
    data = load_data()
    print('\nInitializing Fassword\n')

    password = choose_password()
    key = Fernet.generate_key()
    fern = Fernet(key)
    master = fern.encrypt(bytes(password, 'utf-8'))

    data = {
        'key': key.decode('utf-8'),
        'master': master.decode('utf-8'),
        'entry': {

        }
    }

    save_data(data)
    exit('\nFassword is ready. Type fass -h for options\n')


def add_entry(entry):
    data = load_data()

    if entry in data['entry']:
        exit('\nEntry already exists')

    print(f'\nChoose a password for {entry}')
    password = choose_password()
    f = Fernet(bytes(data['key'], 'utf-8'))
    encrypted = f.encrypt(bytes(password, 'utf-8'))

    data['entry'][entry] = encrypted.decode('utf-8')
    save_data(data)
    print(f'\nEntry for {entry} created!')


def decrypt_entry(entry):
    data = load_data()
    if entry not in data['entry']:
        exit(f'Entry for {entry} does not yet exist')

    f = Fernet(bytes(data['key'], 'utf-8'))
    password = f.decrypt(bytes(data['entry'][entry], 'utf-8'))

    pyperclip.copy(password.decode('utf-8'))
    print(f'Password for {entry} copied to the clipboard')


def update_entry(entry):
    data = load_data()

    if entry not in data['entry']:
        exit(f'Entry for {entry} does not yet exist')

    f = Fernet(bytes(data['key'], 'utf-8'))
    print(f'\nEnter the new password for {entry}')
    password = choose_password()
    encrypted = f.encrypt(bytes(password, 'utf-8'))
    data['entry'][entry] = encrypted.decode('utf-8')
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
    attempt = bytes(getpass('Enter your master password: '), 'utf-8')
    f = Fernet(bytes(data['key'], 'utf-8'))
    master = f.decrypt(bytes(data['master'], 'utf-8'))

    if attempt == master:
        return True
    return False
