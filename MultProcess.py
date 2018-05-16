#encoding = utf-8

#多进程

from multiprocessing import Process
import os

'''
def run_proc(name):
	print('Run child process %s (%s)...' %(name, os.getpid()))
	
if __name__=='__main__':
	print('Parent process %s.' %os.getpid())
	p = Process(target=run_proc, args=('test', ))
	print ('Child process will start.')
	p.start()
	p.join()
	print('child process end.')
	
'''
'''
from multiprocessing import Pool
import time, random

def long_time_task(name):
	print ('Run task %s (%s)...' %(name, os.getpid()))
	start =  time.time()
	time.sleep(random.random()*3)
	end = time.time()
	print('Task %s runs %0.2f seconds.' %(name, (end - start)))

if __name__=='__main__':
	print('Parent process %s.' %os.getpid())
	p = Pool(4)#限定同时跑4个进程
	for i in range(5):#这里给了5个进程，第五个要等到前四个某一个执行完毕，他才开始执行
		p.apply_async(long_time_task, args=(i, ))
	print('Waiting for all subprocesses done...')
	p.close()#join之前先要关闭pool，关闭pool之后就不能添加进程了
	p.join()
	print('All subprocesses done.')

'''

#python 外部调用
import subprocess

print ('nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)