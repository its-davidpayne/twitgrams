# -*- coding: utf-8 -*-
from twython import Twython
import json
import random
import sys
import time

CREDENTIALS_FILENAME = '../creds-twitter.json'
jf = open(CREDENTIALS_FILENAME)
creds = json.load(jf)
jf.close()

client = Twython(creds['consumer_key'],
                 creds['consumer_secret'],
                 creds['access_token'],
                 creds['access_token_secret'])


class TwitterHistory():
    def __init__(self, screen_name):
        self.screen_name = screen_name
    
    def get_tweets(self):
        cumulative_result = []
        count = 0
        max_id = None
        while count < 16:
            if count == 0:
                result = client.get_user_timeline(screen_name=self.screen_name, 
                                              count=200, include_rts=False)
            else:
                result = client.get_user_timeline(screen_name=self.screen_name, 
                                                  count=200, include_rts=False, 
                                                  max_id=max_id)
            
            max_id = result[-1]['id'] - 1
            for tweet in result:
                cumulative_result.append(tweet)
            count += 1
            if count < 15:
                print("Completed round {}. {} Tweets gathered so far".format(
                        count, len(cumulative_result)))
            else:
                print("Finished! {} Tweets gathered in total.".format(
                        len(cumulative_result)))
            if count in [3, 7, 11]:
                print("Sleeping for 15 minutes")
                time.sleep(930)
        return cumulative_result
    
    def return_only_tweet_text(self, full_tweets):
        return [tweet['text'] for tweet in full_tweets]
    
    def clean_tweet(self, text):
        """ much more to add here """
        word_list = text.split(" ")
        for word in word_list:
            if word.startswith("http"):
                word = ""
            elif word.startswith("@"):
                word = ""
        return " ".join(word_list)

    def save_tweets_to_file(self, tweet_texts):
        file_name = "{}.txt".format(self.screen_name)
        with open(file_name, "w") as textwriter:
            for tweet in tweet_texts:
                tweet = self.clean_tweet(tweet)
                tweet = tweet.encode("utf-8", "ignore")
                textwriter.write("{}\n".format(tweet))


