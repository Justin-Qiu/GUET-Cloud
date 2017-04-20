#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import os.path

from Crypto.Random import random
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA

'''
DSA Registration

Input
    User ID, 
    Name,
    Gender in Chinese,
    Unit name in Chinese,
    Position title
Return
    Registration successful: 1, y, g, p, q, x
    User ID already exists: 2, 0, 0, 0, 0, 0
'''
def dsa_reg(usr, name, sex_zh, unit, title):
    
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
        key = DSA.generate(1024)

        # Key data
        y = key.y
        g = key.g
        p = key.p
        q = key.q
        x = key.x

        
        # Save user's public key
        f = open('auth/dsa/keys/%s.pub' % usr,'w')
        f.write(str(y) + ' ' + str(g) + ' ' + str(p) + ' ' + str(q))
        f.close()  
        
        return 1, y, g, p, q, x
    
    # Registeration failed
    else:
        return 2, 0, 0, 0, 0, 0

'''
DSA Authentication

Input
    User ID, 
    Signature 1,
    Signature 2
Return
    Authentication successful: 1
    Authentication failed: 2
    Wrong user ID: 3
'''
def dsa_auth(usr, sig1, sig2):

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
    
    if cur.execute(sql_search) == 1L and os.path.exists('auth/dsa/keys/%s.pub' % usr):
    
        # Signature authentication
        f = open('auth/dsa/keys/%s.pub' % usr,'r')
        pk = f.read() 
        f.close()
        
        y = long(pk.split(' ')[0])
        g = long(pk.split(' ')[1])
        p = long(pk.split(' ')[2])
        q = long(pk.split(' ')[3])
        
        t = (y, g, p, q)
        key = DSA.construct(t)
        
        h = SHA.new(usr).digest()
        
        sig = (long(sig1), long(sig2))
        
        if key.verify(h,sig):
            return 1
        else:
            return 2
    else:
        return 3
    
    conn.close()
