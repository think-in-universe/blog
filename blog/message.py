# -*- coding:utf-8 -*-

import traceback

from utils.logging.logger import logger


def get_message(id):
    return build_message(id)

def build_message(id, message_marker=False):
    if message_marker:
        return MESSAGES[id] + MESSAGE_ID.format(message_id=id)
    else:
        return MESSAGES[id]

MESSAGE_ID = """
<div message_id=\"{message_id}\"></div>
"""

MESSAGES = {}

MESSAGES["blog"] = """
---
title: "{title}"
catalog: true
toc_nav_num: true
toc: true
date: {date}
categories:
- {category}
tags:
{tags}
---


{body}
"""

