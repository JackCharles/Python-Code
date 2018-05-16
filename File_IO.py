#coding:utf-8

#文件读写
f = open('C:/Users/admin/Desktop/test.txt', 'r')
print(f.read())#read()函数一次读取文件全部
f.close()#关闭文件

#由于文件操作随时可能产生异常，当产生异常时f.close()不会被调用
#此时可能导致文件未保存而数据丢失，稳妥的做法是用try...[except]...finally
#包围，但这样太麻烦，于是就引入了下面 with...as...:语句
#with open(...) as <return-object>:他会自动调用close()方法，无论是否有异常发生
with open('C:/Users/admin/Desktop/test.txt','r') as fo:
	print(fo.read())#读入全部
	fo.seek(0,0)#设置文件指针位置：开始0，当前1，结尾2，偏移正数向后，负数向前
	print(fo.read(10))#只读取10个字节
	fo.seek(0,0)
	print(fo.readline())#读取一行(包含换行符)
	fo.seek(0,0)
	for x in fo.readlines():#readlines()读取所有并按行返回一个list
		print(x.strip())#strip(rm)去掉字符串开头和结尾的字符串rm
		#strip()则默认删除空白符\n\t\r''等
#open()函数可选参数encoding='ascii',errors='ignore'

#写文件
with open('C:/Users/admin/Desktop/writeTest.txt','w') as f:
	f.write('file write test!\n')#write不会自动换行
	f.write('Line 2')

#String IO(StringIO顾名思义就是在内存中读写str)
from io import StringIO
sio = StringIO()#Get a StringIO Object
print(sio.write('Hello world!'))#返回写入字符数12
print(sio.write('你好,世界！'))#6
print(sio.getvalue())#输出存的内容

#要读取StringIO，可以用一个str初始化StringIO，然后像读文件一样读取
f = StringIO('Hello!\nHi!\nGoodbye!')
while True:
	s = f.readline()
	if s == '':
		break
	print(s.strip())

#BytesIO用于操作二进制数据
from io import BytesIO
f = BytesIO()
f.write('中文'.encode('utf-8'))#写入的不是str，而是经过UTF-8编码的bytes
print(f.getvalue())

#和StringIO类似，可以用一个bytes初始化BytesIO，然后像读文件一样读取
f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(f.read().decode('utf-8'))#解码

#操作文件和目录
import os#用到os模块
print(os.name)#操作系统类型nt=windows,posix=linux,unix,mac_os
#uname()函数可以获取详细系统信息,windows不支持该函数
#print(os.environ)#以dict形式返回环境变量
for k,v in os.environ.items():
	print(k,'-->',v)

#操作文件和目录的函数在os和os.path模块中
print(os.path.abspath('.'))#查看当前路径的绝对路径
#os.path.join([path1],[path2]...)将多个路径组合后返回
newdir = os.path.join('C:/Users/admin/Desktop','newdir')
os.mkdir(newdir)#创建目录
os.rmdir(newdir)#删除目录

#os.path.split(<dir>)拆分路径，以tuple形式返回最后一个路径和前面剩下的总路径
print(os.path.split('C:/Users/admin/Desktop/test.txt'))
#os.path.splitext(<dir>)得到文件扩展名,以tuple形式返回
print(os.path.splitext('C:/Users/admin/Desktop/test.txt'))
#这些合并、拆分路径的函数并不要求目录和文件要真实存在，它们只对字符串进行操作

pt = 'C:/Users/admin/Desktop/'
os.rename(pt+'writeTest.txt',pt+'rename.txt')#文件重命名
os.remove(pt+'rename.txt')#删除文件

print(os.listdir(pt))#os.listdir(<dir>)列出指定目录下所有文件和目录并返回list
#可以用os.path.isdir(<dir>)或isfile(<dir>)或自行判断字符串来进行过滤
#shutil模块是os模块的补充,详见https://docs.python.org/3.5/library/shutil.html

#Python序列化参见https://blog.oldj.net/2010/05/26/python-pickle/
#所谓序列化即，将一个结构性的变量(如dict或自定义的结构体等)转换成一个字节序列
#方便存储或网络传输，该过程称为序列化pickling,反之恢复过程叫反序列化unpickling
import pickle
#d = dict(name='Bob', age=20, score=88)
d = {'name':'Bob','age':20,'score':88}
d['name'] = 'Alice'
print(d)
print(pickle.dumps(d))#序列化，返回序列化后的字符串(注意：dumps)

with open(pt+'dump.txt','wb+') as f:
	pickle.dump(d,f,1)#写入文件，参数1可选表示高压缩(注意：dump)
	#当然也可以反序列化
	f.seek(0,0)
	d = pickle.load(f)#从文件中反序列化，当然对应的还有loads(str)
print(d)

#比pickle更好更快的所有语言标准方法JSON
import json
d = dict(name='Bob', age=20, score=88)
sj = json.dumps(d)#序列化为json标准格式
print(sj)#操作模式同pickle可写入文件

#任意对象到json转换
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)
#print(json.dumps(s))#Error,JSON不知道怎么转换
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

print(json.dumps(s, default=student2dict))
 #default参数传入一个自定义函数告诉json怎么转换，该函数应返回JSON通用类型dict,list.str等
stuj = json.dumps(s, default=lambda obj: obj.__dict__)#简便方法，调用对象__dict__属性

#解JSON
def dict2student(d):#定义解函数
    return Student(d['name'], d['age'], d['score'])

s1 = json.loads(stuj, object_hook=dict2student);#object_hook参数传入解函数
print(s1)