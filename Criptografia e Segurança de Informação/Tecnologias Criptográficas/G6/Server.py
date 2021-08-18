import os
import asyncio
import socket
import base64
import hashlib
from Crypto.Cipher import AES
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import ParameterFormat
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_der_parameters
from cryptography.hazmat.primitives.serialization import load_der_public_key

conn_cnt = 0
conn_port = 8888
max_msg_size = 9999

class ServerWorker(object):

    """ Classe que implementa a funcionalidade do SERVIDOR. """
    def __init__(self, cnt, parameters, addr=None):
        """ Construtor da classe. """
        self.id = cnt
        self.addr = addr
        self.msg_cnt = 0
        self.parameters = parameters
        self.server_private_key = None
        self.public_key = None
        self.shared_key = None

    def process(self, msg):
        if (self.msg_cnt == 0):
            print('READY')

            self.server_private_key = self.parameters.generate_private_key()
            self.public_key         = self.server_private_key.public_key()

            new  = self.parameters.parameter_bytes(Encoding.DER, ParameterFormat.PKCS3)
            new2 = self.public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
            
            new_msg = b"".join([new, new2])

            self.msg_cnt += 1
        elif (self.msg_cnt == 1):

            client_key = load_der_public_key(msg, backend=default_backend())
            self.shared_key = self.server_private_key.exchange(client_key)
            new_msg = bytes("Done".encode('utf-8'))
            self.msg_cnt += 1

        else:
            enc = base64.b64decode(msg)

            if len(self.shared_key) not in (16, 24, 32):
                key = hashlib.sha256(self.shared_key).digest()

            nonce = enc[:32]
            digest = enc[-AES.block_size:]
            cipher = AES.new(key, AES.MODE_GCM, nonce = nonce)

            txt1 = enc[32:]
            cipher_text = txt1[:-AES.block_size]

            plaintext = cipher.decrypt_and_verify(cipher_text, digest)

            print('%d : %r' % (self.id,plaintext.decode('utf-8')))
            new_msg = plaintext.upper()

            self.msg_cnt += 1

        return new_msg if len(new_msg)>0 else None

# Funcionalidade Cliente/Servidor
@asyncio.coroutine
def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt +=1
    addr = writer.get_extra_info('peername')
    parameters = dh.generate_parameters(generator=2, key_size=2048,
                                            backend=default_backend())
    srvwrk = ServerWorker(conn_cnt,parameters,addr)
    data = yield from reader.read(max_msg_size)
    while True:
        if not data: continue
        if data[:1]==b'\n': break
        data = srvwrk.process(data)
        if not data: break
        writer.write(data)
        yield from writer.drain()
        data = yield from reader.read(max_msg_size)
    print("[%d]" % srvwrk.id)
    writer.close()

def run_server():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', conn_port, loop=loop)
    server = loop.run_until_complete(coro)
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    print('  (type ^C to finish)\n')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print('\nFINISHED!')

run_server()