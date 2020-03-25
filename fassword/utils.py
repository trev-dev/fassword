import json
from getpass import getpass


def yes_or_no(prompt):
    """
    Evaluates a yes or no response. Returns True if yes, False if no.
    """
    resp = input(prompt).lower()
    yes = set(['yes', 'y'])
    no = set(['no', 'n'])

    if resp in no:
        return False
    elif resp in yes:
        return True
    return False


def choose_password():
    passwords_match = False

    while not passwords_match:
        password = getpass(f'Enter new master password: ')
        confirm = getpass(f'Confirm password: ')

        if password == confirm:
            passwords_match = True
            break
        print('\nPasswords do not match.\n')

    return password


def load_data():
    """
    Load the password & user data from the database
    """
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        with open('data.json', 'w+') as f:
            data = {}
            json.dump(data, f)
    finally:
        return data


def save_data(data):
    """
    Save the password data to the database
    """
    with open('data.json', 'w+') as f:
        json.dump(data, f)
