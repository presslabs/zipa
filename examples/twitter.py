# -*- coding: utf-8 -*-
# vim: ft=python:sw=4:ts=4:sts=4:et:
from zipa import api_twitter_com as tw
from requests_oauthlib import OAuth1

TWITTER_APP_KEY = 'XXXX'
TWITTER_APP_SECRET = 'XXXX'
TWITTER_USER_TOKEN = 'XXXX'
TWITTER_USER_SECRET = 'XXXX'

tw.config.use_extensions = True
tw.config.prefix += '1.1'
tw.config.serializer = 'form'
tw.config.auth = OAuth1(TWITTER_APP_KEY, client_secret=TWITTER_APP_SECRET,
                        resource_owner_key=TWITTER_USER_TOKEN,
                        resource_owner_secret=TWITTER_USER_SECRET)

tweet = tw.statuses.update_.create(status='API call to twitter using '
                                   'https://github.com/vtemian/zipa #ep14')
print(tweet.id)
