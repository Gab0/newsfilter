#!/bin/python
from random import choice
import twitter
from subprocess import call
from os import path, chdir, getenv
import sys
from time import sleep

chdir(path.dirname(path.realpath(__file__)))


def writeLink(LINK):
    W = open('LINK_INFO','w')
    W.write(str(LINK))
    W.close()


def loadCredentials():
    Files = ['Credentials', 'NewsChannels']

    Data = {}
    for F in Files:
        if not path.isfile(F):
            print("%s file not found!" % F)
            exit()
        D = open(F).read().split('\n')
        Data[F] = [ x for x in D if x and not x.startswith('#') ]

    return Data


def twitterLogin(Credentials):

    api = twitter.Api(consumer_key=Credentials[0],
                      consumer_secret=Credentials[1],
                      access_token_key=Credentials[2],
                      access_token_secret=Credentials[3],
                      sleep_on_rate_limit=True)
    return api


def parseTweet(Tweet):
    S = Tweet.split(' ')
    LINK=None
    
    for W in range(len(S)):
        if not S[W]:
            continue
        if 'http' in S[W] or 'fb' in S[W]:
            LINK=S[W]
            S[W] = None
        
        elif S[W] == 'RT':
            S[W] = None
            S[W+1] = None

    S = ' '.join([x for x in S if x])
    if S.endswith(':'):
        S=S[:-1]

    DATA = (S,LINK)

    return DATA


def getMessage(api, NewsOrigin, N=7):

    SelectedOrigins = [ choice(NewsOrigin) for k in range(4) ]

    statuses = []
    for NO in SelectedOrigins:
        statuses += api.GetUserTimeline(screen_name=NO, count=7)

    statuses = [x.text for x in statuses]

    Status=[]

    for k in range(N):
        message = parseTweet(choice(statuses))
        Status.append(message)

    return Status


def gatherParseTweets(tweet_number=70):
    # read twitter login credentials and channel list file;
    C = loadCredentials()

    # login @ twitter;
    api = twitterLogin(C['Credentials'])

    # fetch and concatenate messages;
    Tweets = getMessage(api, C['NewsChannels'], N=tweet_number)
    messagetext=''
    linktext=''

    tweetList = []

    for S in Tweets:
        tweetMessage = S[0]
        tweetMessage = tweetMessage.replace('…', '').replace('\n', '')
        messagetext += tweetMessage

        tweetLink = S[1].replace('\n', '') if S[1] else None
        linktext += '%i,%s,%s\n' % (len(messagetext), tweetLink, S[0].replace(',',';').replace('\n', ''))

        tweetData = [tweetMessage, tweetLink]
        tweetList.append(tweetData)

    tweetList = [t for t in tweetList if t[0]]

    return tweetList


