#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA

from rsa import rsa_reg, rsa_auth

usr = raw_input('请输入用户名:')

# Signing
f = open('keys/%s_user.pem' % usr,'r')
key = RSA.importKey(f.read())
f.close()
sig = key.sign(usr, '')

# Signature authentication
auth_result = rsa_auth(usr, sig)
if auth_result == True:
    print '认证成功！'
elif auth_result == False:
    print '认证失败！'
