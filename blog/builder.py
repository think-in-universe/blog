# -*- coding:utf-8 -*-

import os

from steem.comment import SteemComment
from steem.settings import settings, STEEM_HOST
from data.reader import SteemReader
from utils.logging.logger import logger
from blog.message import get_message

BLOG_CONTENT_FOLDER = "./source/_posts"


class BlogBuilder(SteemReader):

    def __init__(self, account="steem-guides", days=None):
        SteemReader.__init__(self, account=account, days=days)
        self.attributes = [u'title', u'pending_payout_value',
            u'author', u'net_votes', u'created', u'url'
            # u'permlink', u'authorperm', u'body', u'community', u'category',
        ]
        self.author = account
        self.blog_folder = os.path.join(BLOG_CONTENT_FOLDER, self.author)
        if not os.path.exists(self.blog_folder):
            os.makedirs(self.blog_folder)

    def get_name(self):
        name = "blog"
        return "{}-{}-{}".format(name, self.author, self._get_time_str())

    def is_qualified(self, post):
        return True

    def _get_content_folder(self):
        return self.blog_folder

    def _write_content(self, post):
        folder = self._get_content_folder()
        c = SteemComment(comment=post)

        # retrieve necessary data from steem
        title = post.title.replace('"', '')
        body = post['body'].replace('<center>','').replace('</center>', '')
        date_str = post.json()["created"]
        date = date_str.replace('T', ' ')
        tags = "\n".join(["- {}".format(tag) for tag in c.get_tags()])
        category = c.get_tags()[0]

        # build content with template
        template = get_message("blog")
        content = template.format(title=title, date=date, tags=tags, category=category, body=body)

        # write into MD files
        filename = os.path.join(folder, "{}_{}.md".format(date_str.split('T')[0], post["permlink"]))
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("Download post [{}] into file {}".format(title, filename))


    def download(self):
        if len(self.posts) == 0:
            self.get_latest_posts()
        if len(self.posts) > 0:
            for post in self.posts:
                self._write_content(post)





