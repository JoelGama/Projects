import os
import sys
import getpass
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def file_encrypt(data,secret):

    # Define salt value
    salt = os.urandom(16)

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )

    # Key used to fernet
    key = base64.urlsafe_b64encode(kdf.derive(secret))

    # Write the kdf key in a keystore file
    file = open('message.keystore', 'wb')
    file.write(key)
    file.close()

    f = Fernet(key)

    # encrypt step
    encrypted = f.encrypt(data)

    # encrypted message plus salt
    return encrypted

def file_decrypt(encodeText):

    # Open keystore file to get kdf key
    file = open('message.keystore', 'rb')
    key = file.read()
    file.close()

    f = Fernet(key)

    # Decrypted data
    data = f.decrypt(encodeText)

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
        output2 = file_decrypt(output)
        # Write original message
        with open('final.txt', 'wb') as file:
            file.write(output2)
    else:
        # If password is wrong
        print("Wrong Password!")

if __name__ == "__main__":
    main()