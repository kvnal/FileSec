# main

import ntpath
import encrypt_decrypt as ed
import time
import argparse
import getpass
import os
import base64

parser = argparse.ArgumentParser()

def getQA():
    return [str(input("security Question : ")),str(input("Answer : "))]

def getDevicePass(path):
    os.chdir(path+'\.fileSec')
    key = open('pass.txt','rb').read()
    key = base64.b64decode(key).decode()
    return key

if __name__ == "__main__":
    parser.add_argument("path",type=str)    
    parser.add_argument("-e","--encrypt",action="store_true")
    parser.add_argument("-d","--decrypt",action="store_true")
    parser.add_argument("-r","--device",type=str)
    parser.add_argument("-f","--forgot",action="store_true")
    
    args = parser.parse_args()
    print(args.device)
    if (ntpath.isfile(args.path)):
        # encrypt
        if(args.encrypt):
            print("use '-reverseTime-' if you want password to be in mm:hh format (24 hr fomat)")
            password = getpass.getpass("Password : ")
            if (password == getpass.getpass("confirm Password : ")):
                q,a = getQA()
                edObj = ed.main(args.path,password).encrypt(q,a)

                if(args.device):
                    os.chdir(args.device)
                    os.mkdir(".fileSec")
                    os.chdir('\.fileSec')
                    with open("pass.txt",'wb') as file:
                        file.write(base64.b64encode(password.encode()))
                        file.close()

            else:
                print("Confirm Password does'nt matched.\nTry again")
        

        elif(args.decrypt and args.path[-4:]=='.lck' ):
            print("decrypt")
            if(not args.forgot):
                
                password = getpass.getpass("Password : ") if not args.device else getDevicePass(args.device)
                edObj = ed.main(args.path,password).decrypt()
            else:
                edObj = ed.main(args.path,"").forgotPass()
                print(edObj)
        else:
            print("file should have .lck extension to decrypt")
    else:
        print("invalid file path")