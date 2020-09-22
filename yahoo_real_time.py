# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:28:25 2020

@author: shufe
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def yahoo_quote(ticker):
    url = 'https://finance.yahoo.com/quote/%s?p=HAL&.tsrc=fin-srch'%ticker
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    p = soup.find('div',attrs = {"My(6px) Pos(r) smartphone_Mt(6px)"})
    text = p.get_text()
    if '+' in text:
        price = float(text.split('+')[0])
    elif '-' in text:
        price = float(text.split('-')[0])
    else:
        price = float('.'.join(text.split(' ')[0].split('.')[:2]))
    t = p.get_text().split(' ')[4]
    today = datetime.now()
    t = datetime.strptime(str(today.date())+'_'+t,'%Y-%m-%d_%I:%M%p')
    return t, price

