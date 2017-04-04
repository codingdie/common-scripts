# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
import json
import codecs
import os
import cookielib

from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding('utf8')
username="547912355@qq.com"
password="xp19960326"


login_host='http://www.jiyue.com/login'
duty_host='http://www.jiyue.com/duty'

cookie = cookielib.MozillaCookieJar('jiyueshenshecookie.txt')
if os.path.exists('jiyueshenshecookie.txt'):cookie.load('jiyueshenshecookie.txt', ignore_discard=True, ignore_expires=True)


handler=urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
user_agent = 'fake-clien'

def get(url):
    global opener
    try:
        request = urllib2.Request(url)
        request.add_header('user-agent',user_agent)
        result=  opener.open(request)
    except urllib2.URLError, e:
        print e.reason
    html= result.read()
    cookie.save(ignore_discard=True, ignore_expires=True)
    return html;
def post(url,data):
    global opener
    try:
        request = urllib2.Request(url,urllib.urlencode(data))
        request.add_header('user-agent',user_agent)
        result=  opener.open(request)
    except urllib2.URLError, e:
        print e.reason
    html= result.read()
    cookie.save(ignore_discard=True, ignore_expires=True)
    return html
def checkLogin():
    global opener
    try:
        request = urllib2.Request(duty_host)
        request.add_header('user-agent',user_agent)
        result=  opener.open(request)
    except urllib2.URLError, e:
        print e.reason
    if result.geturl()==duty_host:
        return True
    else:
        return False

def login(u,passw):
    dic={}
    print '获取登陆参数'
    p=pq(get(login_host))
    form_id= p("#form_id").attr('value')
    timestamp= p("#timestamp").attr('value')
    dic["username-"+form_id]=u
    dic["user_password-"+form_id]=passw
    dic["form_id"]=form_id
    dic["timestamp"]=timestamp
    print '获取登陆参数完毕，尝试登陆'
    post(login_host,dic)
    print '尝试登陆完毕，检测是否登陆成功'
    return checkLogin()

def checkAssign():
    p=pq( get('http://www.jiyue.com/duty'))
    if len(p("button.qiandao").text())>0:
        return False;
    return True;


def assign():
    print '检测是否已经签到'
    if checkAssign():
        print '今天已经签到'
    else:
        print '今天还没签到，开始获取签到参数'
        p=pq( get('http://www.jiyue.com/duty'))
        dic={}
        dic["_wpnonce"]=p("#_wpnonce").attr("value")
        dic["_wp_http_referer"]=p("#_wp_http_referer").attr("value")
        url=duty_host+p(".duty-panel-body form").attr('action');
        print url
        print '开始签到'
        post(url,dic)
        print '签到完成,检测是否成功'
        if checkAssign():print '签到成功'
        else:print '签到失败'

def run():
    print '检测是否登陆'
    if checkLogin():
        print '已登陆'
        assign()
    else:
        print '未登录,登陆中'
        if login(username,password):
            print '登陆成功'
            assign()
        else:
            print '登陆失败'
i=1
while True:
    try:
        print "第"+str(i)+"次循环"
        i=i+1
        run()
        sys.stdout.flush()
        time.sleep(300)
    except:
        print 'error'



