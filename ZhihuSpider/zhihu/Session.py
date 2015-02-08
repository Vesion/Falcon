# -*- coding: utf-8 -*-

import requests
import json
import ConfigParser

class Session():
    """ Basic class used to initiate and maintain a request session """
    
    def __init__(self):
        self.__session = requests.session()
        self.__info = {}
        #self.HasLogedIn = False

    def __parseConfig(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.ini')
        self.__info = dict(cf.items('info'))
        self.__session.headers = dict(cf.items('header'))

    def updateConfig(self): # for debug
        cf = ConfigParser.ConfigParser()
        cf.read('config.ini')
        for c in self.__session.cookies.items():
            cf.set('cookies', c[0], c[1])
        with open('config.ini', 'wb') as configfile:
            cf.write(configfile)

    def login(self):
        self.__parseConfig()
        try:
            rsp = self.__session.post("http://www.zhihu.com/login", 
                                      data = self.__info)
        except requests.exceptions.RequestException as e:
            print e.message()
            sys.exit(0)
        else:
            if rsp.status_code == requests.codes.ok:# log in successfully
                # print self.__session.cookies
                #self.HasLogedIn = True
                print "Log in successfully."
                self.updateConfig() # update cookies into config
            else:
                print r.json()['msg']

    def get(self, url):
        return self.__session.get(url)
        
if __name__ == "__main__":
    s = Session()
    s.login()