#coding:utf-8
#偏函数
import functools
print(int("10",16))#int(str[,base])base为进制，默认为10

#定义了一个偏函数，实际就是把某些参数固定住
int2 = functools.partial(int ,base=2)
print(int2('1000000'))

#Python 面向对象编程
#类声明：class <class-name>(<parent-class-name>):
#The default parent-class-name is object.
class Student(object):
#__init__方法相当于C++构造函数，__init__名字不能变
#类中定义方法的第一个参数必须是self，表示它本身，
#相当于c++中this指针,但该参数在函数调用时无需给出
#Python类中成员变量也无需事先声明
	def __init__(self, name, score):
		self.name = name
		self.score = score
	def print_score(self):
		print('%s: %s' %(self.name, self.score))

Bob = Student('Bob',90)
Alice = Student('Alice',85)

Bob.print_score()
Alice.print_score()

#和静态语言不同，Python允许对实例变量绑定任何数据，
#也就是说对于两个实例变量，虽然它们都是同一个类的
#不同实例，但拥有的变量名称都可能不同
Bob.age = 18
print(Bob.age)#18
#print(Alice.age)#AttributeError: 'Student' object has no attribute 'age'


class stu(object):
	def __init__(self, name, score):
		#将成员写成__XX(两个_)形式的就成了私有成员变量，外部不能直接访问
		#但实际上python只是将该变量改了名字而已通常为_<class-name>__<var-name>
		#通过上述名字仍然可以访问私有变量,python不能阻止你干坏事，只有你自觉
		#通常_x(一个_)也表示私有变量，虽然它可以被访问，但约定俗成视为私有
		self.__name = name;
		self.__score = score;
	def print_score(self):
		print("%s: %s" %(self.__name, self.__score))

A = stu("A",11)
A.print_score()
#print(A.__name)#AttributeError: 'stu' object has no attribute '__name'
print(A._stu__name)#A

#继承
class Animal(object):
	def run(self):
		print("Animal is running...")

class Dog(Animal):
	def run(self):#子类覆盖父类方法
		print("Dog is running...")
	
dog = Dog()
dog.run()

#多态（动态绑定）
class Cat(Animal):
	def run(self):
		print("Cat is running...")

cat = Cat()		
def run_twice(animal):
	animal.run()
	animal.run()

run_twice(dog)
run_twice(cat)
#“开闭”原则：
#对扩展开放：允许新增Animal子类；
#对修改封闭：不需要修改依赖Animal类型的run_twice()等函数。

'''
对于静态语言（例如Java）来说，如果需要传入Animal类型，则传入的对
象必须是Animal类型或者它的子类，否则将无法调用run()方法。
对于Python这样的动态语言来说，则不一定需要传入Animal类型。我们只
需要保证传入的对象有一个run()方法就可以了,这就是动态语言的“鸭子类型”，
它并不要求严格的继承体系，一个对象只要“看起来像鸭子，走起路来像鸭子”，
那它就可以被看做是鸭子。
Python的“file-like object“就是一种鸭子类型。对真正的文件对象，它有一
个read()方法，返回其内容。但是许多对象，只要有read()方法，都被视为
“file-like object“。许多函数接收的参数就是“file-like object“，你不一
定要传入真正的文件对象，完全可以传入任何实现了read()方法的对象。
'''

#获取对象信息
print(type(123))#<class 'int'>
print(type(abs))#<class 'builtin_function_or_method'>
print(type(dog))#<class '__main__.Dog'>
print(type(123)==type(456))#True
print(type(123)==int)#True
print(type('abc')==type('xyz'))#True
print(type('abc')==str)#True
print(type(dog)==Dog)#True
print(type(dog)==Animal)#False

#判断函数类型
import types#使用types模块中定义的常量
print(type(run_twice)==types.FunctionType)#True
print(type(abs)==types.BuiltinFunctionType)#True
print(type(lambda x: x*x)==types.LambdaType)#True
print(type((x for x in range(10)))==types.GeneratorType)#True

#type只能判断绝对相等，不能判断继承关系，isinstance函数可以
print(isinstance(dog,Dog))#True
print(isinstance(dog,Animal))#True
print(isinstance(dog,Cat))#False
#isinstance还可判断是不是某些类型中的一种
print(isinstance([1,2,3],(list,tuple)))#True
print(isinstance('str',(list,int)))#False

#如果要获得一个对象的所有属性和方法，可以使用dir()函数，
#它返回一个包含字符串的list:
print(dir('ABC'))
#其中部分方法是形如__XX__形式的，这是该对象的特殊方法，
#比如__len__,当我们调用len(dog)时，相当于len函数在内部
#调用dog.__len__()，__XX__形式的方法都可以重写，比如：

class len_demo(object):
	def __len__(self):#override
		return 991
demo = len_demo()
print(len(demo))#991
print(demo.__len__())#991

#getattr(<obj>, <attr>[,default])-->value获取对象属性
print(getattr(Bob,'score'))#90
print(getattr(Alice,'age','No age!'))#No age!
#hasattr(<obj>,<attr>)-->bool测试是否有某个属性
print(hasattr(Bob,'age'))#True
print(hasattr(Alice,'age'))#False
#setattr(<obj>,<attr>,<value>)设置某个属性
setattr(Bob,'age',30)
print(Bob.age)#30

#实例属性和类属性
class Computer(object):
	name = 'computer'#相当于C++的静态变量
	
lenovo = Computer()
dell = Computer()
print(lenovo.name)#lenovo实例没有name属性，转而访问Computer类属性name
print(dell.name)#computer
print(Computer.name)#computer，可通过类直接访问
lenovo.name = 'lenovo'
print(lenovo.name)#实例对象有name属性后屏蔽掉相同类属性，输出lenovo
print(Computer.name)#computer
#在编写程序的时候，千万不要把实例属性和类属性使用相同的名字，
#因为相同名称的实例属性将屏蔽掉类属性，但是当你删除实例属性后，
#再使用相同的名称，访问到的将是类属性
