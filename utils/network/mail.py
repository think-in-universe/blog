# -*- coding:utf-8 -*-

import os
import zmail

class Mail:

    def __init__(self):
        self.mail_addr = os.environ['MAIL_ADDR']
        mail_pwd = os.environ['MAIL_SEC']
        self.server = zmail.server(self.mail_addr, mail_pwd)

    def send(self, title, body, attachments=[], html=True, retries=5):
        success = False
        if html:
            success = self.server.send_mail(self.mail_addr, {
                                  'subject' : title,
                                  'content_html' : body,
                                  'attachments': attachments
                              })
        else:
            success = self.server.send_mail(self.mail_addr, {
                                  'subject' : title,
                                  'content_text' : body,
                                  'attachments': attachments
                              })

        if not success and retries > 0:
            return self.send(title, body, attachments, html, retries-1)
        else:
            return success

