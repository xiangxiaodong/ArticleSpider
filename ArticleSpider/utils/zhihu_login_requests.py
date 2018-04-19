# -*- coding: utf-8 -*-
__author__ = 'maxpower'

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib
    
    
import re
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

header = {
    'HOST':'www.zhihu.com',
    'Referer':'https://www.zhihu.com',
    'User-Agent':agent
}
def get_xsrf():
    response = requests.get('https://www.zhihu.com',headers = header)
    # print(response.text)#查看requests返回的值是否正
    match_obj = re.match('.*name="_xsrf" value="(.*?)"',response.text)
    if match_obj:
        print(match_obj.group(1))
    return ''

def zhihu_login(account,password):
    if re.match('^1\d{10}',account):
        print('手机号码登陆')
        post_url = 'https://wwww.zhihu.com/login/phone_num'
        post_data = {
            '_xsrf':get_xsrf,
            'phone_num':account,
            'password':password
        }
    
get_xsrf()