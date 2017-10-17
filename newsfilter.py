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
        Data[F] = [x for x in D if x]

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
    if LINK:
        S += " >"
        LINK = {S:LINK}
    else:
        LINK = {}

    return S, LINK

def getMessage(NewsOrigin, N=7):

    SelectedOrigins = [ choice(NewsOrigin) for k in range(4) ]

    statuses = []
    for NO in SelectedOrigins:
        statuses += api.GetUserTimeline(screen_name=NO, count=7)

    statuses = [ x.text for x in statuses ]

    Status=[]
    LinkData = {}
    for k in range(N):
        message, link = parseTweet(choice(statuses))
        Status.append(message)
        LinkData.update(link)



    writeLink(LinkData)

    return Status

if __name__ == '__main__':
    # read twitter login credentials and channel list file;
    C = loadCredentials()

    # login @ twitter;
    api = twitterLogin(C['Credentials'])

    # fetch and concatenate messages;
    M=(' '*5).join(getMessage(C['NewsChannels']))

    # append news data to scroll file;
    Q=open(getenv('HOME')+'/.scroll', 'w+')
    Q.write(M)


