import os
import sys
import random
import OpenSSL
from random import randrange
from OpenSSL import crypto
from OpenSSL.crypto import FILETYPE_ASN1
from cryptography.x509 import Certificate
from cryptography.x509 import load_pem_x509_certificate

def genCA():
    ca_key = crypto.PKey()
    ca_key.generate_key(crypto.TYPE_RSA, 2048)

    ca_cert = crypto.X509()
    ca_cert.set_version(3)
    ca_cert.set_serial_number(random.randint(50000000,100000000))

    ca_subj = ca_cert.get_subject()
    ca_subj.commonName = "My CA"

    ca_cert.add_extensions([
        crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always', issuer=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'),
        crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign'),
    ])

    ca_cert.set_issuer(ca_subj)
    ca_cert.set_pubkey(ca_key)

    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(10*365*24*60*60) # 10 anos

    ca_cert.sign(ca_key, 'sha256')

    pfx = crypto.PKCS12()
    pfx.set_privatekey(ca_key)
    pfx.set_certificate(ca_cert)
    pfxdata = pfx.export(b'1234')
    
    with open('CA.pfx', 'wb') as pfxfile:
        pfxfile.write(pfxdata)

# Client Certificate
def genClientCertificate():

    ca = crypto.load_pkcs12(open('CA.pfx', "rb").read(),b'1234')
    ca_cert = ca.get_certificate()
    ca_subj = ca_cert.get_subject()
    sk = ca.get_privatekey()

    client_key = crypto.PKey()
    client_key.generate_key(crypto.TYPE_RSA, 2048)

    client_cert = crypto.X509()
    client_cert.set_version(3)
    client_cert.set_serial_number(random.randint(50000000,100000000))

    rando = str(randrange(100000))
    client_subj = client_cert.get_subject()
    client_subj.commonName = rando

    client_cert.add_extensions([
        crypto.X509Extension(b'basicConstraints', False, b'CA:FALSE'),
        crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=client_cert),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always', issuer=ca_cert),
        crypto.X509Extension(b'extendedKeyUsage', False, b'clientAuth'),
        crypto.X509Extension(b'keyUsage', False, b'digitalSignature'),
    ])

    client_cert.set_issuer(ca_subj)
    client_cert.set_pubkey(client_key)

    client_cert.gmtime_adj_notBefore(0)
    client_cert.gmtime_adj_notAfter(365*24*60*60) # 1 ano

    client_cert.sign(sk,'sha256')

    pfx = crypto.PKCS12()
    pfx.set_privatekey(client_key)
    pfx.set_certificate(client_cert)
    pfxdata = pfx.export(b'1234')
    
    filename = rando+'.pfx'

    with open(filename, 'wb') as pfxfile:
        pfxfile.write(pfxdata)

    return filename

def main():
    genCA()

if __name__ == "__main__":
    main()