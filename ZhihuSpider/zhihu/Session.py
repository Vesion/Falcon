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
        Wrapper: get, post
    """
    
    def __init__(self):
        self.__session = requests.session()
        self.__info = {}

        self.__cf = ConfigParser.ConfigParser()
        self.__cf.read('config.ini')

    def __parseConfig(self):
        self.__info = dict(self.__cf.items('info'))
        self.__session.headers = dict(self.__cf.items('header'))

    def updateConfig(self): # for debug
        for ckey, cvalue in self.__session.cookies.items():
            self.__cf.set('cookies', ckey, cvalue)
        with open('config.ini', 'wb') as configfile:
            self.__cf.write(configfile)

    def login(self):
        self.__parseConfig()
        try:
            rsp = self.post("http://www.zhihu.com/login", 
                        data = self.__info)
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:# log in successfully
                print "Log in successfully."
                self.updateConfig() # update cookies into config
                return True
            else:
                print r.json()['msg']
        return False

    def logout(self):
        try:
            rsp = self.get("http://www.zhihu.com/logout")
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                print "Log out successfully."
                self.updateConfig() # update cookies into config
                return True
            else:
                print "Log out failed : {0}".format(rsp.status_code)
        return False

    def get(self, url):
        return self.__session.get(url)

    def post(self, url, data):
        return self.__session.post(url, data)
        
if __name__ == "__main__":
    s = Session()
    s.login()