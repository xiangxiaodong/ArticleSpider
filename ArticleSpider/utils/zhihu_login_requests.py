# -*- coding: utf-8 -*-
__author__ = 'maxpower'

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()  # 代表某一次连接是实例化
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')

try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookies未能加载')
# mac端的chrome用户代理
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

header = {
    'HOST': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'User-Agent': agent
}


def is_login():
    # 通过个人中心页面返回的状态码来判断是否为登陆页面
    inbox_url = 'https://www.zhihu.com/inbox'
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True
    pass

def get_xsrf():
    response = session.get('https://www.zhihu.com', headers=header)
    # print(response.text)#查看requests返回的值是否正
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)
    else:
        return ''


def get_index():
    response = session.get('https://www.zhihu.com', headers=header)
    with open('index_page.html', 'wb') as f:
        f.write(response.text.encode('utf-8'))
    print("ok")


def zhihu_login(account, password):
    # 手机号码方式登陆
    if re.match('^1\d{10}', account):
        print('手机号码登陆')
        post_url = 'https://www.zhihu.com/signin'
        post_data = {
            # '_xsrf':get_xsrf(),
            '_xsrf': 'df65f759-addd-465f-894f-1b9da79c26b4',
            'username': account,
            'password': password
        }
    
    # 邮箱方式登陆
    else:
        if '@' in account:
            print('手机号码登陆')
            post_url = 'https://www.zhihu.com/signin'
            post_data = {
                # '_xsrf': get_xsrf(),
                '_xsrf': 'df65f759-addd-465f-894f-1b9da79c26b4',
                'username': account,
                'password': password
            }
            response_text = session.post(post_url, data=post_data, headers=header)
            session.cookies.save()
    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()


zhihu_login('17682310408', 'xxd102401')
# get_index()
# get_xsrf()
# is_login()
