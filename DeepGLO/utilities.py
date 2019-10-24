import pandas as pd
import numpy as np
import datetime


def last_days(num=60, date=datetime.datetime(2018, 6, 20)):
    y = [str(date.year) + "%02d" % date.month + "%02d" % date.day]
    for i in range(1, num):
        d = date - datetime.timedelta(days=i)
        y = y + [str(d.year) + "%02d" % d.month + "%02d" % d.day]
    return y


def date_range(d1=datetime.datetime(2018, 3, 19), d2=datetime.datetime(2018, 6, 20)):
    td = d2 - d1
    ndays = td.days
    y = [str(d1.year) + "%02d" % d1.month + "%02d" % d1.day]
    for i in range(1, ndays + 1):
        d = d1 + datetime.timedelta(days=i)
        y = y + [str(d.year) + "%02d" % d.month + "%02d" % d.day]
    return y
