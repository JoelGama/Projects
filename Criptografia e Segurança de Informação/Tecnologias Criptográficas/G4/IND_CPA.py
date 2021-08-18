import os
import sys
import base64
import random
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.algorithms import ChaCha20
from cryptography.hazmat.backends import default_backend

class Adversario_Deterministico:
    def __init__(self, nome, estado):
        self.nome   = nome
        self.estado = estado

    def choose(self, enc_oracle):
        return (b"00000000", b"1111111")

    def guess(self, enc_oracle, c):
        c2 = enc_oracle(b"00000000")
        return c != c2

class Cypher_det:
    # Cifra deterministica baseada no ChaCha20
    def keygen(self):
        return os.urandom(32)

    def enc(self, key, ptxt):
        
        nonce = '0000000000000000'
        algorithm = ChaCha20(key,bytes(nonce,'utf8'))
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        encryptor  = cipher.encryptor()
        ciphertext = encryptor.update(ptxt)

        return ciphertext

class Jogo: 

    def ind_CPA(self,C,A):
        k = C.keygen()
        enc_oracle = lambda ptxt: C.enc(k,ptxt)
        m = [0,1]
        m[0], m[1] = A.choose(enc_oracle)
        list = [0,1]
        print(m)
        b = random.choice(list)
        c = C.enc(k,m[b])
        b2 = A.guess(enc_oracle, c)
        return b2

def main():
    C = Cypher_det()
    A = Adversario_Deterministico("Mario","0")
    J = Jogo()
    result = J.ind_CPA(C,A)
    return result

if __name__ == "__main__":
    main()