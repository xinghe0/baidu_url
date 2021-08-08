
# @Time : 2021-08-07 20:54
# @File : bs.py
# @Author : XingHe
# @Software: PyCharm

from bs4 import BeautifulSoup as bs
import requests
import time

def main(keyword):
	for i in range(1,380,10):
		url = "https://www.baidu.com/s?wd=" + keyword + "&pn=" + str(i)
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
		try:
			print("**----开始抓取网站url----***" + '\n')
			r = requests.get(url=url,headers=headers,timeout=5)
			#print(r.text)

			soup = bs(r.text,'lxml')
			urls = soup.find_all(name='a',attrs={'target':'_blank','style':'text-decoration:none;position:relative;'})
			#print(urls)

			for url in urls:
				#print(url['href'])
				need_url = requests.get(url=url['href'])
				print(need_url.url)
				if need_url.status_code==200 :
					with open(r'ip.txt','a+') as f :
						f.write(need_url.url + '\n')
						f.close
						time.sleep(1)
		except Exception as e:
			pass


if __name__ == '__main__':
	main('inurl:index.action')