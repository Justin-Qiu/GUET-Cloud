#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import os.path
import time

'''
用户登录函数：

输入参数
    用户名，口令
返回值
    登录成功：'1', 姓名，性别，单位，职务，域，文件信息（文件名，大小，修改日期，权限）
    密码错误：'2'
    用户名不存在：'3'
'''
def user_log(usr, pwd):

    #连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost', 
            user='admin', 
            passwd='123456', 
            db='project',
            charset='utf8'
            )
            
    # 创建游标
    cur = conn.cursor()
    
    # SQL查询语句
    sql = "SELECT * FROM users WHERE loginid = '%s'" % usr
    
    # 执行SQL语句
    cur.execute(sql)
    
    # 获取用户信息
    results = cur.fetchall()
    for row in results:
        pass_word = row[2]
        if pwd == pass_word:
            name = row[3]
            sex = row[4]
            unitid = row[5]
            title = row[6]
            
            # 性别标识符转中文
            sex = str(sex)
            if sex == '0':
                sex_zh = u'男'
            elif sex == '1':
                sex_zh = u'女'
                
            # 查询所在单位
            sql_unit = "SELECT * FROM unit WHERE id = %d" % unitid
            cur.execute(sql_unit)
            result_unit = cur.fetchall()
            unit_name = result_unit[0][1]
            if unit_name == u'西安电子科技大学':
                area = u'域内'
            else:
                area = u'域外'
            
            # 获取所有文件和权限
            files = []
            for i in os.walk('files'):
                i[2].sort()
                for j in i[2]:
                
                    # 获取文件大小
                    file_size = os.path.getsize('files/%s' % j)
                    if file_size < 1024:
                        file_size = str(file_size) + 'B'
                    elif file_size < (1024 * 1024):
                        file_size = '%.1f' % (float(file_size)/1024) + 'KB'
                    elif file_size < (1024 * 1024 * 1024):
                        file_size = '%.1f' % (float(file_size)/(1024 * 1024)) + 'MB'
                    elif file_size < (1024 * 1024 * 1024):
                        file_size = '%.1f' % (float(file_size)/(1024 * 1024 * 1024)) + 'GB'
                    else:
                        file_size = '%.1f' % (float(file_size)/(1024 * 1024 * 1024 * 1024)) + 'TB'
                        
                    # 获取文件最后修改时间
                    file_time = os.stat('files/%s' % j).st_mtime
                    struct_time = time.localtime(file_time)
                    if struct_time.tm_mon < 10:
                        mon = '0' + str(struct_time.tm_mon)
                    else:
                        mon = str(struct_time.tm_mon) 
                    if struct_time.tm_mday < 10:
                        mday = '0' + str(struct_time.tm_mday)
                    else:
                        mday = str(struct_time.tm_mday) 
                    if struct_time.tm_hour < 10:
                        hour = '0' + str(struct_time.tm_hour)
                    else:
                        hour = str(struct_time.tm_hour) 
                    if struct_time.tm_min < 10:
                        mins = '0' + str(struct_time.tm_min)
                    else:
                        mins = str(struct_time.tm_min)
                    if struct_time.tm_sec < 10:
                        sec = '0' + str(struct_time.tm_sec)
                    else:
                        sec = str(struct_time.tm_sec)
                    file_time = (str(struct_time.tm_year) + '-' + 
                                 mon + '-' + mday + ' ' + hour + ':' + mins + ':' + sec)
                    
                    # 从数据库中读取用户权限
                    cur.execute("SELECT * FROM files WHERE fname = '%s'" % j)
                    result_file = cur.fetchall()
                    if title == u'校长':
                        colume = 2
                    elif title == u'院长':
                        colume = 3
                    elif title == u'老师':
                        colume = 4
                    elif title == u'学生':
                        colume = 5
                    trans = {'R': u'读', 'W': u'写', 'O': u'操作'}
                    for row in result_file:
                        row[colume]
                        auth = u''
                        for cha in row[colume]:
                            auth = auth + trans[cha]
                        files.append([row[1], file_size, file_time, auth])
            
            # 返回信息
            return '1', name, sex_zh, unit_name, title, area, files
        else:
        
            # 口令错误
            return '2'
       
    # 用户不存在
    return '3'

    # 关闭数据库连接
    conn.close()

  
