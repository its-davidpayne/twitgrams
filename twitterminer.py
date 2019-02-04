#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
import time
from twython import Twython

CREDENTIALS_FILENAME = 'creds-twitter.json'
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
    
    def __repr__(self):
        return f"TwitterHistory({self.screen_name})"

    def get_tweets(self):
        """ The twitter API allows you to fetch 4x200 tweets at a time, at 15 min
        intervals, to a max of 3000.

        So for a user with 3k+ tweets, this WILL take 45 minutes regardless.
        """
        cumulative_result = []
        count = 0
        max_id = None
        try:
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
                    print(f"{time.asctime()} Completed round {count}. {len(cumulative_result)} Tweets gathered so far")
                else:
                    print(f"{time.asctime()} Finished! {len(cumulative_result)} Tweets gathered in total.")
                if count in [3, 7, 11]:
                    print(f"{time.asctime()} Sleeping for 15 minutes")
                    time.sleep(910)
        except IndexError as e:
            print(f"{time.asctime()} Ending early with only {len(cumulative_result)} tweets gathered.\n{str(e)}")
        return cumulative_result
    
    def return_only_tweet_text(self, full_tweets):
        """ each tweet is a json object, we only want the actual text"""
        return [tweet['text'] for tweet in full_tweets]
    
    def skip_word(self, word):
        """ skip any word that fits these criteria"""
        if word.startswith("@"):
            return True
        elif word.startswith("http"):
            return True
        # Scope for more elifs here
        else:
            return False

    def clean_tweet(self, text):
        """ removes words that skip_word() deems unusable"""
        # return " ".join([word for word in text.split() if not self.skip_word(word)])
        word_list = text.split(" ")
        out_list = []
        for word in word_list:
            if not self.skip_word(word):
                out_list.append(word)
        return " ".join(out_list)

    def save_tweets_to_file(self, tweet_texts):
        """after cleaning, write the results to a txt file in the 
        data subfolder
        """
        file_name = f"data{os.sep}{self.screen_name}.txt"
        with open(file_name, "w") as textwriter:
            for tweet in tweet_texts:
                tweet = self.clean_tweet(tweet)
                textwriter.write("{}\n".format(tweet))


