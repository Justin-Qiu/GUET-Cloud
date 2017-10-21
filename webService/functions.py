#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import os.path
import time

def key_gen(group_num):
    root_key = 'CREpfaBC7L6spPEkB1ix07EYA5XeSoFw1UgrceAXsHjAabMRUiuTQni30wb1YepL70aejxktqI90Cy3Tlkpd660IVvRA9uUXw6ajBy9Gi02HQ3Df5HtSECROHovVrYGrtSRjdNdfthZuYsuh0AISzLOMCRKVeP58lL9IH0hoI9C103Mjij4iES82TE3jCFlCA4fb8UNM8UJHXzUfkuKB8FmdkKyHY9krihA6bpXHOT89xs5O7ptqjawKjZA3FqraEjT0W2oTp1PDqoEpInBLs8OwU18T3BeP0sgU1K5sOd2SxptDpHpTjRQZC3EAIofwdeq9X2te7YPUyEnnVN5PrtTVHJL3PpRmA4Ycd8hVEkjG1PtQWHf4Pfg6lVkjYNC5TOjTGe1C6lXcFqrY'
    
    tree = [[1,2,3], [4,5,6], [7,8], [9,10], [11,12], [13,14], [15,16], [17,18], [19,20], [21,22], [23,24], None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    
    result = []
    result.append(0)
    def pre_root_traversal(root,tree):
        if isinstance(root, list):
            for i in range(0, len(root)):
                if root[i] not in result:
                    result.append(root[i])
                    if tree[root[i]] != None:
                        pre_root_traversal(tree[root[i]], tree)

    pre_root_traversal(tree[0], tree)
    root_result = result

    result = []
    result.append(group_num)
    pre_root_traversal(tree[group_num], tree)
    gen_result = result

    start = 0
    for i in range(0, len(root_result)):
        if root_result[i] == group_num:
            start = i

    group_key = root_key[start*16:(start+len(gen_result))*16]

    for i in range(0, len(gen_result)):
	if gen_result[i] not in root_result:
	    return -1

    return group_key


'''
User registration function

Input parameter
    User ID, 
    Password, 
    Name,
    Gender in Chinese,
    Group ID
Return value
    Registration successful: 1, group key
    User ID already exists: 2, ''
'''
#def user_reg(usr, pwd, name, sex_zh, unit, title):
def user_reg(usr, pwd, name, sex_zh, group_num):
    
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
    '''
    # Unit transfer  
    sql_unit = "SELECT * FROM unit WHERE unit_name = '%s'" % unit
    cur.execute(sql_unit)
    result_unit = cur.fetchall()
    unitid = result_unit[0][0] 
    '''
             
    # Avoid duplication
    sql_search = "SELECT * FROM user WHERE loginid = '%s'" % usr
    
    if cur.execute(sql_search) == 0L:
    
        # Insert into database
        #sql = "insert into users(loginid, pass_word, name, sex, unitid, title) values('%s', '%s', '%s', '%d', '%d', '%s')" % (usr, pwd, name, sex, unitid, title) 
        sql = "insert into user(loginid, pass_word, name, sex, groupid) values('%s', '%s', '%s', '%d', '%d')" % (usr, pwd, name, sex, group_num) 
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        
        key = key_gen(group_num)
        
        return '1', key
    
    # Registeration failed
    else:
        return '2', ''

'''
用户登录函数：

输入参数
    用户名，口令
返回值
    登录成功：'1', 姓名，性别，组编号，文件信息（文件名，大小，修改日期，组编号, upload user）
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
    #sql = "SELECT * FROM users WHERE loginid = '%s'" % usr
    sql = "SELECT * FROM user WHERE loginid = '%s'" % usr
    
    # 执行SQL语句
    cur.execute(sql)
    
    # 获取用户信息
    results = cur.fetchall()
    
    for row in results:
        pass_word = row[2]
        if pwd == pass_word: #and pass_word != '':
            name = row[3]
            sex = row[4]
            #unitid = row[5]
            #title = row[6]
            groupid = str(row[5])
            
            tree = [[1,2,3], [4,5,6], [7,8], [9,10], [11,12], [13,14], [15,16], [17,18], [19,20], [21,22], [23,24], None, None, None, None, None, None, None, None, None, None, None, None, None, None]
            
            group_list = []
            node = row[5]
            group_list.append(node)
            if tree[node] != None:
                group_list.extend(tree[node])
                for i in range(len(tree[node])):
                    if tree[tree[node][i]] != None:
                        group_list.extend(tree[tree[node][i]])
            
            # 性别标识符转中文
            sex = str(sex)
            if sex == '0':
                sex_zh = u'男'
            elif sex == '1':
                sex_zh = u'女'
            
            '''    
            # 查询所在单位
            sql_unit = "SELECT * FROM unit WHERE id = %d" % unitid
            cur.execute(sql_unit)
            result_unit = cur.fetchall()
            unit_name = result_unit[0][1]
            if unit_name == u'西安电子科技大学':
                area = u'域内'
            else:
                area = u'域外'
            '''
            
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
                    #cur.execute("SELECT * FROM files WHERE fname = '%s'" % j)
                    cur.execute("SELECT * FROM file WHERE fname = '%s'" % j)
                    result_file = cur.fetchall()
                    '''
                    if title == u'校长':
                        colume = 2
                    elif title == u'院长':
                        colume = 3
                    elif title == u'老师':
                        colume = 4
                    elif title == u'教师':
                        colume = 4
                    elif title == u'学生':
                        colume = 5
                    trans = {'R': u'读', 'W': u'写', 'O': u'删'}
                    '''
                    for row in result_file:
                        '''
                        for cha in row[colume]:
                            auth = auth + trans[cha]
                        if row[colume] == '':
                            auth = u'无'
                        '''
                        if row[2] in group_list:
                            auth = str(row[2])
                            from_user = row[3]
                            files.append([row[1], file_size, file_time, auth, from_user])
            
            # 返回信息
            #return '1', name, sex_zh, unit_name, title, area, files
            return '1', name, sex_zh, groupid, files
        else:
        
            # 口令错误
            return '2'
       
    # 用户不存在
    return '3'

    # 关闭数据库连接
    conn.close()

'''
用户上传文件函数：

输入参数
    username, group id, 文件名，文件内容
返回值
    上传失败：1
    上传成功：-1
''' 
def file_upload(usr, groupid, file_name, txt):

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
    
    file_name = file_name.encode('utf-8')
    
    #sql_search = "SELECT * FROM files WHERE fname = '%s'" % file_name
    sql_search = "SELECT * FROM file WHERE fname = '%s'" % file_name
    
    if cur.execute(sql_search) == 0L:
        #sql = "insert into files(fname,校长,院长,老师,学生) values('%s','RWO','RWO','RWO','RWO')" % file_name
        sql = "insert into file(fname, groupid, usr) values('%s','%d','%s')" % (file_name, groupid, usr)
        cur.execute(sql)
        conn.commit()
        
        txt = txt.encode('utf-8')
        with open('files/%s' % file_name, 'w') as f:
            f.write('%s' % txt)   
        return 1
    else:
        return -1
    
    # 关闭数据库连接
    conn.close()

'''
用户读文件函数：

输入参数
    文件名
返回值
    文件内容, 组编号
'''
def file_read(file_name):
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
    #sql = "SELECT * FROM users WHERE loginid = '%s'" % usr
    sql = "SELECT * FROM file WHERE fname = '%s'" % file_name
    
    # 执行SQL语句
    cur.execute(sql)
    
    # 获取用户信息
    results = cur.fetchall()
    for row in results:
        groupid = str(row[2])
        '''
        title = row[6]
        cur.execute("SELECT * FROM files WHERE fname = '%s'" % file_name)
        result_file = cur.fetchall()
        if title == u'校长':
            colume = 2
        elif title == u'院长':
            colume = 3
        elif title == u'老师':
            colume = 4
        elif title == u'教师':
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
       '''
    
    # 关闭数据库连接
    conn.close()
    
    with open('files/%s' % file_name, 'r') as f:
        txt = f.read()
    return txt, groupid

'''
用户写文件函数：

输入参数
    用户名，文件名，文件内容
返回值
    有写权限且写入成功：1
    无写权限：-1
''' 
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
        elif title == u'教师':
            colume = 4
        elif title == u'学生':
            colume = 5
        
        # 根据用户权限修改文件
        txt = txt.encode('utf-8')
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
'''
用户编辑文件权限函数：

输入参数
    用户名，文件名
返回值
    有编辑权限：1
    无编辑权限：-1
''' 
'''
def file_write_auth(usr, file_name):

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
        elif title == u'教师':
            colume = 4
        elif title == u'学生':
            colume = 5
        
        # 根据用户权限修改文件
        for fil in result_file:
            if 'W' in fil[colume]:
                return 1
            else:
                return -1   

    # 关闭数据库连接
    conn.close()
'''
'''
用户删除文件函数：

输入参数
    用户名，文件名
返回值
    有删除权限且删除成功：1
    无删除权限：-1
''' 
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
        elif title == u'教师':
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
'''
'''
文件名搜索函数：

输入参数
    用户名，关键词
返回值
    有搜索结果：文件信息（文件名，大小，修改日期，权限）
    无搜索结果：[]
'''
'''
def file_search(usr, kw):

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
        #name = row[3]
        #sex = row[4]
        #unitid = row[5]
        title = row[6]
    
    # 获取所有文件和权限
    files = []
    for i in os.walk('files'):
        i[2].sort()
        for j in i[2]:       
            if kw in j:
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
                elif title == u'教师':
                    colume = 4
                elif title == u'学生':
                    colume = 5
                trans = {'R': u'读', 'W': u'写', 'O': u'删'}
                for row in result_file:
                    row[colume]
                    auth = u''
                    for cha in row[colume]:
                        auth = auth + trans[cha]
                    if row[colume] == '':
                        auth = u'无'
                    files.append([row[1], file_size, file_time, auth])

    return files
    
    # 关闭数据库连接
    conn.close()
'''
