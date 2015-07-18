# -*- coding: utf-8 -*-

import requests
import ConfigParser

class Session():
    """ 
    Basic class used to initiate and maintain a request session.
    NOTE:
        All of attrs are private for safe regarding.
    API: login, logout
    Wrapper: get, post, set/get[Header], set/get[Cookie]
    """
    
    _HOST_ = "http://www.zhihu.com"

    def __init__(self):
        self.__session = requests.session()

    def setHeader(self, **headers):
        for key, value in headers.items():
            self.__session.headers[key] = value

    def getHeader(self):
        return self.__session.headers

    def setCookie(self, **cookies):
        for key, value in cookies.items():
            self.__session.cookies[key] = value

    def getCookie(self):
        return self.__session.cookies

    def setConfig(self, section, **options): # for debug
        cf = self.getConfig()
        for key, value in options.items():
            cf.set(section, key, value)
        with open('config.ini', 'wb') as configfile:
            cf.write(configfile)

    def getConfig(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.ini')
        return cf
    
    def get(self, url, params = {}):
        return self.__session.get(url, params = params)

    def post(self, url, data = {}):
        return self.__session.post(url, data = data)

    def login(self):
        self.setHeader(**dict(self.getConfig().items('header')))
        user_info = dict(self.getConfig().items('info'))
        user_info['_xsrf'] = self.getCookie()['_xsrf']

        try:
            rsp = self.post(Session._HOST_ + "/login/email", 
                        data = user_info)
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                print "Login successfully."
                self.setConfig('cookie', **self.__session.cookies)
                return True
            else:
                print "Login error: " + str(rsp.status_code)
        return False

    def logout(self):
        try:
            rsp = self.get(Session._HOST_ + "/logout")
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                print "Log out successfully."
                self.setConfig('cookie', **self.__session.cookies)
                return True
            else:
                print "Log out failed : {0}".format(rsp.status_code)
        return False
        
if __name__ == "__main__":
    s = Session()
    s.login()
    
