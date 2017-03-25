#coding: utf-8 

from suds.client import Client  
  
client = Client('http://localhost:7789/?wsdl', cache=None)

print ''

result = client.service.login(1615123100, 654321)
if result.string[0] == '1':
    print '登录成功！'
elif result.string[0] == '2':
    print '密码错误！'
elif result.string[0] == '3':
    print '用户名不存在！'

print ''

result = client.service.user(1615123100, 123456)
print result.string[0],
print result.string[1],
print result.string[2],
print result.string[3],
print result.string[4]

print ''

result = client.service.files(1615123100, 123456)
for i in range(len(result.stringArray)):
    for j in range(4):
        print result.stringArray[i].string[j],
    print ''

print ''

result = client.service.read(1615123105, u'文件01')
if result.string[0] == '1':
    print '有阅读权限'
elif result.string[0] == '2':
    print '无阅读权限'
print ''
print result.string[1]

#print dir(result.stringArray)
