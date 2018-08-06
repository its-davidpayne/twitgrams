# -*- coding: utf-8 -*-
from twython import Twython
import json
import os
import random
import sys
import time
        
                
screen_name = sys.argv[1]

if not os.path.exists("../{}.txt".format(screen_name)) and not os.path.exists("{}.txt".format(screen_name)):
    import twitterminer
    from twitterminer import TwitterHistory
    UserBot = TwitterHistory(screen_name)
    full_tweets = UserBot.get_tweets()
    tweet_texts = UserBot.return_only_tweet_text(full_tweets)
    UserBot.save_tweets_to_file(tweet_texts)

if os.path.exists(f"{screen_name}.txt"):
    tweet_file = f"{screen_name}.txt" 
else:
    tweet_file = f"../{screen_name}.txt"


with open(tweet_file, "rb") as reader:
    tweetlist = [tweet for tweet in reader]


def beginning_words(tweetlist):
    beginlist = []
    for tweet in tweetlist:
        tweets = tweet.split()
        beginlist.append(tweets[0])
    return beginlist


def make_pairs(tweetlist):
    for tweet in tweetlist:
        tweets = tweet.split()
        for i in range(len(tweets)-1):
            try:
                yield (tweets[i], tweets[i+1])
            except IndexError:
                yield (tweets[i])
   

def create_dict(pairs):
    map_dict = {}
    for prefix, suffix in pairs:
        if prefix in map_dict.keys():
            map_dict[prefix].append(suffix)
        else:
            map_dict[prefix] = [suffix]
    return map_dict


def make_tweet(beginlist, map_dict, length):
    first_word = random.choice(beginlist)
    markov_chain = [first_word]
    for _ in range(length):
        try:
            markov_chain.append(random.choice(map_dict[markov_chain[-1]]))
        except KeyError:
            continue
    return " ".join(markov_chain)

def do_tweets(number):
    for _ in range(number):
        make_tweet(beginning_words, map_dict, 20)

#TODO clean out links, @s, maybe emojis.

beginning_words = beginning_words(tweetlist)
pairs = make_pairs(tweetlist)
map_dict = create_dict(pairs)

make_tweet(beginning_words, map_dict, 20)