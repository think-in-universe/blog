# -*- coding:utf-8 -*-

import logging
import os

import pandas as pd
from beem import Steem
from beem.instance import set_shared_steem_instance

from utils.logging.logger import logger_ctl

pd.options.mode.chained_assignment = None


STEEM_HOST = "https://steemit.com"
STEEMD_HOST = "https://steemd.com"
# more API nodes can be found from the file: https://github.com/holgern/beem/blob/cf284bdcffd490463be19cbf518af02db8eaf4be/beem/nodelist.py
STEEM_API_NODES = [
    "https://rpc.steemviz.com",
    "https://anyx.io", # may introduce encoding issue, be careful
    "https://steemd.minnowsupportproject.org",
    "https://api.steemitdev.com",
    "https://api.steemit.com",
]

STEEM_KEYS = ["posting_key", "active_key"]


class Settings:

    debug_mode = False
    steem_db_inst = None
    steem_instance = None

    def __init__(self):
        self.keys = {}
        pass

    def set_debug_mode(self):
        if not self.is_debug():
            print('launch: debug mode')
            self.debug_mode = True
            self.set_log_level(logging.INFO)
            self.steem_db_inst = None

    def is_debug(self):
        return self.debug_mode

    def set_log_level(self, level):
        logger_ctl.set_level(level)

    def get_db(self):
        if self.steem_db_inst is None:
            if self.is_debug():
                self.steem_db_inst = SteemDatabase(TESTING_DATABASE)
            else:
                self.steem_db_inst = SteemDatabase(PRODUCTION_DATABASE)
        return self.steem_db_inst

    def set_steem_node(self, node=None):
        if self.steem_instance is None:
            # print(shared_steem_instance().get_config())
            api_node = node or self.get_env_var('API_NODE') or STEEM_API_NODES[2]
            if self.is_debug():
                print ("connecting to steem node...")
            stm = Steem(
                node=api_node,
                # bundle=True, # Enable bundle broadcast
                # nobroadcast=True, # Enable this for testing
                keys=self._get_steem_keys(),
            )
            # Set stm as shared instance
            set_shared_steem_instance(stm)
            if self.is_debug():
                print ("connected to node: [{}]".format(api_node))
            self.steem_instance = stm

        return self.steem_instance

    def get_steem_node(self, node=None):
        if self.steem_instance is None:
            self.set_steem_node(node)
        return self.steem_instance

    def _get_steem_keys(self):
        steem_keys = []
        for key in STEEM_KEYS:
            v = self._get_steem_key(key)
            if v:
                steem_keys.append(v)
        return steem_keys

    def _get_steem_key(self, key):
        return self.get_env_var(key.upper())

    def get_env_var(self, key):
        if key in os.environ:
            return os.environ[key]
        else:
            return None


settings = Settings()

