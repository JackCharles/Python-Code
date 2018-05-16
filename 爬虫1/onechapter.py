#encoding = utf-8

__author__ = "zj2011@live.com"

import requests
import re
import os
import threading
import urllib.request as UR

ComicName = 39 #进击的巨人

pattern  = re.compile(r'<img\ssrc="(.+)"\sid=')
failedList = []
mutex = threading.Lock()

#one thread download one chapter
class spiderOneChapter(threading.Thread):
	def __init__(self, url, fileName):
		threading.Thread.__init__(self)
		self.__url__ = url
		self.__fileName__ = fileName

	def run(self):
		retry = 0
		htmlText = requests.get(self.__url__).text
		if not htmlText=='Not Found':
			imageUrl = pattern.findall(htmlText)[0]
			while retry<3:
				try:
					UR.urlretrieve(imageUrl, self.__fileName__)
					print("%s download finish." %imageUrl)
					retry=100
				except:
					retry+=1
					print("%s download failed, retry %s times..." %(imageUrl, retry))
			
			if retry==3:
				mutex.acquire()
				failedList.append(imageUrl)
				mutex.release()
				print("%s download failed and I don't know why..." %imageUrl)
				
		
def downloadOneChapter():
	print("if you do not know the chapter id, please read help document.")
	chapter = input("please input the chapter id you want to download:")
	url = 'http://manhua.fzdm.com/39/'+chapter+'/index_'
	if requests.get(url+'0.html').text=='Not Found':
		print('chapter id is incorrect, check it and try again.')
		return
		
	ComicName = "进击的巨人PART"
	if os.path.isdir(ComicName):
		print("The folder %s alreday exists, please delete it and try again." %ComicName)
		return
		
	os.mkdir(ComicName)
	os.mkdir(ComicName+"/"+chapter)
	threadList = []
	maxPage = 60
	for i in range(0,maxPage):
		fileName = ComicName+'/'+chapter+'/'+str(i)+'.jpg'
		threadList.append(spiderOneChapter(url+str(i)+'.html', fileName))

	for i in range(0, maxPage):
		threadList[i].start()
	for i in range(0, maxPage):
		threadList[i].join()
		
	with open(ComicName+'/FailedList.txt','w') as f:
		for item in failedList:
			f.write(item+'\n')
	print('Download finished, see the FailedList.txt for details.')


if __name__=='__main__':
	downloadOneChapter()