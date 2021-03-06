
import os
from Crypto.Cipher import AES
import ntpath
import header_get
import base64
import re
import time
import getpass

class main:
    def __init__(self,path,KEY):
#         self.path = path
        self.KEY=KEY
        self.__filename=ntpath.basename(path)
        self.__extension=self.__filename[-4:]
        self.path= path[:len(self.__filename)] if path != self.__filename else False
        os.chdir(rf"{self.path}") if self.path else None
        
    def key16(self,key):
        return  key.encode()+ (AES.block_size - len(key))*b'*' 
    
    def setExtension(self,exe):
        return f'&*{exe}*&'
    
    def setQA(self,Q,A):
        return f'$%{Q}^%{A}%$'
    
    def setKey(self):
        return f'#@{self.KEY}@#'
    
    def setBase64(self,data):
        return base64.b64encode(data)
    
    def getExtension(self,data):
        return header_get.EX(data)
    
    def getQA(self,data):
        return header_get.QA(data) # [Q,A]
    
    def getKey(self,data):
        return header_get.KEY(data)
    
    def getBase64(self,data):
        return base64.b64decode(data)
    
    def checkTime(self,header):
        if(self.getKey(header)=="-reverseTime-"):
            if(self.KEY== header_get.TIME(time.ctime())):
                return "-reverseTime-"
        return self.KEY
    
    def forgotPass(self):
        
        file = open(self.__filename[:-4]+'.lck','rb').read()
        file = self.getBase64(file)
        file = file.split(b'%^$%^$')
        header = file[0].decode()

        q,a = self.getQA(header)
        if (input(f'Security question : \n{q}\n') == a):
            newPassword = getpass.getpass("New Password : ")
            if (getpass.getpass("Confirm New Password : ")==newPassword):
                self.KEY = self.getKey(header)
                self.decrypt()
                self.__filename = self.getExtension(header)
                self.KEY = newPassword
                self.encrypt(q,a)


            return "Password changed Done!"
        return "Invalid Security Answer"
    
    def encrypt(self,Q,A):
        
        file = open(self.__filename,'rb').read()
        
        key = self.key16(self.KEY)
        cipher = AES.new(key,AES.MODE_EAX)
        nonce = cipher.nonce
        encrypt,tag = cipher.encrypt_and_digest(file)
        
        ## encrypt file
        with open(self.__filename[:-4]+'.lck','wb') as enc:
            header = self.setExtension(self.__filename) +self.setKey()+ self.setQA(Q,A)
            data = bytes(header,encoding='utf8')+b'\n%^$%^$'+nonce+encrypt
            
            enc.write(self.setBase64(data))
            enc.close()
        os.remove(self.__filename)
        
    
    def decrypt(self,_open=False):
        
        file = open(self.__filename[:-4]+'.lck','rb').read()
        file = self.getBase64(file)
        file = file.split(b'%^$%^$')
        data = file[1]
        
        header = file[0].decode()
        fileName = self.getExtension(header)
        self.KEY = self.checkTime(header)
        if(self.getKey(header)==self.KEY):
            key = self.key16(self.KEY)
            nonce = data[:16]
            
            cipher = AES.new(key,AES.MODE_EAX,nonce)
            decrypt = cipher.decrypt(data[16:])

            with open(fileName,'wb') as dec:
                dec.write(decrypt)
                dec.close()


            os.remove(self.__filename)
            if(_open):
                os.startfile(fileName)
            
        else:
            print('incorrect pass')
