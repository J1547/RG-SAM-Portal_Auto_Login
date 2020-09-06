# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from html import unescape
from time import sleep
from os import system

class Browser:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options = chrome_options)
    username = ''
    password = ''
    url = ''
    service = ''
    servicelist = ['移动','电信','联通','校内网']
    file = ''
    actions = webdriver.ActionChains(browser)
        
    def get(self):
        self.browser.get(self.url)
        
    def islogin(self):
        return self.browser.current_url.find('success') != -1
    
    def getaccount(self):
        tag = True
        try:
            self.file = open(r'account.txt','r')
        except:
            tag = False
        
        content = self.file.read() if tag else ''
        if tag and content != '':
            s = e = 1
            e = content.find('|',s)
            self.url = content[s:e]
            s = e + 1
            e = content.find('|',s)
            self.username = content[s:e]
            s = e + 1
            e = content.find('|',s)
            self.password = content[s:e]
            s = e + 1
            e = content.find('|',s)
            self.service = content[s:e]
            self.file.close()
        else:
            self.file =open (r'account.txt','w')
            self.url = input('登陆网址：')
            self.username = input('账号：')
            self.password = input('密码：')
            self.service = input('运营商：')
            info = '|{uu}|{u}|{p}|{s}|'.format(uu = self.url,u = self.username,p = self.password,s = self.service)
            self.file.write(info)
            print('[+] 账号信息保存在当前目录下的account.txt，账号信息错误请删除account.txt后再启动本程序！')
            self.file.close()
    
    def inputinfo(self):
        u = self.browser.find_element_by_id('username')
        p = self.browser.find_element_by_id('pwd')
        p_tip = self.browser.find_element_by_id('pwd_tip')
        # 输入账号
        u.send_keys(self.username)
        # 选择运营商
        self.browser.find_element_by_id('defaultService').click()
        self.browser.find_element_by_id('_service_' + str(self.servicelist.index(self.service))).click()
        # 输入密码
        p_tip.click()
        p.send_keys(self.password)
        
    def submit(self):
        # 提交表单
        self.browser.execute_script("this.className='loginButtonHKClicked_1';doauthen();")

    def geterrmsg(self):
        errormsg = self.browser.find_element_by_id('errorInfo_center').get_attribute('val')
        return unescape(errormsg)


if __name__ == '__main__':
    b = Browser()
    b.getaccount()
    b.get()
    if not b.islogin():
        
        b.inputinfo()
        b.submit()
        sleep(1)
        if not b.islogin():
            print('[+] 登陆失败！' + b.geterrmsg())
            input('[+] 退出')
        else:
            print('[+] 登陆成功！')
    else:
        print('[+] 已登录！')
    b.browser.close()
    system('exit')
