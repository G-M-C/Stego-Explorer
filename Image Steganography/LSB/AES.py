import pyaes
import pbkdf2
import binascii
import os
import secrets



def encrypt():
        password = input("\nEnter the password\n")
        if len(password) == 0:
            raise ValueError('Password is required !!!')
        password_salt = os.urandom(16)
        key = pbkdf2.PBKDF2(password,password_salt).read(32)



        init_vector = secrets.randbits(256)
        message = input("\nEnter message to be stego'd\n")
        if len(message) == 0:
            raise ValueError('Message cannot be empty !!!')
        aes = pyaes.AESModeOfOperationCTR(key , pyaes.Counter(init_vector))
        cipher = aes.encrypt(message)
        cipher=binascii.hexlify(cipher)
        key=binascii.hexlify(key)


        f = open("key_file","wb")
        f.write(key)
        f.close()

        f = open("init_vector_file","w")
        f.write(str(init_vector))
        f.close()

        return cipher



def decrypt(cipher,key,init_vector):

        key=binascii.unhexlify(key)
        cipher=binascii.unhexlify(cipher)
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(init_vector))
        decrypted_message = aes.decrypt(cipher)
        decrypted_message = decrypted_message.decode('utf-8')
        print('Decrypted Message : ' , decrypted_message)





























