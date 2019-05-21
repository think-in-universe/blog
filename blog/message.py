# -*- coding:utf-8 -*-

import traceback

from utils.logging.logger import logger


def get_message(id):
    return build_message(id)

def build_message(id, footer=True, message_marker=False):
    message = MESSAGES[id]

    if footer:
        message += FOOTERS[id]
    if message_marker:
        message += MESSAGE_ID.format(message_id=id)

    return message

MESSAGE_ID = """
<div message_id=\"{message_id}\"></div>
"""

MESSAGES = {}
FOOTERS = {}

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
thumbnail: {thumbnail}
---


{body}
"""

FOOTERS["blog"] = """
- - -

This page is synchronized from the post: [{title}]({url})
"""

