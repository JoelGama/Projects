import os
import asyncio
import socket
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.padding import PSS

conn_cnt = 0
conn_port = 8888
max_msg_size = 9999

class ServerWorker(object):

    def __init__(self, cnt, private_key, public_key, addr=None):
        self.id = cnt
        self.msg_cnt = 0
        self.addr = addr
        self.server_private_key = private_key
        self.client_public_key = public_key

    def process(self, msg):

        enc = base64.b64decode(msg)

        ciphertext = enc[:len(enc)//2]
        signature = enc[len(enc)//2:]

        plaintext = self.server_private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        try:
            self.client_public_key.verify(
                signature,
                plaintext,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            print('%d : %r' % (self.id,plaintext.decode('utf-8')))
            new_msg = plaintext.upper()
            self.msg_cnt += 1

        except InvalidSignature:
            print('Invalid!')
            new_msg = (base64.b64encode(b'Deu erro ao validar'))
            self.msg_cnt += 1

        return new_msg if len(new_msg)>0 else None

# Funcionalidade Cliente/Servidor
@asyncio.coroutine
def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt +=1
    addr = writer.get_extra_info('peername')

    with open("server_private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    with open("client_public.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    srvwrk = ServerWorker(conn_cnt,private_key,public_key,addr)
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
