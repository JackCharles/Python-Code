#coding:utf-8
#动态绑定属性和方法
class Student(object):
	pass

bob = Student()
bob.name = 'Bob'#动态给[实例]绑定一个属性name
print(bob.name)

#给实例绑定方法
def set_age(self, age):
	self.age = age
from types import MethodType
bob.set_age = MethodType(set_age, bob)#给bob绑定一个方法
bob.set_age(18)
print(bob.age)#18

#给一个实例绑定的方法，对另一个实例是不起作用的
alice = Student()
#alice.set_age(18)#AttributeError: 'Student' object has no attribute 'set_age'
#为了给所有实例都绑定方法，可以给class绑定方法
def set_score(self,score):
	self.score = score
Student.set_score = set_score#直接赋值即可
alice.set_score(80)
print(alice.score)

#使用__slots__限定实例属性,不能添加__slots__限定以外的属性
class Stu(object):
	__slots__ = ('name','score')

tom = Stu()
tom.name = 'Tom'
tom.score = 90
#tom.age = 18#AttributeError: 'Stu' object has no attribute 'age'
print(tom.name,':',tom.score)
#__slots__仅对当前类起作用，不影响子类

#使用@property，将方法变成属性调用，可实行强制检查
class Demo(object):
	@property#相当于变成getter
	def score(self):
		print("This is a getter!")
		return self._score;
	@score.setter#相当于变成setter
	def score(self, score):
		if not isinstance(score,int):
			raise ValueError("score must be an integer!")
		if score<0 or score >100:
			raise ValueError("score must between 0 and 100!")
		self._score = score
	
d = Demo()
#d.score = 1000#ValueError: score must between 0 and 100!
d.score = 89#setter
print(d.score)#getter

#Python枚举
from enum import Enum #Enum类
Month = Enum('Month',('Jan','Feb','Mar'))#第一个参数为枚举名称
print(Month.Jan.value)
print(Month['Jan'].value)
for name, member in Month.__members__.items():#遍历
	print(name, '=>', member, ',', member.value)
	
#动态创建类type(<class-name>,<base-class-tuple>,<class-mathod-dict>)
def member_func(self):
	print("I am member function!")
Hello = type("Hello",(object,), dict(mem=member_func))#动态创建类
h = Hello()
h.mem()

#错误和调试
#捕获错误
#try...except...[else...][finally...]
try:
	a = 5/2
except ZeroDivisionError as e:#可用BaseException捕获所有异常
	print(e)
else:#可选
	print("No Error")
finally:#可选
	print("finally！")
	
	
#记录错误
import logging
#logging可以打印完错误信息后继续执行并正常退出，
#logging还可以将错误写到日志文件中，以便日后查看
def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)

main()
print('END')

#抛出异常
class FooError(ValueError):#define FooError
	pass
def foo1(s):
    n = int(s)
    if n==0:
        raise FooError('invalid value: %s' % s)
    return 10 / n

foo1('1')

#调试技巧
#断言assert <something-should-be>,<else>
def divv(s):
	assert s!=0,'s is zero!'
	return 10/s
print(divv(1))

#logging
logging.basicConfig(level=logging.INFO)#配置记录级别
#官方文档：http://python.usyiyi.cn/python_278/library/logging.html