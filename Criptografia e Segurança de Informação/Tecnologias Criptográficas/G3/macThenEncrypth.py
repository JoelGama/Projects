import os
import sys
import json
import base64
import hmac
import getpass
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.algorithms import ChaCha20
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def file_encrypt(data,secret):

    # Salt for kdf
    salt = os.urandom(16)

    # Key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    # Key for encrypt and MAC
    key = base64.urlsafe_b64encode(kdf.derive(secret))

    # Key and nonce for Enrypt
    kenc = key[:32]
    nonce = os.urandom(16)

    # Key for MAC
    kmac = key[32:]

    # MAC from the message
    mac = hmac.new(kmac, data, hashlib.sha256).digest()

    # Encrypt MAC + Message (with ChaCha20)
    algorithm = ChaCha20(kenc,nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor  = cipher.encryptor()
    ciphertext = encryptor.update(mac+data)

    nonce = base64.b64encode(nonce).decode('utf-8')
    ct = base64.b64encode(ciphertext).decode('utf-8')

    saltsafe = base64.b64encode(salt).decode('utf-8')

    # Encrypted message
    output = json.dumps({'nonce':nonce, 'ciphertext':ct, 'salt':saltsafe})

    return output

def file_decrypt(secret, output):

    # Json content
    b64   = json.loads(output)
    nonce = base64.b64decode(b64['nonce'])
    ct    = base64.b64decode(b64['ciphertext'])
    salt  = base64.b64decode(b64['salt'])

    # key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    # Key for encrypt and MAC
    key = base64.urlsafe_b64encode(kdf.derive(secret))

    # Key for decrypt
    kenc = key[:32]

    # Key for MAC
    kmac = key[32:]

    # Decrypt step (with ChaCha20)
    algorithm = ChaCha20(kenc,nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor  = cipher.decryptor()
    ciphertext = decryptor.update(ct)

    # MAC and message decrypted
    tag  = ciphertext[:32]
    data = ciphertext[32:]

    mac = hmac.new(kmac, data, hashlib.sha256).digest()

    # Compare MAC tags
    if mac == tag:
        return data
    else:
        errorMessage = bytes("Error",encoding='utf8')
        return errorMessage

def main():

    # Open message file
    with open(sys.argv[1], 'rb') as file:
        data = file.read()

    # get user password
    password = getpass.getpass()
    password = bytes(password,encoding='utf8')

    # encrypt
    output = file_encrypt(data,password)

    # get user password
    passwordDecode = getpass.getpass()
    passwordDecode = bytes(passwordDecode,encoding='utf8')

    if passwordDecode == password:
        # Decrypt
        output2 = file_decrypt(passwordDecode,output)
        # Write original message
        with open('final.txt', 'wb') as file:
            file.write(output2)
    else:
        # If password is wrong
        print("Wrong Password!")

if __name__ == "__main__":
    main()