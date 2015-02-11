# -*- coding: utf-8 -*-

import requests
import json
import ConfigParser

class Session():
    """ 
    Basic class used to initiate and maintain a request session.
    NOTE:
        All of attrs are private for safe regarding.
    API: login, logout
        Wrapper: get, post, setHeader
    """
    
    _HOST_ = "http://www.zhihu.com"

    def __init__(self):
        self.__session = requests.session()
        self.setHeader(**dict(self.getConfig().items('header')))

    def getConfig(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.ini')
        return cf
    
    def setHeader(self, **headers):
        for key, value in headers.items():
            self.__session.headers[key] = value

    def setConfig(self, section, **options): # for debug
        cf = self.getConfig()
        for key, value in options.items():
            cf.set(section, key, value)
        with open('config.ini', 'wb') as configfile:
            cf.write(configfile)

    def get(self, url):
        return self.__session.get(url)

    def post(self, url, data):
        return self.__session.post(url, data)

    def login(self):
        user_info = dict(self.getConfig().items('info'))
        try:
            rsp = self.post(Session._HOST_ + "/login", 
                        data = user_info)
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:# log in successfully
                print "Log in successfully."
                self.setConfig('cookie', **self.__session.cookies) # update cookies into config
                return True
            else:
                print r.json()['msg']
        return False

    def logout(self):
        try:
            rsp = self.get(Session._HOST_ + "/logout")
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                print "Log out successfully."
                self.setConfig('cookie', **self.__session.cookies) # update cookies into config
                return True
            else:
                print "Log out failed : {0}".format(rsp.status_code)
        return False
        
if __name__ == "__main__":
    s = Session()
    s.login()