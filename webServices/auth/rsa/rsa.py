#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import os.path

from Crypto.PublicKey import RSA

'''
RSA Registration

Input
    User ID, 
    Name,
    Gender in Chinese,
    Unit name in Chinese,
    Position title, 
    User's initial public key
Return
    Registration successful: '1', Unencrypted public key, Encrypted private key
    User ID already exists: '2', Empty string, Empty string
'''
def rsa_reg(usr, name, sex_zh, unit, title, pk_init):
    
    # Database connection
    conn = MySQLdb.connect(
            host='localhost',
            user='admin',
            passwd='123456',
            db='project',
            charset='utf8'
            )

    cur = conn.cursor()
    
    # Gender transfer
    if sex_zh == u'男':
        sex = 0
    elif sex_zh == u'女':
        sex = 1
    
    # Unit transfer  
    sql_unit = "SELECT * FROM unit WHERE unit_name = '%s'" % unit
    cur.execute(sql_unit)
    result_unit = cur.fetchall()
    unitid = result_unit[0][0] 
             
    # Avoid duplication
    sql_search = "SELECT * FROM users WHERE loginid = %s" % usr
    
    if cur.execute(sql_search) == 0L:
    
        # Insert into database
        sql = "insert into users(loginid, pass_word, name, sex, unitid, title) values('%s', '', '%s', '%d', '%d', '%s')" % (usr, name, sex, unitid, title) 
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        
        # Key generation
        key = RSA.generate(2048)

        # Private key
        sk = key.exportKey('PEM')
        
        sk_list = []
        for i in range(len(sk)/256):
            sk_list.append(sk[i*256 : i*256 + 256])
        sk_list.append(sk[(len(sk)/256)*256:])
        
        # Save user's public key
        pkey = key.publickey()
        pk = pkey.exportKey('PEM')
        f = open('keys/%s.pub' % usr,'w')
        f.write(pk)
        f.close()  
        
        # Encrypt private key with initial public key
        pk_usr = RSA.importKey(pk_init)
        
        sk_enc = '' 
        for i in range(len(sk_list)):
            sk_enc = sk_enc + pk_usr.encrypt(sk_list[i], '')[0]
            
        '''
        sk_enc = []
        for i in range(len(sk_list)):
            sk_enc.append(pk_usr.encrypt(sk_list[i], '')[0])
        '''
        
        return '1', pk, sk_enc
    
    # Registeration failed
    else:
        return '2', '', ''

'''
RSA Authentication

Input
    User ID, 
    Signature
Return
    Authentication successful: True
    Authentication failed: False
'''
def rsa_auth(usr, sig):

    # Database connection
    conn = MySQLdb.connect(
            host='localhost',
            user='admin',
            passwd='123456',
            db='project',
            charset='utf8'
            )

    cur = conn.cursor()
    
    # Search username in database and key files
    sql_search = "SELECT * FROM users WHERE loginid = %s" % usr
    
    if cur.execute(sql_search) == 1L and  os.path.exists('keys/%s.pub' % usr):
    
        # Signature authentication
        f = open('keys/%s.pub' % usr,'r')
        pk = RSA.importKey(f.read())
        f.close()
        if pk.verify(usr, sig) == True:
            return True
        elif pk.verify(usr, sig) == False:
            return False
    else:
        return False
    
    conn.close()
