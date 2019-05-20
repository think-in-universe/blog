# -*- coding:utf-8 -*-

from utils.logging.logger import logger


class Voter:

    def __init__(self, author):
        self.author = author

    def upvote(self, post, weight=100):
        if post:
            post.upvote(weight=weight, voter=self.author)
            logger.info("Voted to [{}] successfully".format(post.title))

