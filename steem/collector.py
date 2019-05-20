# -*- coding:utf-8 -*-

import pandas as pd
import traceback
import json

from beem.account import Account
from beem.comment import Comment
from beem.discussions import Query, Discussions_by_created

from steem.comment import SteemComment
from steem.settings import settings
from utils.logging.logger import logger
from utils.system.date import in_recent_days

LIMIT_THRESHOLD = 100


def get_posts(account=None, tag=None, keyword=None, limit=None, days=None):
    if account:
        return SteemPostsByAccount(account=account, tag=tag, keyword=keyword, limit=limit, days=days).read_posts()
    elif tag and not account:
        return SteemPostsByTag(tag=tag, keyword=keyword, limit=limit, days=days).read_posts()

def get_comments(account=None, receiver=None, limit=None, days=None):
    return SteemCommentsByAccount(account=account, receiver=receiver, limit=limit, days=days).read_comments()

def in_recent_n_days(post, n):
    return in_recent_days(post['created'], n)


class SteemPostsByAccount:

    def __init__(self, account, tag=None, keyword=None, limit=None, days=None):
        self.username = account
        self.account = Account(account)
        self.tag = tag
        self.keyword = keyword # and keyword.decode('utf-8')
        self.limit = int(limit) if limit else None
        self.days = float(days) if days else None
        self.total = None

    def get_total(self):
        if self.total is None:
            self.total = len(self.account.get_blog()) # not correct
        return self.total

    def read_posts(self, start=0):
        c_list = {}
        posts = []

        if self.limit:
            blogs = self.account.get_blog(start_entry_id=start, limit=self.limit)
        elif self.days:
            blogs = self.account.blog_history(start=start, limit=None, reblogs=False)
        else:
            blogs = map(Comment, self.account.history(only_ops=["comment"]))

        days_done = False
        for c in blogs:
            if c.permlink in c_list:
                continue
            sc = SteemComment(comment=c)
            if not sc.is_comment() and c.author == self.username:
                tags = sc.get_tags()
                if self.tag is None or self.tag in tags:
                    if self.keyword is None or self.keyword in c.title:
                        days_done = self.days is not None and not in_recent_n_days(c, self.days)
                        if days_done:
                            break
                        else:
                            c = sc.refresh()
                            sc.log()
                            c_list[c.permlink] = 1
                            posts.append(c)

        print ('{} posts are fetched'.format(len(posts)))
        return posts


class SteemPostsByTag:

    def __init__(self, tag, keyword=None, limit=None, days=None):
        self.tag = tag
        self.keyword = keyword #and keyword.decode('utf-8')
        self.limit = int(limit) if limit else None
        self.days = float(days) if days else None

    def read_posts(self):
        posts = []
        number_per_request = LIMIT_THRESHOLD - 1
        index = 0
        days_done = False

        while True:
            limit = min(self.limit - len(posts), number_per_request) if self.limit else number_per_request
            if index > 0:
                limit = limit + 1
                last_post = new_posts[-1]
            else:
                last_post = None

            res = self.read_posts_with_limit(limit, last_post)
            new_posts = res["posts"]
            days_done = res["days_done"]

            # remove the head because it's the end of last request
            if index > 0:
                new_posts.pop(0)
            if len(new_posts) > 0:
                posts.extend(new_posts)
            else:
                break

            # if time exceeds, stop
            if days_done:
                if settings.is_debug():
                    print ('{} posts in {} days are fetched'.format(len(posts), self.days))
                break

            # if limit exceeds, stop
            index += 1
            if self.limit and self.limit <= len(posts):
                if settings.is_debug():
                    print ('{} posts of {} target posts are fetched'.format(len(posts), self.limit))
                break

        print ('{} posts are fetched'.format(len(posts)))
        return posts

    def read_posts_with_limit(self, limit, last_post=None):
        posts = []

        if last_post:
            q = Query(limit=limit, tag=self.tag,
                start_author=last_post.author,
                start_permlink=last_post.permlink
                # before_date=str(last_post['created'])
                )
        else:
            q = Query(limit=limit, tag=self.tag)

        blogs = Discussions_by_created(q)
        logger.info ('reading posts: {}'.format(len(blogs)))

        c_list = {}
        days_done = False
        for c in blogs:
            if c.permlink in c_list:
                continue
            if not c.is_comment():
                if self.keyword is None or self.keyword in c.title:
                    days_done = self.days is not None and not in_recent_n_days(c, self.days)
                    if days_done:
                        break
                    else:
                        SteemComment(comment=c).log()
                        c_list[c.permlink] = 1
                        posts.append(c)
        return {
            "posts": posts,
            "days_done": days_done
        }



class SteemCommentsByAccount:

    def __init__(self, account, receiver=None, limit=None, days=None):
        self.username = account
        self.account = Account(account)
        self.receiver = str(receiver) if receiver else None
        self.limit = int(limit) if limit else None
        self.days = float(days) if days else None
        self.total = None

    def read_comments(self):
        c_list = {}
        comments = []

        comment_history = self.account.comment_history(limit=self.limit)

        days_done = False
        for c in comment_history:
            if c.permlink in c_list:
                continue
            if c.is_comment() and c.author == self.username:
                sc = SteemComment(comment=c)
                days_done = self.days is not None and not in_recent_n_days(c, self.days)
                if days_done:
                    break
                else:
                    if self.receiver is None or len(self.receiver) == 0 \
                        or c.parent_author == self.receiver:
                        c = sc.refresh()
                        sc.log()
                        c_list[c.permlink] = 1
                        comments.append(c)

        print ('{} comments are fetched'.format(len(comments)))
        return comments

