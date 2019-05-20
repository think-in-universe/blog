# -*- coding:utf-8 -*-

import os, time, random
from invoke import task

from steem.settings import settings
from blog.builder import BlogBuilder


@task(help={
      'account': 'the account of the blog to download',
      'days': 'the posts in recent days to fetch',
      'debug': 'enable the debug mode'
      })
def download(ctx, account="robertyan", days=None, debug=False):
    """ download the posts by the account """

    if debug:
      settings.set_debug_mode()

    settings.set_steem_node()

    builder = BlogBuilder(account=account, days=days)
    builder.download()


@task(help={
      })
def test(ctx):
    """ test the generation in local environment """

    os.system("hexo generate")
    os.system("hexo server")


@task(help={
      })
def deploy(ctx):
    """ deploy the hexo results to web server """

    os.system("hexo deploy --generate")

