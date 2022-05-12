import hashlib
import random
from string import ascii_lowercase, ascii_uppercase, digits

salt_string = ascii_lowercase + ascii_uppercase + digits


def generate_salt(_k: int = 8):
    """

    :param _k:
    :return:
    """
    return "".join(random.choices(salt_string, k=_k))


def get_hash(_string: str, _salt: str = generate_salt(8)):
    """
    :param _string:
    :param _salt:
    :return: sha3_256($_string.$salt)
    """
    return hashlib.sha3_256((_string + _salt).encode()).hexdigest() + ":" + _salt


def check_hash(input_password: str, password_salt_hash: str):
    """
    :param input_password:
    :param password_salt_hash:
    :return: sha3_256($input.$salt) == sha3_256($pass.$salt)
    """
    try:
        return get_hash(input_password, password_salt_hash.split(":")[1]) == password_salt_hash
    except IndexError:
        return False


if __name__ == '__main__':
    a = get_hash("123456", generate_salt(8))
    b = check_hash("123456", a)
    print(a, b)
