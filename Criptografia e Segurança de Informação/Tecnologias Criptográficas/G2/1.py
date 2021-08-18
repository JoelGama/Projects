import os
import sys
import getpass
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def file_encrypt(data,secret):

    # Define salt value
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    # Key used to fernet
    key = base64.urlsafe_b64encode(kdf.derive(secret))

    f = Fernet(key)

    # encrypt step
    encrypted = f.encrypt(data)

    # encrypted message plus salt
    return salt + encrypted

def file_decrypt(encodeText,secretDecode):

    salt = encodeText[:16]
    text = encodeText[16:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    # Key used to fernet
    key = base64.urlsafe_b64encode(kdf.derive(secretDecode))

    f = Fernet(key)

    # Decrypted data
    data = f.decrypt(text)

    return data


def main():

    # Open message file
    with open(sys.argv[1], 'rb') as file:
        data = file.read()

    # get user password
    password = getpass.getpass()
    password = bytes(password,encoding='utf8')

    # encrypted data
    output = file_encrypt(data,password)

    # encrypted file
    with open('outputFile.txt', 'wb') as file:
        file.write(output)

    # get user password
    passwordDecode = getpass.getpass()
    passwordDecode = bytes(passwordDecode,encoding='utf8')

    if passwordDecode == password:
        # Decrypt
        output2 = file_decrypt(output,passwordDecode)
        # Write original message
        with open('final.txt', 'wb') as file:
            file.write(output2)
    else:
        # If password is wrong
        print("Wrong Password!")

if __name__ == "__main__":
    main()