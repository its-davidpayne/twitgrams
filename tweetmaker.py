#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random

class Tweeter():
    def __init__(self, screen_name):
        self.screen_name = screen_name
        self.tweet_file = f"data{os.sep}{self.screen_name}.txt"
        with open(self.tweet_file, "r") as reader:
            self.tweetlist = [tweet.replace("\n", " ") for tweet in reader]
        self.first_words = self.beginning_words(self.tweetlist)
        self.pairs = self.make_pairs(self.tweetlist)
        self.bigram_dict = self.create_bigram_dict(self.pairs)

    def __repr__(self):
        return f"Tweeter({self.screen_name})"
    
    def beginning_words(self, tweetlist):
        """ returns a list of the first word of each tweet"""
        # return [tweet[0] for tweet in tweets.split() for tweets in tweetlist]
        beginlist = []
        for tweet in tweetlist:
            tweets = tweet.split()
            try:
                beginlist.append(tweets[0])
            except:
                continue
        return beginlist
    
    def make_pairs(self, tweetlist):
        """returns every word and the word that follows it"""
        for tweet in tweetlist:
            tweets = tweet.split()
            for i in range(len(tweets)-1):
                try:
                    yield (tweets[i], tweets[i+1])
                except IndexError: # if i is last word of the tweet
                    yield (tweets[i])
    
    def create_bigram_dict(self, pairs):
        """returns a dict containing mapping every word to all words that 
        have ever come immediately after it within the corpus"""
        bigram_dict = {}
        for prefix, suffix in pairs:
            if prefix in bigram_dict.keys():
                bigram_dict[prefix].append(suffix)
            else:
                bigram_dict[prefix] = [suffix]
        return bigram_dict
    
    def make_tweet(self, first_words, bigram_dict, length):
        """ picks a random first word, then randomly selects one of the words
        that can follow it, and so on until it selects a sentence end or the 
        assembled tweet reaches <length> words long.
        """
        chain = [random.choice(first_words)]
        for _ in range(length):
            try:
                chain.append(random.choice(bigram_dict[chain[-1]]))
            except KeyError:
                continue
        return " ".join(chain).replace("\n", " ")
    
    def multitweets(self, number):
        """wrapper to make creating tweets simpler"""
        for _ in range(number):
            print(self.make_tweet(self.first_words, self.bigram_dict, 23))


if __name__ == '__main__':
    screen_name = str(input("Enter the twitter username: "))
    # This section uses the Twitter api to record up to 3000 of a user's
    # tweets. This can take an hour due to twitter API limits.
    # Unless of course I've already gathered this user's tweets, then
    # it just reads them from the existing textfile.
    if not os.path.exists(f"data{os.sep}{screen_name}.txt"):
        import twitterminer
        from twitterminer import TwitterHistory
        UserReader = TwitterHistory(screen_name)
        full_tweets = UserReader.get_tweets()
        tweet_texts = UserReader.return_only_tweet_text(full_tweets)
        UserReader.save_tweets_to_file(tweet_texts)
    
    Twitterer = Tweeter(screen_name)
    Twitterer.multitweets(20)
