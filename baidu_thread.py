import requests
from queue import Queue
import threading
from bs4 import BeautifulSoup as bs
import time

headers = {
		'Host': 'www.baidu.com',
		'Connection': 'keep-alive',
		'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
		'sec-ch-ua-mobile': '?0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Sec-Fetch-Site': 'cross-site',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-User': '?1',
		'Sec-Fetch-Dest': 'document',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9'
		}

class BaiduSpaider(threading.Thread) :
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self._queue = queue
	def run(self) :
		while not self._queue.empty() :
			url = self._queue.get()
			#print("run里面的url"+ url)
			try:
				self.spider(url)
			except Exception as e:
				#print(e)
				pass

	def spider(self,url):
		#print("spider里面的url"+url)
		r= requests.get(url=url,headers=headers)
		#print(r.text)
		soup = bs(r.text, 'lxml')
		urls = soup.find_all(name='a', attrs={'target': '_blank', 'style': 'text-decoration:none;position:relative;'})
		for url in urls:
			#print(url['href'])
			need_url = requests.get(url=url['href'])
			print(need_url.url)
			if need_url.status_code == 200:
				with open(r'ip.txt', 'a+') as f:
					f.write(need_url.url + '\n')
					f.close
					time.sleep(1)

def main(keyword):
	queue = Queue(maxsize=5000)
	for i in range(0,370,10) :
		queue.put('https://www.baidu.com/s?wd=%s&pn=%s'%(keyword,str(i)))
		#print("mian里面的url"+'https://www.baidu.com/s?wd=%s&pn=%s'%(keyword,str(i)))

	thread = []
	thread_count = 15

	for i in range(thread_count):
		thread.append(BaiduSpaider(queue))
	for t in thread:
		t.start()
	for t in thread:
		t.join()

if __name__ == '__main__':
	print("""
 ____        _     _            _ 
| __ )  __ _(_) __| |_   _ _ __| |
|  _ \ / _` | |/ _` | | | | '__| |
| |_) | (_| | | (_| | |_| | |  | |
|____/ \__,_|_|\__,_|\__,_|_|  |_|
""")
	main('inurl:login.action')
