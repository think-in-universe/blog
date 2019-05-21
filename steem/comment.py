# -*- coding:utf-8 -*-

import re
import html

from bs4 import BeautifulSoup
from markdown import markdown

from beem import Steem
from beem.comment import Comment
from beem.exceptions import ContentDoesNotExistsException

from steem.settings import STEEM_HOST
from utils.logging.logger import logger


REGEX_IMAGE_URL = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)\.(jpg|jpeg|png|gif|svg)"


class SteemComment:

    def __init__(self, comment=None, author_perm=None, url=None):
        self.comment = comment
        self.author_perm = author_perm
        self.url = url

    def get_author_perm(self):
        if self.author_perm is None:
            self.author_perm = "/".join(self.url.split("/")[-2:])
        return self.author_perm

    def get_comment(self):
        if self.comment is None:
            self.comment = Comment(self.get_author_perm())
        return self.comment

    def get_url(self):
        if self.url is None:
            if self.author_perm:
                self.url = u"{}/{}".format(STEEM_HOST, self.author_perm)
            else:
                c = self.get_comment()
                if c.authorperm:
                    self.url = u"{}/{}".format(STEEM_HOST, c.authorperm)
                else:
                    self.url = u"{}/@{}/{}".format(STEEM_HOST, c.author, c.permlink)

        return self.url

    def get_pic_url(self, regex=False):
        if regex:
            # follow markdown format
            m = re.search(r"!\[(.*)\]\((\S+)\)", self.get_comment().body)
            if m:
                pic_url = m.group(2)
                return pic_url

            # follow url format
            m = re.search(REGEX_IMAGE_URL, self.get_comment().body)
            if m:
                pic_url = m.group(0)
                return pic_url
        else:
            links = self.get_img_links()
            if links and len(links) > 0:
                return links[0]

        return None

    def get_text_body(self):
        """ Converts a markdown string to plaintext """

        # md -> html -> text since BeautifulSoup can extract text cleanly
        html = markdown(self.get_comment().body)

        # remove code snippets
        html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
        html = re.sub(r'<code>(.*?)</code >', ' ', html)

        # extract text
        soup = BeautifulSoup(html, "html.parser")
        text = ''.join(soup.findAll(text=True))

        text = re.sub(REGEX_IMAGE_URL, '', text)

        return text

    def _get_valid_link(self, url):
        url = url.strip()
        if url[-1] == ")":
            url = url[:-1]
        # unescape HTML chars
        return html.unescape(url)

    def _is_img_link(self, url):
        m = re.match(REGEX_IMAGE_URL, url)
        return m is not None

    def get_links(self, regex=True):
        body = self.get_comment().body

        if regex:
            # text = re.sub('<[^<]+?>', ' ', str(self.text))
            links = re.findall(URL_REGEX, body)
        else:
            # md -> html -> text since BeautifulSoup can extract text cleanly
            html = markdown(body)
            # extract links
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.findAll("a")
            links = [tag.get("href") for tag in tags]

        if len(links) > 0:
            links = [self._get_valid_link(link) for link in links if link is not None]

        return links or []

    def get_img_links(self):
        body = self.get_comment().body

        # md -> html -> text since BeautifulSoup can extract text cleanly
        html = markdown(body)
        # extract links
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.findAll("img")
        links = [tag.get("src") for tag in tags]

        if len(links) > 0:
            links = [self._get_valid_link(link) for link in links if link is not None]

        return links or []

    def get_tags(self):
        c = self.get_comment()
        if c.json_metadata and 'tags' in c.json_metadata:
            return c.json_metadata['tags']
        else:
            self.refresh()
            c = self.get_comment()
            if c.json_metadata and 'tags' in c.json_metadata:
                return c.json_metadata['tags']
        return []

    def has_tag(self, tag):
        return tag in self.get_tags()

    def has_tags(self, tags):
        if not tags or len(tags) == 0:
            return False
        for tag in tags:
            if self.has_tag(tag):
                return True
        return False

    def refresh(self):
        c = self.get_comment()
        try:
            c.refresh()
        except ContentDoesNotExistsException:
            logger.info("failed when refresh {}".format(self.get_url()))
            return None

        return c

    def log(self):
        c = self.get_comment()
        logger.info("@%s | %s | %s | %s" % (c.author, c.title, self.get_url(), c['created']))

    def is_commented_by(self, account):
        commented_by = [reply['author'] for reply in self.get_comment().get_replies()]
        return account in commented_by

    def is_upvoted_by(self, account):
        voters = self.get_comment().get_curation_rewards()['active_votes'].keys()
        return account in voters

    def is_downvoted_by(self, account):
        has_downvoted = False
        for vote in self.get_comment().get_votes():
            if vote.voter == account and vote.percent < 0:
                has_downvoted = True
        return has_downvoted

    def is_comment(self):
        c = self.get_comment()
        return c["parent_author"] != ''
