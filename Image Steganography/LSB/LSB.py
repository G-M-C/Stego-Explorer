import cv2
import numpy as np
from AES import encrypt
from AES import decrypt
from PIL import Image



def aes_handshaker(mode,msg=" "):
    if mode == 1 :
        cipher = encrypt()
        cipher = cipher.decode("utf-8")
        return cipher

    elif mode == 2:

        msg = bytes(msg,'utf-8')

        f = open('key_file','rb')
        key = f.read()
        f.close()

        f = open('init_vector_file','r')
        init_vector = f.read()
        f.close()

        init_vector = int(init_vector)

        decrypt(msg,key,init_vector)






def msg2binary(data):
    if type(data) == str:
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [ format(i, "08b") for i in data ]
    elif type(data) == int or type(data) == np.uint8:
        return format(data, "08b")
    else:
        raise TypeError("The data you've entered if of an unsupported format")

def encode(img_name,msg):

    img = cv2.imread(img_name)
    available_bytes = img.shape[0] * img.shape[1] * 3//8
    print("\nNumber of bytes available for encoding : ",available_bytes)

    msg = msg + "$$$$$"
    msg_index = 0
    bin_msg = msg2binary(msg)
    msg_len = len(bin_msg)

    for row in img:
        for pixel in row:

            r,g,b = msg2binary(pixel)

            if msg_index < msg_len:
                pixel[0] = int(r[:-1] + bin_msg[msg_index], 2)
                msg_index += 1

            if msg_index < msg_len:
                pixel[1] = int(g[:-1] + bin_msg[msg_index], 2)
                msg_index += 1

            if msg_index < msg_len:
                pixel[2] = int(b[:-1] + bin_msg[msg_index], 2)
                msg_index += 1

            if msg_index >= msg_len:
                break

    return img

def decode(img_name):
    img = cv2.imread(img_name)
    bin_data = ""

    for row in img:
        for pixel in row:

            r,g,b = msg2binary(pixel)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    all_bytes = [bin_data[i : i+8] for i in range(0,len(bin_data),8)]

    decoded_data= ""

    for byte in all_bytes:
        decoded_data += chr(int(byte,2))

        if decoded_data[-5:] == "$$$$$":
            break

    return decoded_data[:-5]



def stego():
    ch = int(input("\n1.Encode\n2.Decode\nYour choice ?"))

    if ch == 1:
        cipher = aes_handshaker(1)
        print(cipher)
        print("\nEnter the image name along with extension to be used for encoding")
        img_name = input()
        temp = encode(img_name,cipher)
        cv2.imwrite('encoded.png',temp)
        print("!!! ALERT !!!")
        print("Encoding Completed")
        print("Please forward the following files to the intended recipient")
        print("\n1.encoded.png\n2.key_file\n3.init_vector_file")


    if ch == 2:
        print("\nEnter the image name along with extension for decoding")
        img_name = input()
        msg = decode(img_name)
        aes_handshaker(2,msg)


stego()





























































