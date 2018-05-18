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
    if LINK:
        S += "ø"
    DATA = (S,LINK)

    return DATA

def getMessage(NewsOrigin, N=7):

    SelectedOrigins = [ choice(NewsOrigin) for k in range(4) ]

    statuses = []
    for NO in SelectedOrigins:
        statuses += api.GetUserTimeline(screen_name=NO, count=7)

    statuses = [ x.text for x in statuses ]

    Status=[]

    for k in range(N):
        message = parseTweet(choice(statuses))
        Status.append(message)

    return Status

if __name__ == '__main__':
    # read twitter login credentials and channel list file;
    C = loadCredentials()

    # login @ twitter;
    api = twitterLogin(C['Credentials'])

    # fetch and concatenate messages;
    M = getMessage(C['NewsChannels'], N=70)
    messagetext=''
    linktext=''
    for S in M:
        messagetext+=S[0] + ' ' * 7
        linktext+='%i,%s\n' % (len(messagetext), S[1])



    # append news data to scroll file;
    #Q=open(getenv('HOME')+'/.scroll', 'w+')
    #Q.write(M)
    print(messagetext.strip('\n'))
    #print('###')
    #print(linktext.strip('\n'))
    open('LINK_INFO', 'w').write(linktext)
    #print("ààaàààààà")

