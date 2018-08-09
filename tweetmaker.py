# -*- coding: utf-8 -*-
import os
import random


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
    return " ".join(markov_chain).replace("\n", " ")


def do_tweets(number):
    for _ in range(number):
        print(make_tweet(beginning_words, map_dict, 20))


if __name__ == '__main__':
    screen_name = str(input("Enter the twitter username: "))
    if not os.path.exists(f"data{os.sep}{screen_name}.txt"):
        import twitterminer
        from twitterminer import TwitterHistory
        UserBot = TwitterHistory(screen_name)
        full_tweets = UserBot.get_tweets()
        tweet_texts = UserBot.return_only_tweet_text(full_tweets)
        UserBot.save_tweets_to_file(tweet_texts)

    tweet_file = f"data{os.sep}{screen_name}.txt" 
    
    with open(tweet_file, "r") as reader:
        tweetlist = [tweet for tweet in reader]


    beginning_words = beginning_words(tweetlist)
    pairs = make_pairs(tweetlist)
    map_dict = create_dict(pairs)

    do_tweets(20)
