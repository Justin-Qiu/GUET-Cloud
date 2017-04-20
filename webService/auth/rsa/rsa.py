#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import os.path

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

'''
RSA Registration

Input
    User ID, 
    Name,
    Gender in Chinese,
    Unit name in Chinese,
    Position title
Return
    Registration successful: '1', Public key, Private key
    User ID already exists: '2', Empty string, Empty string
'''
def rsa_reg(usr, name, sex_zh, unit, title):
    
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
    sql_search = "SELECT * FROM users WHERE loginid = '%s'" % usr
    
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
        
        '''
        sk_list = []
        for i in range(len(sk)/256):
            sk_list.append(sk[i*256 : i*256 + 256])
        sk_list.append(sk[(len(sk)/256)*256:])
        '''
        
        # Save user's public key
        pkey = key.publickey()
        pk = pkey.exportKey('PEM')
        f = open('auth/rsa/keys/%s.pub' % usr,'w')
        #f = open('keys/%s.pub' % usr,'w')
        f.write(pk)
        f.close()  
        
        '''
        # Encrypt private key with initial public key
        pk_usr = RSA.importKey(pk_init)
        
        sk_enc = '' 
        for i in range(len(sk_list)):
            sk_enc = sk_enc + pk_usr.encrypt(sk_list[i], '')[0]
        '''
           
        '''
        sk_enc = []
        for i in range(len(sk_list)):
            sk_enc.append(pk_usr.encrypt(sk_list[i], '')[0])
        '''
        
        return '1', pk, sk
    
    # Registeration failed
    else:
        return '2', '', ''

'''
RSA Authentication

Input
    User ID, 
    Signature
Return
    Authentication successful: 1
    Authentication failed: 2
    Wrong user ID: 3
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
    sql_search = "SELECT * FROM users WHERE loginid = '%s'" % usr
    
    if cur.execute(sql_search) == 1L and os.path.exists('auth/rsa/keys/%s.pub' % usr):
    
        # Signature authentication
        f = open('auth/rsa/keys/%s.pub' % usr,'r')
        #f = open('keys/%s.pub' % usr,'r')
        pk = RSA.importKey(f.read())
        f.close()
        
        h = SHA.new(usr)
        verifier = PKCS1_v1_5.new(pk)
        if verifier.verify(h, sig.decode('hex')):
            return 1
        else:
            return 2
        '''
        if pk.verify(usr, (long(sig),)) == True:
            return 1
        elif pk.verify(usr, (long(sig),)) == False:
            return 2
        '''
    else:
        return 3
    
    conn.close()
