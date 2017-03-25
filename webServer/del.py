#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions import user_log
from functions import file_read
from functions import file_write
from functions import file_del

print '--------------------------------------------------'
usr = raw_input('用户名：')
pwd = raw_input('密码：')

try1 = user_log(usr, pwd)

print '--------------------------------------------------'

if try1 == -1:
    print '密码错误！'
elif try1 == -2:
    print '用户名错误！'
else:
    print '登录成功！'
    print '--------------------------------------------------'
    for item in try1[:-1]:
        print item + ' ',
    print ''
    print '--------------------------------------------------'

if try1 != -1 and try1 != -2:
    for i in range(len(try1[-1])):
        for j in range(4):
            print try1[-1][i][j],
        print ''

print '--------------------------------------------------'

if try1 != -1 and try1 != -2:
    index = raw_input('请输入您要删除的文件序号：')
    print '--------------------------------------------------'
    file_name = '文件' + index
    try2 = file_del(usr, file_name)
    if try2 == -1:
        print '您无权删除该文件！'
    elif try2 == 1:
        print '文件删除成功！'

    print '--------------------------------------------------' 
