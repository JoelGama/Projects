import os
import asyncio
import socket
import base64
import hashlib
from Crypto.Cipher import AES
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import ParameterFormat
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_der_parameters
from cryptography.hazmat.primitives.serialization import load_der_public_key

conn_port = 8888
max_msg_size = 9999

class Client:

    """ Classe que implementa a funcionalidade de um CLIENTE. """
    def __init__(self, sckt=None):
        """ Construtor da classe. """
        self.sckt = sckt
        self.msg_cnt = 0
        self.client_private_key = None
        self.client_public_key = None
        self.shared_key = None

    def process(self, msg=b""):
        """ Processa uma mensagem (`bytestring`) enviada pelo SERVIDOR.
            Retorna a mensagem a transmitir como resposta (`None` para
            finalizar ligação) """
        if (self.msg_cnt == 0):

            new_msg = bytes("Hello".encode('utf-8'))
            self.msg_cnt += 1

        elif (self.msg_cnt == 1):
            txt1 = msg[:268]
            txt2 = msg[268:]

            parameters        = load_der_parameters(txt1, backend=default_backend())
            server_public_key = load_der_public_key(txt2, backend=default_backend())

            self.client_private_key = parameters.generate_private_key()
            self.client_public_key  = self.client_private_key.public_key()
            self.shared_key         = self.client_private_key.exchange(server_public_key)

            new_msg = self.client_public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
            self.msg_cnt +=1
        else:
            nonce = os.urandom(32)

            if len(self.shared_key) not in (16, 24, 32):
                key = hashlib.sha256(self.shared_key).digest()

            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

            data = input()
            (cipher_text, digest) = cipher.encrypt_and_digest(data.encode('utf-8'))

            print('Received (%d): %r' % (self.msg_cnt,data))
            print('Input message to send (empty to finish)')

            new_msg = (base64.b64encode(nonce+cipher_text+digest))
            self.msg_cnt +=1

        return new_msg if len(new_msg)>0 else None

# Funcionalidade Cliente/Servidor
@asyncio.coroutine
def tcp_echo_client(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    reader, writer = yield from asyncio.open_connection('127.0.0.1',
                                                        conn_port, loop=loop)
    addr = writer.get_extra_info('peername')
    client = Client(addr)
    msg = client.process()
    while msg:
        writer.write(msg)
        msg = yield from reader.read(max_msg_size)
        if msg :
            msg = client.process(msg)
        else:
            break
    writer.write(b'\n')
    print('Socket closed!')
    writer.close()

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()