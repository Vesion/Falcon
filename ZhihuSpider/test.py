# -*- coding: utf-8 -*-

import requests
import json
import ConfigParser

class Session():
    """ Used to initiate and maintain a request session """
    
    def __init__(self):
        self.__session = requests.session()
        self.__info = {}
        self.__header = {}
        self.HasLogedIn = False

    def __parseConfig(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.ini')
        self.__info = cf.items('info')
        self.__header = cf.items('header')
        self.__session.cookies = cf.items('cookies')

    def login(self):
        self.__parseConfig()
        try:
            print self.__header
            rsp = self.__session.post("http://www.zhihu.com/login", 
                                      data = self.__info, 
                                      headers = self.__header)
        except requests.exceptions.RequestException as e:
            print e.message()
            sys.exit(0)
        else:
            if rsp.status_code == requests.codes.ok: # log in successfully
                # print self.__session.cookies
                self.HasLogedIn = True
            else:
                print r.json()['msg']

    def get(self, url):
        return self.__session.get(url)
        
if __name__ == "__main__":
    s = Session()
    s.login()