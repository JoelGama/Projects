import os
import asyncio
import socket
import base64
import sys
import OpenSSL
from OpenSSL import crypto
from OpenSSL.crypto import PKCS12
from OpenSSL.crypto import FILETYPE_ASN1
from cryptography.x509 import Certificate
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.padding import PSS
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key

conn_cnt = 0
conn_port = 8888
max_msg_size = 9999

class ServerWorker(object):

    def __init__(self, cnt, private_key, public_key, server_cert, ca, addr=None):
        self.id = cnt
        self.msg_cnt = 0
        self.addr = addr
        self.server_private_key = private_key
        self.server_public_key = public_key
        self.server_cert = server_cert
        self.ca_cert = ca
        self.client_public_key = None

    def process(self, msg):

        if (self.msg_cnt == 0):

            cert = load_pem_x509_certificate(msg, default_backend())
            client_cert = OpenSSL.crypto.X509.from_cryptography(cert)

            try:
                store = crypto.X509Store()
                store.add_cert(self.ca_cert)

                store_ctx = crypto.X509StoreContext(store, client_cert)
                store_ctx.verify_certificate()

                pk = client_cert.get_pubkey()
                self.client_public_key = pk.to_cryptography_key()

                new_msg = self.server_cert.to_cryptography().public_bytes(Encoding.PEM)
                self.msg_cnt += 1

                return new_msg

            except Exception as e:
                print(e)
                sys.exit(1)

        else:

            enc = base64.b64decode(msg)
            end_string = b'\n-----END CERTIFICATE-----\n'

            signature = enc[:256]
            certificate = enc[256:]

            c = certificate.split(end_string)[0]
            mensagem = certificate.split(end_string)[1]
            certificado = (c + end_string)

            cert = load_pem_x509_certificate(certificado, default_backend())
            client_cert = OpenSSL.crypto.X509.from_cryptography(cert)

            try:
                store = crypto.X509Store()
                store.add_cert(self.ca_cert)

                store_ctx = crypto.X509StoreContext(store, client_cert)
                store_ctx.verify_certificate()

                pk = client_cert.get_pubkey()
                self.client_public_key = pk.to_cryptography_key()

                chosen_hash = hashes.SHA256()
                hasher = hashes.Hash(chosen_hash, default_backend())

                cpk = self.client_public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                spk = self.server_public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

                hasher.update(cpk)
                hasher.update(spk)
                digest = hasher.finalize()

                try:
                    self.client_public_key.verify(
                        signature,
                        digest,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        utils.Prehashed(chosen_hash)
                    )

                    print('%d : %r' % (self.id,mensagem.decode('utf-8')))
                    new_msg = mensagem.upper() + self.server_cert.to_cryptography().public_bytes(Encoding.PEM)
                    self.msg_cnt += 1

                except:
                    print('Invalid!')
                    new_msg = (base64.b64encode(b'Deu erro ao validar'))
                    self.msg_cnt += 1

            except Exception as e:
                print(e)
                sys.exit(1)

        return new_msg if len(new_msg)>0 else None

# Funcionalidade Cliente/Servidor
@asyncio.coroutine
def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt +=1
    addr = writer.get_extra_info('peername')

    server = crypto.load_pkcs12(open("Servidor.p12", "rb").read(), '1234')

    with open("CA.cer", "rb") as file:
        cer = file.read()
    
    ca = OpenSSL.crypto.load_certificate(FILETYPE_ASN1,cer)
    server_cert = server.get_certificate()

    try:
        store = crypto.X509Store()
        store.add_cert(ca)

        store_ctx = crypto.X509StoreContext(store, server_cert)

        store_ctx.verify_certificate()

        sk = server.get_privatekey()
        pk = server_cert.get_pubkey()

        private_key = sk.to_cryptography_key()
        public_key = pk.to_cryptography_key()

        srvwrk = ServerWorker(conn_cnt,private_key,public_key,server_cert,ca,addr)
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

    except Exception as e:
        print(e)
        return False

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
