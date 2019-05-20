# -*- coding:utf-8 -*-

import os, time, random
from invoke import task

from steem.collector import get_posts
from steem.settings import settings


@task(help={
      'account': 'the name of the user to watch',
      'tag': 'the tag to filter the posts',
      'keyword': 'the keyword to filter the posts',
      'limit': 'the limit of posts to return',
      'days': "return the recent n days' posts",
      'debug': 'enable debug mode'
      })
def list_posts(ctx, account=None, tag=None, keyword=None, limit=None, days=None, debug=False):
    """ list the post by account, tag, keyword, etc. """

    if debug:
        settings.set_debug_mode()
    settings.set_steem_node()

    get_posts(account, tag, keyword, limit, days)

