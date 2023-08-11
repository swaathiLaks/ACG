'''
Common functions Program

StudentID: P2227171
Name: Swaathi Lakshmanan
Class: DISM/FT/1B/05
Assessment: Assignment 2

Script name:
commonfn.py

Purpose: 
Contains all the functions used across the whole program.

Usage Syntax:
Run with command line: python .\client.py

Input files:
None

Output files:
None

Python version:
Python 3

Reference:
https://www.geeksforgeeks.org/python-convert-string-to-binary/
https://pycryptodome.readthedocs.io/en/latest/src/examples.html#generate-public-key-and-private-key
https://cryptography.io/en/latest/fernet/
https://medium.com/@harshnative/encrypting-sqlite-database-in-python-using-pysqlitecipher-module-23b80129fda0

Library/Module:
Install pycryptodome module: pip install pycryptodome

Known issues:
None
'''

# imports
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto import Random
from cryptography.fernet import Fernet
from pysqlitecipher import sqlitewrapper

# FUNCTIONS FOR DATA IN TRANSIT

# function to generate session key
def genseskey():
    return get_random_bytes(16)

# function to encrypt data with session key
def enWithSesKey(seskey,msg):
    ciphAes = AES.new(seskey, AES.MODE_EAX)
    data=msg
    ciphTxt, tag = ciphAes.encrypt_and_digest(data)
    return ciphTxt, tag, ciphAes.nonce

# function to encrypt a text with key
def encrypting(str1,pkeyf):
    key1=RSA.import_key(open(pkeyf).read())
    ciphRsa = PKCS1_OAEP.new(key1)
    encStr1 = ciphRsa.encrypt(str1)
    return encStr1

# function to decrypt text with a key
def decrypting(enstr,pkeyf):
    key1=RSA.import_key(pkeyf)
    ciphRsa = PKCS1_OAEP.new(key1)
    str1= ciphRsa.decrypt(enstr)
    return str1

# function to decrypt message with sesssion key
def deWithSesKey(seskey,enmsg,tag,nonce):
    ciphAes = AES.new(seskey, AES.MODE_EAX, nonce)
    data = ciphAes.decrypt_and_verify(enmsg,tag)
    return data

# function to create signature
def ensignature(msg,pkeyf):
    key = RSA.import_key(pkeyf)
    h = SHA256.new(msg)
    signature = PKCS1_PSS.new(key).sign(h)
    return signature

# function to decrypt and verify signature
def designature(msg,pkeyf,signature):
    key = RSA.import_key(open(pkeyf).read())
    h = SHA256.new(msg)
    try:
        PKCS1_PSS.new(key).verify(h, signature)
        return True
    except:
        return False

# FUNCTIONS FOR DATA AT REST

# function to read a file and return the data
def readfile(file):
    file = open(file,"rb")
    data = file.read()
    file.close()
    return data

# function to write to a file
def writefile(file,data):
    file = open(file,"wb")
    file.write(data)
    file.close()

# function to write fernet key
def ferkey():
    key = Fernet.generate_key()
    return key
# function to encrypt data at rest
def enrest(key,data):
    f = Fernet(key)
    token = f.encrypt(data)
    return token

# function to decrypt data at rest
def derest(key,file_name):
    token = readfile(file_name)
    f = Fernet(key)
    data = f.decrypt(token)
    return data

# function to use for storing private key
def storprivkey(key,file, store=True):
    if store:
        privkey=readfile(file)
        enkey=enrest(key,privkey)
    else:
        enkey=derest(key,file)
    writefile(file,enkey)

# DATABASE FUNCTIONS

# function to retrieve key from database based on viewer wants to view/ edit
def viewfromdatabase(keys):
    userinput=input("Please enter the file you would like to view or edit: ")
    y=True
    for i in keys:
        if i[1]==userinput:
            y=False
            x=True
            while x:
                x=False
                useropt=input("Would you like to\n1) view\n2) edit\n>> ")
                if useropt=="1":
                    printing=derest(i[2],i[1])
                    print(f"Here's data from {i[1]}: {printing}\n")
                elif useropt=="2":
                    userrewrite=input("Please enter your new data: ")
                    writefile(i[1],bytes(userrewrite,'utf-8'))
                    storprivkey(i[2],i[1])
                else:
                    print("Please enter a valid input")
                    x=True
    else:
        if y:
            print('File name does not exist.')
