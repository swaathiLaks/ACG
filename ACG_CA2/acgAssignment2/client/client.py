'''
Client Program

StudentID: P2227171
Name: Swaathi Lakshmanan
Class: DISM/FT/1B/05
Assessment: Assignment 2

Script name:
client.py

Purpose: 
Contains code for client to connect to server.

Usage Syntax:
Run with command line: python .\client.py

Input/output files:
d:/assignment2/day_end.csv
d:/assignment2/keys.db
d:/assignment2/menu.csv

Input files:
d:/assignment2/sreceiver.pem

Python version:
Python 3

Reference:
None

Library/Module:
Install pysqlitecipher module: pip install pysqlitecipher==0.11

Known issues:
None
'''
#!/usr/bin/env python3
# Please starts the tcp server first before running this client


# Imports
import sys
import socket
import commonfn
from pysqlitecipher import sqlitewrapper
global host, port

# Intial verfication code
try:
    upassword=input("Enter Password for database: ")
    obj = sqlitewrapper.SqliteCipher(dataBasePath="keys.db" , checkSameThread=False , password=upassword)
except:
    print("Password is wrong.")
    exit()
keys = (obj.getDataFromTable("mykeys" , raiseConversionError = True , omitID = False))
privkey=keys[1][0][2]

# Code to view/ edit data
askuser=input("Would you like to edit or view files (enter (y) if you want to): ").lower()
if askuser=="y":
    commonfn.viewfromdatabase(keys[1])

# decrypting day_end.csv
commonfn.storprivkey(keys[1][1][2],'day_end.csv',False)

host = socket.gethostname()
port = 8888 
cmd_GET_MENU = b"GET_MENU"
cmd_END_DAY = b"CLOSING"
menu_file = "menu.csv"
return_file = "day_end.csv"

# Connect to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((host, port))
    my_socket.sendall(cmd_GET_MENU )
    endata = my_socket.recv(4096)

# INTEGRITY, NON REPUDIATION AND DECRYPTING

    # splitting data
    newList=(endata).split(b'\n\n\nSIGN')

    # decrytion session key
    reseskey=commonfn.decrypting(newList[3],privkey)

    # decrypting data
    data=commonfn.deWithSesKey(reseskey,newList[1],newList[2],newList[4])

    # verifying signature
    ishash=commonfn.designature(data,'sreceiver.pem',newList[0])
    if ishash:
        print('Integrity and Non-repudiation checked.')
        val='y'
    else:
        print('Either integrity or non-repudiation is corrupted. Would you like to continue writing to the file?')
        val=input("Enter 'y' to continue writing to the the file: ").lower()

# INTEGRITY, NON REPUDIATION AND DECRYPTING 

# ENCRYPTING DATA AT REST

    if val=='y':
        obj.deleteDataInTable("mykeys" , 2 , commit = True , raiseError = True , updateId = True)

        # generating new fernet key
        newkey=commonfn.ferkey()

        # adding key to database
        obj.insertIntoTable("mykeys" , [menu_file,newkey] , commit = True)

        # encrypting plaintext data with new key
        endata=commonfn.enrest(newkey,data)

# ENCRYPTING DATA AT REST

        menu_file = open(menu_file,"wb")
        menu_file.write(endata)
        menu_file.close()
    my_socket.close()
print('Menu today received from server')
# print('Received', repr(endata))  # for debugging use
my_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((host, port))
    my_socket.sendall(cmd_END_DAY)
    try:
        out_file = open(return_file,"rb")
    except:
        print("file not found : " + return_file)
        sys.exit(0)
    file_bytes = out_file.read(1024)
    sent_bytes=b''
    while file_bytes != b'':

# ENCRYPTION SCHEME

        # generating new session key
        seskey=commonfn.genseskey()

        # encryptinng data with session key
        ciphTxt,tag,nonce=commonfn.enWithSesKey(seskey,file_bytes)

        # creating digital signature
        signature=commonfn.ensignature(file_bytes,privkey)  
        
        # encrypting session key  
        enSesKey=commonfn.encrypting(seskey,'sreceiver.pem')

        # concatenating all data
        file_bytes=(signature+b'\n\n\nSIGN'+ciphTxt+b'\n\n\nSIGN'+tag+b'\n\n\nSIGN'+enSesKey+b'\n\n\nSIGN'+nonce)

# ENCRYPTION SCHEME

        my_socket.send(file_bytes)
        sent_bytes+=file_bytes
        file_bytes = out_file.read(1024) # read next block from file
    out_file.close()
    my_socket.close()
print('Sale of the day sent to server')

# encrypting day_end.csv
commonfn.storprivkey(keys[1][1][2],'day_end.csv')

#print('Sent', repr(sent_bytes))
my_socket.close()
