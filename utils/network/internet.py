# -*- coding:utf-8 -*-

from requests import get

def get_ip():
    try:
        r =  get('https://api.ipify.org')
        return r.text
    except:
        return "none"
