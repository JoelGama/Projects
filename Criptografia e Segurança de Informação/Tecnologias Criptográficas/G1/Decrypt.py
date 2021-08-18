from cryptography.fernet import Fernet
import os

input_file = 'message.encrypted'
output_file = 'message.txt'

# Read the key from the key file
file = open('key.key', 'rb')
key = file.read()
file.close()

# Read the encrypted file
with open(input_file, 'rb') as f:
    data = f.read()

fernet = Fernet(key)

# decrypt step
encrypted = fernet.decrypt(data)

# write the decrypted message in the output file
with open(output_file, 'wb') as f:
    f.write(encrypted)
