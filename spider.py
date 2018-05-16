#coding=utf-8
#煎蛋妹子图爬虫

import requests
from bs4 import BeautifulSoup as BS
import re
import os
import threading
import urllib.request as UR

url = 'http://jandan.net/ooxx/page-'
file_name = 1
lock = threading.Lock()


def spider(url):
    headers = {'User-Agent': 'baidu_spider v2.0'}#你好，我是百度蜘蛛，请不要拦我
    r = requests.get(url, headers=headers)
    soup_root = BS(r.content, 'html5lib')
    print(r.text)
    soup_list = soup_root.ol
    image_tag = soup_list.find_all(name='a', attrs={'class': 'view_img_link'})
    for attr in image_tag:
        img_url = "http:" + (attr['href'])
        global file_name
        UR.urlretrieve(img_url, "pictures/" + str(file_name) + '.jpg')
        lock.acquire()
        file_name += 1
        lock.release()


def main(start_page=410 , end_page=416):
	if not os.path.exists('pictures'):
		os.mkdir('pictures')
	threads = []
	for i in range(start_page, end_page+1):
		threads.append(threading.Thread(target=spider, args=(url + str(i),)))
	for i in threads:
		i.start()
	for i in threads:
		i.join()
	print('下载完成')

if __name__ == '__main__':
    main()
