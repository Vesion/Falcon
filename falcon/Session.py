#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

import requests
import json
import ConfigParser

class Session():
    """ 
    Fundamental class instantiated to initiate and maintain an HTTP session.
    APIs: login, logout, get ,post
    Wrappers: set/get[Header], set/get[Cookie], set/get[Config]
    """
    
    _HOST_ = "http://www.zhihu.com"

    def __init__(self):
        self.__session = requests.session()
        self.__config = self.getConfig()

    def setHeader(self, headers):
        for key, value in headers.items():
            self.__session.headers[key] = value

    def getHeader(self):
        return self.__session.headers

    def setCookie(self, cookies):
        for key, value in cookies.items():
            self.__session.cookies[key] = value

    def getCookie(self):
        return self.__session.cookies

    def setConfig(self, section, options):
        for key, value in options.items():
            self.__config.set(section, key, value)
        with open('config.ini', 'wb') as configfile:
            self.__config.write(configfile)

    def getConfig(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.ini')
        return cf
    
    def get(self, url, params = {}):
        return self.__session.get(url, params = params)

    def post(self, url, data = {}):
        return self.__session.post(url, data = data)

    def login(self):
        self.setHeader(dict(self.__config.items('header')))

        try:
            rsp = self.post(Session._HOST_ + "/login/email", 
                        data = {
                            'email'    : self.__config.get('info', 'email'),
                            'password' : self.__config.get('info', 'password'),
                            '_xsrf'    : self.__config.get('cookie', '_xsrf')
                        })
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                if not rsp.json()['errcode']:
                    print "Login successfully."
                    self.setConfig('cookie', self.__session.cookies)
                else:
                    print "Login failed with response errcode: {0}".format(rsp.json()['errcode'])
                return True
            else:
                print "Login failed: {0}".format(rsp.status_code)
        return False

    def logout(self):
        try:
            rsp = self.get(Session._HOST_ + "/logout")
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                print "Logout successfully."
                self.setConfig('cookie', self.__session.cookies)
                return True
            else:
                print "Logout failed : {0}".format(rsp.status_code)
        return False



if __name__ == "__main__":
    s = Session()
    s.login()
    s.logout()
    
