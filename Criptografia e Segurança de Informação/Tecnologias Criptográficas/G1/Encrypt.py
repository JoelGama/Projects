from cryptography.fernet import Fernet
import os

inputFile = 'message.txt'
outputFile = 'message.encrypted'

# Key generation
key = Fernet.generate_key()

# Write the key in a key file to the decrypt phase
file = open('key.key', 'wb')
file.write(key)
file.close()

# Read the input file content
with open(inputFile, 'rb') as file:
    data = file.read()

fernet = Fernet(key)

# encrypt step
encrypted = fernet.encrypt(data)

# Write the encrypted message in the output file
with open(outputFile, 'wb') as file:
    file.write(encrypted)

# delete the input file for security
#os.remove("inputFile")
