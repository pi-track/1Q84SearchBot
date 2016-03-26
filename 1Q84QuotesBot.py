#!/usr/bin/env python
import tweepy
from Search1Q84 import search_text
from FoodKeys import keys
import re
import random
import time
import os

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_latest_since_id():
    f = open('since_id.txt','r')
    latest_since_id = f.read()
    f.close()
    return str(latest_since_id)

def set_latest_since_id(since_id):
    f = open('since_id.txt','w')
    f.write(str(since_id))
    f.close()
    return

#Search the api for anything @1Q84Quotes since the last time we searched
twt = api.search(q="@1Q84Quotes", since_id=get_latest_since_id())
#twt = api.search(q="@1Q84Quotes", since_id='713474105777979392')
#Set the latest since_id to the latest tweet to ignore these tweets going forward
if len(twt) > 0:
    set_latest_since_id(twt[0].id)  # set this as the latest since id so that the next search will include everything since then

# Trim out @'s #'s etc
#search for matches
for s in twt:
    q = s.text
    s.line = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", s.text).split())
    print(s.line)
    s.matches = search_text(s.line)
    # print(s.line, s.matches)
    print(s.id)
    # s.reply=''

#make sure the reply is <140 characters
# select one of the matches at random and send it back at the original user
for s in twt:
    s.reply = ''
    while len(s.reply) >= 140 or len(s.reply) == 0:
        if len(s.matches) == 0:
            s.reply_text = 'nothing'
        else:
            s.reply_text = random.choice(s.matches)
            s.matches.remove(s.reply_text)
        s.reply = ".@{0} {1}".format(s.user.screen_name, s.reply_text)
    #print('len reply = {0} and reply is: {1}'.format(len(s.reply), s.reply))
    api.update_status(s.reply)
    print(s.reply)
