from bs4 import BeautifulSoup
import urllib, os, time, re, sys

# 默认参数
url = 'http://m.sohu.com'
interval = 60
path = '/tmp/backup/'

# 获取参数
if __name__ == '__main__':
	for i in range(0, len(sys.argv)):
		if sys.argv[i] == '-d' and i+1 < len(sys.argv):
			interval = sys.argv[i+1]
		elif sys.argv[i] == '-u' and i+1 < len(sys.argv):
			url = sys.argv[i+1]
		elif sys.argv[i] == '-o' and i+1 < len(sys.argv):
			path = sys.argv[i+1]

def save_file(url, path, dir_name, text):
	name = url.split('/')[-1]
	if not os.path.exists(path+'/'+dir_name+'/'):
		os.makedirs(path+'/'+dir_name+'/')
	urllib.urlretrieve(url , path+'/'+dir_name+'/'+name)
	return text.replace(url, dir_name+'/'+name)

# 读取并且存储图片，然后修改html
def save_imgs(soup, path, now, text):
	imgs = soup.find_all('img')
	data = []
	for item in imgs:
	  # 当存在original属性的时候图片是通过js加载的，直接保存到本地加载时会出错，这时需要把src替换掉
		if item.has_attr('original') and item['original'] not in data:
			name = item['original'].split('/')[-1]
			s = str(item).replace(item['src'], 'images/'+name)
			s = s.replace('original="'+item['original']+'"', '')
			if item.has_attr('data-webp') and item['data-webp'] == '1':
				s = s.replace('data-webp="1"', '')
			text = text.replace(str(item), s)
			if not os.path.exists(path+now+'/images/'):
				os.makedirs(path+now+'/images/')
			urllib.urlretrieve(url , path+now+'/images/'+name)
		if item.has_attr('src') and item['src'] not in data:
			text = save_file(item['src'], path+now, 'images', text)
	return text

def save_css(soup, path, now, text):
	css = soup.find_all('link', type='text/css')
	data = []
	for item in css:
		if item.has_attr('href') and item['href'] not in data:
			text = save_file(item['href'], path+now, 'css', text)
	return text

def save_js(soup, path, now, text):
	js = soup.find_all('script', type='text/javascript')	
	data = []
	for item in js:
		if item.has_attr('src') and item['src'] not in data:
			text = save_file(item['src'], path+now, 'js', text)
	return text

temp = True
while temp:
	html = urllib.urlopen(url)
	text = html.read()
	soup = BeautifulSoup(text)
	
  # 获取当前时间
	now = str(time.strftime('%Y%m%d%H%M',time.localtime(time.time())))

	text = save_imgs(soup, path, now, text)
	text = save_css(soup, path, now, text)
	text = save_js(soup, path, now, text)

	fp = open(path+now+"/index.html", 'w')
	fp.write(text)
	fp.close() 

	time.sleep(float(interval))
