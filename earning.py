# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:14:27 2020

@author: shufe
"""

from datetime import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import pandas as pd


date_from = datetime.datetime.strptime(
    'Jan 3 2020  10:00AM', '%b %d %Y %I:%M%p')
date_to = datetime.datetime.strptime(
    'May 27 2020  1:00PM', '%b %d %Y %I:%M%p')
yec = YahooEarningsCalendar()
print(yec.earnings_on(date_from))
print(yec.earnings_between(date_from, date_to))

a = yec.earnings_between(date_from, date_to)
df = pd.DataFrame(a)
df.index = df['startdatetime'].map(lambda x: datetime.datetime.strptime(x.split('T')[0], '%Y-%m-%d'))
df.to_csv('earning_info.csv')