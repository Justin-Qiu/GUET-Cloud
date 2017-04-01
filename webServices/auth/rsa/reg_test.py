#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA

from rsa import rsa_reg, rsa_auth

# User's information
usr = raw_input('请输入用户名:')
name = u'邱震尧'
sex_zh = u'男'
unit = u'西安电子科技大学'
title = u'学生'

'''
Server's operation
'''
# Key initialization
key_init = RSA.generate(2048)
pk_tmp = key_init.publickey()
pk_init = pk_tmp.exportKey('PEM') # Sent to server
sk_init = key_init.exportKey('PEM') # Saved by user

reg_result = rsa_reg(usr, name, sex_zh, unit, title, pk_init)

if reg_result[0] == '1':
    pk = reg_result[1]
    sk_enc = reg_result[2]
    skey = RSA.importKey(sk_init)
    
    sk_list = []
    for i in range(len(sk_enc)/256):
        sk_list.append(sk_enc[i*256 : i*256 + 256])
    sk_list.append(sk_enc[(len(sk_enc)/256)*256:])
    
    sk = ''
    for i in range(len(sk_list)):
        sk = sk + skey.decrypt(sk_list[i])
    
    #sk = skey.decrypt(sk_enc) # Decrypt private key
    
    print '注册成功！'
elif reg_result[0] == '2':
    print '用户名已存在！'

'''
User's operation
'''
# User saves private key
f = open('keys/%s_user.pem' % usr,'w')
f.write(sk)
f.close() 
