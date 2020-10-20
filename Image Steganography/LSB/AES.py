import pyaes
import pbkdf2
import binascii
import os
import secrets



def encrypt():
        password = input("\nEnter the password\n")
        password_salt = os.urandom(16)
        key = pbkdf2.PBKDF2(password,password_salt).read(32)



        init_vector = secrets.randbits(256)
        message = input("\nEnter message to be stego'd\n")
        aes = pyaes.AESModeOfOperationCTR(key , pyaes.Counter(init_vector))
        cipher = aes.encrypt(message)
        cipher=binascii.hexlify(cipher)
        key=binascii.hexlify(key)
        l = [cipher,key,init_vector]
        return l



def decrypt(cipher,key,init_vector):

        key=binascii.unhexlify(key)
        cipher=binascii.unhexlify(cipher)
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(init_vector))
        decrypted_message = aes.decrypt(cipher)
        print('Decrypted Message : ' , decrypted_message)


























