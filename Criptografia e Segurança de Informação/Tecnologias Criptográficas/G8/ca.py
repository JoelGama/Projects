import sys
from OpenSSL import crypto
from OpenSSL.crypto import PKCS12

def cliente(path):
    client = crypto.load_pkcs12(open(path + "/Cliente1  .p12", 'rb').read(), '1234')
    client.get_certificate()
    client.get_privatekey()
    client.get_ca_certificates()
    return client

def servidor(path):
    server = crypto.load_pkcs12(open(path + "/Servidor.p12", 'rb').read(), '1234')
    server.get_certificate()
    server.get_privatekey()
    server.get_ca_certificates()
    return server

def ca(path):

def main():
    path = sys.argv[1]
    
    client = cliente(path)
    
    server = servidor(path)


if __name__ == "__main__":
    main()