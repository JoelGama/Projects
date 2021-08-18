import os
import asyncio
import socket
import base64
import sys
import OpenSSL
from OpenSSL import crypto
from OpenSSL.crypto import PKCS12
from OpenSSL.crypto import FILETYPE_ASN1
from OpenSSL.crypto import X509
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

conn_port = 8888
max_msg_size = 9999

class Client:

    def __init__(self, private_key, public_key, client_cert, ca, sckt=None):
        self.sckt = sckt
        self.msg_cnt = 0
        self.client_private_key = private_key
        self.client_public_key = public_key
        self.client_cert = client_cert
        self.ca_cert = ca
        self.server_public_key = None

    def process(self, msg=b""):

        if (self.msg_cnt == 0):

            new_msg = self.client_cert.to_cryptography().public_bytes(Encoding.PEM)
            self.msg_cnt += 1

            return new_msg
        else:

            if (self.msg_cnt == 1):

                cert = load_pem_x509_certificate(msg, default_backend())
                server_cert = OpenSSL.crypto.X509.from_cryptography(cert)
                mensagem = 'Recebi tudo bem'

            else:

                begin_string = b'-----BEGIN CERTIFICATE-----\n'

                c = msg.split(begin_string)[1]
                mensagem = msg.split(begin_string)[0]
                certificado = (begin_string + c)

                cert = load_pem_x509_certificate(certificado, default_backend())
                server_cert = OpenSSL.crypto.X509.from_cryptography(cert)

            try:
                store = crypto.X509Store()
                store.add_cert(self.ca_cert)

                store_ctx = crypto.X509StoreContext(store, server_cert)
                store_ctx.verify_certificate()

                pk = server_cert.get_pubkey()
                self.server_public_key = pk.to_cryptography_key()

            except Exception as e:
                print(e)
                sys.exit(1)

            print('Input message to send (empty to finish)')
            print(mensagem)

            data = input()
            mensagem = data.encode('utf-8')

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

            signature = self.client_private_key.sign(
                digest,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                utils.Prehashed(chosen_hash)
            )

            cert = self.client_cert.to_cryptography().public_bytes(Encoding.PEM)
            new_msg = (base64.b64encode(signature+cert+mensagem))
            self.msg_cnt += 1

            return new_msg if len(new_msg)>0 else None

# Funcionalidade Cliente/Servidor
@asyncio.coroutine
def tcp_echo_client(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    reader, writer = yield from asyncio.open_connection('127.0.0.1',
                                                        conn_port, loop=loop)
    addr = writer.get_extra_info('peername')

    cliente = crypto.load_pkcs12(open("Cliente1.p12", "rb").read(), '1234')

    with open("CA.cer", "rb") as file:
        cer = file.read()
    
    ca = OpenSSL.crypto.load_certificate(FILETYPE_ASN1,cer)
    client_cert = cliente.get_certificate()

    try:
        store = crypto.X509Store()
        store.add_cert(ca)

        store_ctx = crypto.X509StoreContext(store, client_cert)

        store_ctx.verify_certificate()

        sk = cliente.get_privatekey()
        pk = client_cert.get_pubkey() 

        private_key = sk.to_cryptography_key()
        public_key = pk.to_cryptography_key()

        client = Client(private_key,public_key,client_cert,ca,addr)
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

    except Exception as e:
        print(e)
        return False

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())

run_client()