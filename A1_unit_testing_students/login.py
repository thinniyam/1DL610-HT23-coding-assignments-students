import json

# Login as a user
def login():
    username = input('Enter your username: ')

    # Look for user in database
    with open('users.json', 'r') as file:
        data = json.load(file)
        user = None
        for entry in data:
            if entry.get('username') == username:
                user = entry
                password = input('Enter your password: ')
                if entry.get('password') == password:
                    print('Successfully logged in.')
                    return {
                        'username': entry.get('username'),
                        'wallet': entry.get('wallet'),
                    }
                else:
                    print('The password was incorrect.')
                    return None

        # register new user
        if user is None:
            register_confirmation = input('User not found! Would you like to register? (Y/N): ')
            if register_confirmation.upper() == 'Y':
                while True:
                    password = input('Enter your password: ')
                    validation_errors = validate_password(password)
                    if not validation_errors:
                        save_user({
                            'username': username,
                            'password': password,
                            'wallet': 0,
                        })
                        print('Your account was created successfully.')
                        break
                    else:
                        for validation_error in validation_errors.values():
                            print(validation_error)
        return None


def save_user(user):
    """
    Save the new user into database.

    :param user: the user dictionary
    :return: void
    """
    with open('users.json', 'r+') as file:
        users = json.load(file)
        users.append(user)

        # Update the users.json file
        file.seek(0)
        json.dump(users, file, indent=4)
        file.close()


def check_username(data, username):
    """
    Check if the user already exists.

    :param data: the list of existing users
    :param username: the username of the new user
    :return: boolean
    """
    return any(user.get('username') == username for user in data)


def validate_password(password):
    """
    Validates the password criteria.

    :param password: the password
    :return: dictionary: the list of errors
    """
    allowed_symbols = ['@', '$', '#', '&', '%']
    min_length = 8
    errors = {}

    if len(password) >= min_length:
        if not any(char.isupper() for char in password):
            errors.update({'capital': 'The password must contain at least one capital letter.'})

        if not any(not char.isalnum() for char in password):
            errors.update({'symbol': 'The password must contain at least one special symbol.'})
    else:
        errors.update({'length': 'The password must be at least eight characters.'})

    return errors
