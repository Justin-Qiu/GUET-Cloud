#coding: utf-8  

import soaplib  
from soaplib.core.service import rpc, DefinitionBase, soap  
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi  
from soaplib.core.model.clazz import Array

from functions import user_reg
from functions import user_log
from functions import file_read
from functions import file_write
from functions import file_del

from auth.rsa.rsa import rsa_reg
from auth.rsa.rsa import rsa_auth
from auth.elgamal.elgamal import elgamal_reg
from auth.elgamal.elgamal import elgamal_auth
from auth.dsa.dsa import dsa_reg
from auth.dsa.dsa import dsa_auth

class WebService(DefinitionBase): 
    @soap(String, String, String, String, String, String, _returns = Integer)  
    def reg(self, usr, pwd, name, sex_zh, unit, title):
        info = user_reg(usr, pwd, name, sex_zh, unit, title)
        return info
 
    @soap(String, String, _returns = String)  
    def login(self, usr, pwd):
        info = user_log(usr, pwd)[0]
        return info
        
    @soap(String, String, _returns = Array(String))  
    def user(self, usr, pwd):
        info = user_log(usr, pwd)[1:6]
        return info
        
    @soap(String, String, _returns = Array(Array(String)))  
    def files(self, usr, pwd):
        info = user_log(usr, pwd)[6]
        return info

    @soap(String, String, _returns = Array(String))  
    def read(self, usr, file_name):
        info = file_read(usr, file_name)
        return info
        
    @soap(String, String, String, _returns = Integer)  
    def edit(self, usr, file_name, txt):
        info = file_write(usr, file_name, txt)
        return info
    
    @soap(String, String, _returns = Integer)  
    def delete(self, usr, file_name):
        info = file_del(usr, file_name)
        return info
        
    @soap(String, String, String, String, String, _returns = Array(String))  
    def reg_rsa(self, usr, name, sex_zh, unit, title):
        info = rsa_reg(usr, name, sex_zh, unit, title)
        return info
    
    @soap(String, String, _returns = Integer)  
    def auth_rsa(self, usr, sig):
        info = rsa_auth(usr, sig)
        return info
    
    @soap(String, String, String, String, String, _returns = Array(Integer))  
    def reg_elgamal(self, usr, name, sex_zh, unit, title):
        info = elgamal_reg(usr, name, sex_zh, unit, title)
        return info
    
    @soap(String, String, String, _returns = Integer)  
    def auth_elgamal(self, usr, sig1, sig2):
        info = elgamal_auth(usr, sig1, sig2)
        return info
        
    @soap(String, String, String, String, String, _returns = Array(Integer))  
    def reg_dsa(self, usr, name, sex_zh, unit, title):
        info = dsa_reg(usr, name, sex_zh, unit, title)
        return info
    
    @soap(String, String, String, _returns = Integer)  
    def auth_dsa(self, usr, sig1, sig2):
        info = dsa_auth(usr, sig1, sig2)
        return info
          
if __name__=='__main__':  
    try:  
        from wsgiref.simple_server import make_server  
        soap_application = soaplib.core.Application([WebService], 'tns')  
        wsgi_application = wsgi.Application(soap_application)  
        server = make_server('10.170.52.239', 7789, wsgi_application)  
        print 'soap server starting......'  
        server.serve_forever()  
    except ImportError:  
        print "Error: example server code requires Python >= 2.5"  
