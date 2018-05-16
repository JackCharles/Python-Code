#encoding = utf-8

__author__ = "zj2011@live.com"

import requests
import re
import os
import threading
import urllib.request as UR

ComicName = 39 #进击的巨人

pattern  = re.compile(r'var\smhurl\s=\s"([a-zA-Z0-9/.]+)";')
pattern2 = re.compile(r'pure-u-lg-1-4"><a href="([a-z0-9]+)/"')
failedList = []
mutex = threading.Lock()

#one thread download one chapter
class spiderAll(threading.Thread):
	def __init__(self, url, fileName):
		threading.Thread.__init__(self)
		self.__url__ = url
		self.__fileName__ = fileName

	def run(self):
		index = 0
		retry = 0
		while(True):
			htmlText = requests.get(self.__url__+'/index_'+str(index)+'.html').text
			if htmlText=='Not Found':
				break
			else:
				imageUrl = "http://101.96.10.31/p1.xiaoshidi.net/" + pattern.findall(htmlText)[0]
				while retry<3:
					try:
						UR.urlretrieve(imageUrl, self.__fileName__+"/"+str(index+1)+'.jpg')
						print("%s download finish." %imageUrl)
						retry = 100
					except:
						retry += 1
						print("%s download failed, retry %s times..." %(imageUrl, retry))
						
				if retry==3:
					mutex.acquire()
					failedList.append(imageUrl)
					mutex.release()
					print("%s download failed and I don't know why..." %imageUrl)
				retry = 0
				index += 1

		
def downloadAll():
	htmlText = requests.get('http://manhua.fzdm.com/39/').text
	chapterSet = set(pattern2.findall(htmlText))
	if not chapterSet:
		print('http://manhua.fzdm.com/39/ request failed...')
		return
		
	ComicName = "进击的巨人ALL"
	if os.path.isdir(ComicName):
		print("The folder %s alreday exists, please delete it and try again." %ComicName)
		return
		
	os.mkdir(ComicName)
	threadList = []
	
	for chapter in chapterSet:
		folderName = ComicName+"/"+chapter
		print(folderName)
		os.mkdir(folderName)
		url = 'http://manhua.fzdm.com/39/'+chapter
		threadList.append(spiderAll(url, folderName))

	for i in range(0, len(threadList)):
		threadList[i].start()
	for i in range(0, len(threadList)):
		threadList[i].join()
		
	with open(ComicName+'/FailedList.txt','w') as f:
		for item in failedList:
			f.write(item+'\n')
	print('Download finished, see the FailedList.txt for details.')

if __name__=='__main__':
	downloadAll()