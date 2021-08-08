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
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Cookie': 'BIDUPSID=C9A11D6B97FA3D959272480C2993BF13; PSTM=1617093645; BAIDUID=C9A11D6B97FA3D9598517F3A46563EFB:SL=0:NR=10:FG=1; H_WISE_SIDS=107311_110085_114551_127969_131423_154214_161420_164075_165135_165936_166148_167538_167729_169308_170704_170817_170872_171235_171772_172316_172322_172386_172404_172452_172470_172491_172590_172680_172897_172998_173016_173032_173125_173126_173130_173203_173244_173251_173282_173414_173563_173575_173594_173609_173617_8000091_8000106_8000131_8000142_8000143; __yjs_duid=1_a836a7cc5f9563cf5d45e26124a32f021619697346419; sug=3; sugstore=0; ORIGIN=0; bdime=0; BD_UPN=12314753; BDSFRCVID_BFESS=EN0OJexroG0YTAJeP1MTMWUr7gKK0gOTDYLEOwXPsp3LGJLVgK9uEG0Pt_U-mEt-J8jwogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbkD_C-MfIvDqTrP-trf5DCShUFsthbrB2Q-XPoO3KJZShj_bq0aXtuI3noHt-biWbRM2MbgylRp8P3y0bb2DUA1y4vpKMP8bmTxoUJ2XMKVDq5mqfCWMR-ebPRiWPb9QgbP2pQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5P0hxry2Dr2aI52B5r_5TrjDnCr-j7TXUI82h5y05OkQg6Z0xthBCTYSU54jPJvyT8sXnORXx74QC6L3lI-0xKKSCbKbU4B5fL1Db3JyhLLamTJslFy2t3oepvoX-Jc3MkAX-jdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEtbkD_C-MfIvDqTrP-trf5DCShUFs2f3iB2Q-XPoO3KJZShj_bq0aXjFI3noHt-biWbRM2MbgylRp8P3y0bb2DUA1y4vpKMP8bmTxoUJ2XMKVDq5mqfCWMR-ebPRiWPb9QgbP2pQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQJUoP8pcN2b5oQT843-QZKl8DBGRu-M5-Jb3vOIJTXpOUWfAkXpJvQnJjt2JxaqRC5hkBfq5jDh3MBpQDhtoJexIO2jvy0hvcBn3cShnaXMjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNtDt60jfn3aQ5rtKRTffjrnhPF3Qf6QXP6-hnjy3bRk-pjF5xta8fbE3poKjP-UyN3MWh3RymJ42-39LPO2hpRjyxv4bUn-5toxJpOJXaILWl52HlFWj43vbURvX--g3-7PWU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCDBMIL43H; MCITY=-%3A; ab_sr=1.0.1_ZmZlYTA5YzdhODFhNDZmNjY4N2Q4N2E0MjJlMDA2MmE0ZjJlMjM3YWE5ZjIzZWQ5ODlkOTFjNzlkNjY1ZmRjOGQ1MjhkYzEyMzBiMWQwNzFjZTJlZTEyMTE2ZjBjODM1NTU5ZjVlMzI1MGY1NzlmNjQ0MzY3YjczZDZmZWVjNDViNTExNWZmYWM1YzMyMzg5YjRjMTcwMGVmNDVlMjQ1MQ==; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; delPer=0; PSINO=6; BAIDUID_BFESS=D22D6DC01C87DEF8B292F41FBBB518B7:FG=1; BDRCVFR[8XxVvliF3qY]=mk3SLVN4HKm; H_PS_645EC=b261VhB57HZewiMisUIZXNj5nONGZ8RTqzzocnPiHSQcbuU4z%2FZKgTW6jHLVxrsOeSiuJq%2FfGOC5; BA_HECTOR=8l25a1210185052l351ggvj720q'
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
