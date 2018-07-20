#!/bin/python

import newsfilter

from taskbarScroller import Scroller


def parseAction(entity):
    T = "enterHyperlink -l %s"
    return T % entity[1]


def processData(data):
    for i, d in enumerate(data):
        data[i].append(i % 2)
    return data


if __name__ == "__main__":
    scroller = Scroller(100, 0.2, 2, 7)

    scroller.gatherData = newsfilter.gatherParseTweets
    scroller.parseAction = parseAction
    scroller.processData = processData

    scroller.scrollerLoop()
