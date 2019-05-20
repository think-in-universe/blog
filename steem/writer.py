# -*- coding:utf-8 -*-

from steem.settings import settings
from utils.logging.logger import logger

class Writer:

    def __init__(self, author):
        self.steem = settings.get_steem_node()
        self.author = author

    def post(self, title, body, tags, self_vote=False):
        self.steem.post(title, body, author=self.author, tags=tags, self_vote=self_vote)
        logger.info("Authored the post [{}] successfully".format(title))

    def reply(self, post, body):
        if post:
            post.reply(body, title='', author=self.author)
            logger.info("Replied to [{}] successfully".format(post.title))
