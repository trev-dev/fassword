import json
from cryptography.fernet import Fernet


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


def encrypt(string, key=False):
    if not key:
        key = Fernet.generate_key()
    else:
        key = bytes(key, 'utf-8')

    fernet = Fernet(key)
    encrypted = fernet.encrypt(bytes(string, 'utf-8'))

    return (encrypted.decode('utf-8'), key.decode('utf-8'))


def decrypt(string, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(bytes(string, 'utf-8'))
    return decrypted.decode('utf-8')
