# -*- coding:utf-8 -*-

from beem.account import Account
from beem.rc import RC as ResourceCredits
from utils.system.date import from_then


class SteemAccount:

    def __init__(self, author):
        self.author = author
        self.account = Account(self.author)
        self.rc = None

    def get_profile(self, key=None):
        profile = self.account.profile
        if key is not None:
            if key in profile:
                return profile[key]
            else:
                return None
        else:
            return profile

    def name(self):
        return self.account.name

    def reputation(self):
        return self.account.rep

    def steem_power(self, own=False):
        return self.account.get_steem_power(onlyOwnSP=False)

    def follower_count(self):
        return self.account.get_follow_count()["follower_count"]

    def post_count(self):
        return self.account.json()["post_count"]

    def birthday(self):
        return self.account["created"]

    def age_in_days(self):
        created = self.birthday()
        if created:
            return from_then(created).days
        return None

    def _get_rc(self):
        if self.rc is None:
            self.rc = ResourceCredits()
        return self.rc

    def _get_rc_mana(self, key):
        rc_info = self.account.get_rc_manabar()
        if key in rc_info:
            return rc_info[key]
        else:
            return None

    def rc_percentage(self):
        return self._get_rc_mana('current_pct')

    def current_rc_mana(self):
         return self._get_rc_mana('current_mana')

    def max_rc_mana(self):
        return self._get_rc_mana('max_mana')

    def remaining_comments(self):
        cost_per_comment = self._get_rc().comment()
        number_of_comments = self.current_rc_mana() / cost_per_comment
        return int(number_of_comments)

    def daily_recovery_comments(self):
        cost_per_comment = self._get_rc().comment()
        number_of_comments = self.max_rc_mana() * 0.2 / cost_per_comment
        return number_of_comments