'''
用户读文件函数：

输入参数
    用户名，文件名
返回值
    有读权限：'1'，文件内容
    无读权限：'2'，空内容
'''
def file_read(usr, file_name):

    #连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost', 
            user='admin', 
            passwd='123456', 
            db='project',
            charset='utf8'
            )
            
    # 创建游标
    cur = conn.cursor()
    
    # SQL查询语句
    sql = "SELECT * FROM users WHERE loginid = '%s'" % usr
    
    # 执行SQL语句
    cur.execute(sql)
    
    # 获取用户信息
    results = cur.fetchall()
    for row in results:
        title = row[6]
        cur.execute("SELECT * FROM files WHERE fname = '%s'" % file_name)
        result_file = cur.fetchall()
        if title == u'校长':
            colume = 2
        elif title == u'院长':
            colume = 3
        elif title == u'老师':
            colume = 4
        elif title == u'学生':
            colume = 5
        
        # 根据用户权限读取文件
        for fil in result_file:
            if 'R' in fil[colume]:
                with open('files/%s' % file_name, 'r') as f:
                    txt = f.read()
                return '1', txt
            else:
                return '2', ''    

    # 关闭数据库连接
    conn.close()


'''
用户写文件函数：

输入参数
    用户名，文件名，文件内容
返回值
    有写权限且写入成功：1
    无写权限：-1
''' 
def file_write(usr, file_name, txt):

    #连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost', 
            user='admin', 
            passwd='123456', 
            db='project',
            charset='utf8'
            )
            
    # 创建游标
    cur = conn.cursor()
    
    # SQL查询语句
    sql = "SELECT * FROM users WHERE loginid = '%s'" % usr
    
    # 执行SQL语句
    cur.execute(sql)
    
    # 获取用户信息
    results = cur.fetchall()
    for row in results:
        title = row[6]
        cur.execute("SELECT * FROM files WHERE fname = '%s'" % file_name)
        result_file = cur.fetchall()
        if title == u'校长':
            colume = 2
        elif title == u'院长':
            colume = 3
        elif title == u'老师':
            colume = 4
        elif title == u'学生':
            colume = 5
        
        # 根据用户权限修改文件
        for fil in result_file:
            if 'W' in fil[colume]:
                with open('files/%s' % file_name, 'w') as f:
                    f.write('%s' % txt)
                return 1
            else:
                return -1   

    # 关闭数据库连接
    conn.close()


'''
用户删除文件函数：

输入参数
    用户名，文件名
返回值
    有删除权限且删除成功：1
    无删除权限：-1
''' 
def file_del(usr, file_name):

    #连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost', 
            user='admin', 
            passwd='123456', 
            db='project',
            charset='utf8'
            )
            
    # 创建游标
    cur = conn.cursor()
    
    # SQL查询语句
    sql = "SELECT * FROM users WHERE loginid = '%s'" % usr
    
    # 执行SQL语句
    cur.execute(sql)
    
    # 获取用户信息
    results = cur.fetchall()
    for row in results:
        title = row[6]
        cur.execute("SELECT * FROM files WHERE fname = '%s'" % file_name)
        result_file = cur.fetchall()
        if title == u'校长':
            colume = 2
        elif title == u'院长':
            colume = 3
        elif title == u'老师':
            colume = 4
        elif title == u'学生':
            colume = 5
        
        # 根据用户权限删除文件
        for fil in result_file:
            if 'O' in fil[colume]:
                os.remove('files/%s' % file_name)
                cur.execute("DELETE FROM files WHERE fname = '%s'" % file_name)
                conn.commit()
                return 1
            else:
                return -1

    # 关闭数据库连接
    conn.close()
