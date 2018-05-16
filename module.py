#!/user/bin/env python3
# coding:utf-8

'a test module'

__author__ = 'JackCharles'

import sys


def test():
    args = sys.argv
    if len(args) == 1:
        print('Hello world!')
    elif len(args) == 2:
        print('Hello, %s' % args[1])
    else:
        print('Too many arguments!')


if __name__ == '__main__':
    test()

'''
第1行注释可以让这个hello.py文件直接在Unix/Linux/Mac上运行;
第2行注释表示.py文件本身使用标准UTF-8编码；
第4行是文档注释，任何模块代码的第一个字符串都被视为模块的
文档注释，模块定义的文档注释也可以用特殊变量__doc__访问；
第6行使用__author__变量把作者写进去；
以上就是Python模块的标准文件模板，当然也可以全部删掉不写。

sys模块有一个argv变量，用list存储了命令行的所有参数。
argv至少有一个元素，因为第一个参数永远是该.py文件的名称。

if __name__=='__main__':
    test()
当我们直接运行module模块时，Python解释器把一个特殊变量
__name__置为__main__，而如果在其他地方导入该模块时，if判断
将失败，因此这种if测试可以让一个模块通过命令行运行时执行一
些额外的代码，最常见的就是测试模块。

类似__xxx__这样的变量是特殊变量，可以被直接引用，但是有特殊用途
类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该
被直接引用，比如_abc，__abc等；之所以我们说，private函数和变量
“不应该”被直接引用，而不是“不能”被直接引用，是因为Python并没有
一种方法可以完全限制访问private函数或变量，但是，从编程习惯上不
应该引用private函数或变量。
'''
