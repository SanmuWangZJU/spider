import requests
from lxml import etree
import time
from urllib import request
from PIL import Image
import http.cookiejar as cookielib
import matplotlib.pyplot as plt
session=requests.session()

#get coolies
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("Cookie can't load")


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#     "Host": "www.zhihu.com",
#     "Referer": "https://www.zhihu.com/",
# }
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
# agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}

login_url = 'https://www.zhihu.com/#signin'
element = session.get(login_url, headers=headers)
dom = etree.HTML(element.content.decode('utf-8'))#
_xsrf = dom.xpath('//input/@value')[0]
captcha_lang = dom.xpath('/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div[3]/@data-type')

def getxsrf():
	'''get _xsrf for zhihu login
	'''
	# login_url = 'http://www.zhihu.com/#signin'
	login_url = 'https://www.zhihu.com/#signin'
	element = session.get(login_url, headers=headers)
	dom = etree.HTML(element.content.decode('utf-8'))#
	return dom.xpath('//input/@value')[0]

def getcaptcha_cn():
	'''used in getcaptcha() to get captcha when lang is cn
	'''
	image = plt.imread('captcha.gif')
	plt.imshow(image)
	# cap_num=int(input('输入倒立文字个数\n'))
	pos=plt.ginput(0,0)

	def change(l):
		k=[]
		for i in l:
			i=list(i)
			i[0]=i[0]//2+0.375
			i[1]=int(i[1])//2
			k.append(i)
		return k

	# pos = [(72.887096774193552, 48.338709677419359), (149.5, 48.338709677419359)]
	input_points = change(pos)
	return input_points


def getcaptcha():
	'''获取验证码
	'''
	t = str(int(time.time() * 1000))
	captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login'
	captcha_cn_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login&lang=cn'
	
	if captcha_lang == 'en':
		captcha_url = captcha_url
		#使用urllib中的request的urlretrieve方法保存验证码图片到本地
		request.urlretrieve(captcha_url,'E:\myProgram\captcha.gif')
		im = Image.open('E:\myProgram\captcha.gif')
		im.show()
		im.close()
		captcha = input('输入验证码信息\n')
		return captcha
	else:
		captcha_url = captcha_cn_url
		request.urlretrieve(captcha_url,'E:\myProgram\captcha.gif')
		input_points = getcaptcha_cn()
		
		captcha={}
		captcha["img_size"] = [200,44]
		captcha["input_points"] = input_points
		captcha_type = 'cn'
		return captcha,captcha_type
	

def login():
	post_url = 'http://www.zhihu.com/login/phone_num'
	postdata = {
	'_xsrf': getxsrf(),
	'password':'WangSenFirst01',
	# 'captcha':getcaptcha(),
	'remember_me': 'true',
	'phone_num':'15267007868',
	}
	
	try:
		# 不需要验证码直接登录
		login_page = session.post(post_url, data = postdata, headers = headers)
		login_code = login_page.text

		print('login_code is',login_page.status_code)
		print(login_page.text)
	except:
		# 需要输入验证码
		captcha,captcha_type = getcaptcha()
		postdata['captcha']=captcha
		postdata['captcha_type']=captcha_type
		login_page = session.post(post_url,data = postdata,headers = headers)
		login_code = eval(login_page.text)
		print(login_code['msg'])
	
	# data['captcha']=getcaptcha()
	# login_page = session.post(post_url,data = data,headers = headers)
	# login_code = login_page.text
	# print(login_code['msg'])

	session.cookies.save()


def islogedin():
	# url = "https://www.zhihu.com/settings/profile"
	url = 'https://www.zhihu.com/settings/profile'
	# url = "https://www.zhihu.com"
	st= session.get(url,headers = headers,allow_redirects=False)
	login_code  = st.status_code
	print('login_code in islogedin() is {0}'.format(login_code))
	
	# print(st.text)
	if login_code==200:
		print(st.text)
		return True
	else:
		print('Flase')
		return False
def getpeple():
    followees_url = 'https://www.zhihu.com/people/feng-ren-38-7/following'
    followees_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        # 'Referer': 'https://www.zhihu.com/people/feng-ren-38-7/following',
        # 'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate, sdch, br'
    }
    myfollowees = session.get(followees_url, headers=followees_headers)
    print(myfollowees.status_code)
    print(myfollowees.text)
# if __name__ == '__main__':
# islogedin()
# 	login()
# getpeple()
	# if islogedin():
	# 	print('已经登录')
	# else:
	# 	login()

captcha,captcha_type = getcaptcha()
print(captcha_type,captcha)