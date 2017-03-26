#!/usr/bin/env python
# -*- coding: utf-8 -*-

from suds.client import Client 

client = Client('http://192.168.40.129:7789/?wsdl', cache=None)

print '--------------------------------------------------'
usr = raw_input('用户名：')
pwd = raw_input('密码：')

try1 = client.service.login(usr, pwd)

print '--------------------------------------------------'

if try1 == '2':
    print '密码错误！'
elif try1 == '3':
    print '用户名不存在！'
elif try1 == '1':
    print '登录成功！'
    print '--------------------------------------------------'
    user_info = client.service.user(usr, pwd)
    for item in user_info.string[:-1]:
        print item + ' ',
    print ''
    print '--------------------------------------------------'
    
    files_info = client.service.files(usr, pwd)
    for i in range(len(files_info.stringArray)):
        for j in range(4):
            print files_info.stringArray[i].string[j],
        print ''

    print '--------------------------------------------------'

    oprt = raw_input('请选择您要进行的操作（删除[d]/阅读[R]）：')
    print '--------------------------------------------------'
    if oprt == 'd':
        index = raw_input('请输入您要删除的文件序号：')
        print '--------------------------------------------------'
        file_name = u'文件' + index
        file_delete = client.service.delete(usr, file_name)
        if file_delete == -1:
            print '您无权删除该文件！'
        elif file_delete == 1:
            print '删除成功!'
    else:
        index = raw_input('请输入您要查看的文件序号：')
        print '--------------------------------------------------'
        file_name = u'文件' + index
        file_read = client.service.read(usr, file_name)
        if file_read.string[0] == '2':
            print '您无权阅读该文件！'
        elif file_read.string[0] == '1':
            print file_read.string[1]
            print '--------------------------------------------------'
            flag = raw_input('是否修改该文件？ [y/N] ')
            if flag == 'y':
                print '--------------------------------------------------'
                print '请输入修改后的内容：'
                txt = raw_input()
                file_edit = client.service.edit(usr, file_name, txt)
                print '--------------------------------------------------'
                if file_edit == -1:
                    print '您无权修改该文件！'
                elif file_edit == 1:
                    print '修改成功!'
            else:
                pass

print '--------------------------------------------------' 
