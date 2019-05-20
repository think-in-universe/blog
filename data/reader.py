# -*- coding:utf-8 -*-

import io
import os
import re
import traceback
import pandas as pd

from steem.collector import get_posts
from steem.comment import SteemComment
from steem.settings import STEEM_HOST, settings

from utils.system.date import get_cn_time_str, in_recent_days
from utils.csv.csv_writer import write_json_array_to_csv
from utils.network.mail import Mail
from utils.logging.logger import logger


class SteemReader:

    def __init__(self, tag="cn", account=None, keyword=None, limit=None, days=None):
        self.posts = []
        self.attributes = [u'title', u'pending_payout_value',
            u'author', u'net_votes', u'created', u'url'
            #, u'body', u'community', u'category', u'authorperm',
        ]
        self.tag = tag
        if self.tag and len(tag.split(",")) > 0:
            self.tags = tag.split(",")
        else:
            self.tags = None
        self.account = account
        self.keyword = keyword
        self.limit = int(limit) if limit else None
        self.days = float(days) if days else None

        first_tag = self.tags[0] if self.tags else self.tag
        self.folder = ".items/{}".format(first_tag or "by_account")
        self.filename = None

    def is_recent(self, post, days):
        return in_recent_days(post['created'], days)

    def is_qualified(self, post):
        return True

    def subset(self, item, keys=[]):
        for key in list(item.keys()):
            if key not in keys:
                del item[key]
        if u'url' in item:
            item[u'url'] = STEEM_HOST + item[u'url']
        else:
            if settings.is_debug():
                logger.info("the item may have issue: {} with keys: {}".format(item, list(item.keys())))
        return item

    def _merge_posts(self, posts1, posts2, attr):
        urls = [post[attr] for post in posts1]
        for post in posts2:
            if not post[attr] in urls:
                posts1.append(post)
        return posts1

    def _read_posts(self):
        print ("fetching posts...")
        if self.tags and len(self.tags) > 0:
            posts = []
            for t in self.tags:
                posts_t = get_posts(tag=t, account=self.account, keyword=self.keyword, limit=self.limit, days=self.days)
                posts = self._merge_posts(posts, posts_t, 'url')
            return posts
        else:
            return get_posts(tag=self.tag, account=self.account, keyword=self.keyword, limit=self.limit, days=self.days)

    def get_latest_posts(self):
        posts = self._read_posts()
        self.posts = [post for post in posts if self.is_qualified(post)]
        print ("{} posts to review".format(len(self.posts)))
        return self.posts

    def _get_time_str(self):
        str_time, timestamp = get_cn_time_str()
        return str_time

    def get_name(self):
        first_tag = self.tags[0] if self.tags else self.tag
        name = first_tag or "user-" + self.account

        return "{}-{}".format(name, self._get_time_str())

    def get_filename(self):
        if self.filename is not None:
            return self.filename

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self.filename = "{}/{}.csv".format(self.folder, self.get_name())
        return self.filename

    def write_posts(self):
        filename = self.get_filename()
        print ("writing posts to CSV:", filename)
        posts = [self.subset(post, self.attributes) for post in self.posts]
        write_json_array_to_csv(posts, filename)
        return filename

    def send_notification(self):
        title = self.get_name()

        count = len(self.posts)
        if count > 0:
            title = title + " | {} new posts".format(count)
            body = self.csv_to_html(filename=self.get_filename())
        else:
            title = title + " | no new posts"
            body = "no new posts"

        print ("sending notification...")
        mail_server = Mail()
        success = mail_server.send(title, body)
        if success:
            print("success")
        else:
            print("failure")

    def csv_to_html(self, df=None, filename=None):
        if df is None:
            if filename is not None:
                df = pd.read_csv(filename)
            else:
                return ""

        with pd.option_context('display.max_colwidth', -1):
            output = df.to_html(index=False, justify="left", float_format='%.3f')
        return output

