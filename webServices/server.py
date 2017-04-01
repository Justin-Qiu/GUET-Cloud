#coding: utf-8  

import soaplib  
from soaplib.core.service import rpc, DefinitionBase, soap  
from soaplib.core.model.primitive import String, Integer  
from soaplib.core.server import wsgi  
from soaplib.core.model.clazz import Array
  
from functions import user_log
from functions import file_read
from functions import file_write
from functions import file_del  

class WebService(DefinitionBase):  
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
  
if __name__=='__main__':  
    try:  
        from wsgiref.simple_server import make_server  
        soap_application = soaplib.core.Application([WebService], 'tns')  
        wsgi_application = wsgi.Application(soap_application)  
        server = make_server('192.168.40.129', 7789, wsgi_application)  
        print 'soap server starting......'  
        server.serve_forever()  
    except ImportError:  
        print "Error: example server code requires Python >= 2.5"  
