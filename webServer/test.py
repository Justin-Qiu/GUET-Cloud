#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import user_log
from server import file_read
from server import file_write
from server import file_del

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
    index = raw_input('请输入您要查看的文件序号：')
    print '--------------------------------------------------'
    file_name = '文件' + index
    try2 = file_read(usr, file_name)
    if try2 == -2:
        print '您无权阅读该文件！'
    elif try2[1] == -1:
        print try2[0],
        print '--------------------------------------------------'
        print '您无权修改该文件！'
    elif try2[1] == 1:
        print try2[0],
        print '--------------------------------------------------'
        print '您可以修改该文件！'
        flag = raw_input('是否修改该文件？ [y/N] ')
        if flag == 'y':
            print '--------------------------------------------------'
            print '请输入修改后的内容：'
            txt = raw_input()
            file_write(usr, file_name, txt)
            print '--------------------------------------------------'
            print '修改成功'
        else:
            pass
    print '--------------------------------------------------' 
