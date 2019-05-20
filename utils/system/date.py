# -*- coding:utf-8 -*-

import time
from datetime import datetime, timedelta
import pytz


def utc_now():
    return datetime.now(pytz.utc)

def in_recent_days(date, days):
    return date > days_ago(days)

def days_ago(days):
    return utc_now() - timedelta(days=days)

def from_then(date):
    return utc_now() - date

def get_cn_time_str():
    # get timezone
    tz = pytz.timezone(pytz.country_timezones('cn')[0])
    str_time = datetime.now(tz).strftime('%Y-%m-%d')  # '%Y-%m-%d_(%H_%M_%S)'
    # get timestamp
    timestamp = int(1000 * time.time())

    return str_time, timestamp
