#!/bin/python

import time
import colour
import sys
import newsfilter

from taskbarScroller import Scroller


def parseAction(entity):
    T = "python /home/gabs/newsfilter/enterHyperlink.py -l %s"
    return T % entity[1]i


def processData(data):
    for i, d in enumerate(data):
        data[i].append(i % 2)
    return data


if __name__ == "__main__":
    scroller = Scroller(120, 0.3, 2, 7)

    scroller.gatherData = newsfilter.gatherParseTweets
    scroller.parseAction = parseAction
    scroller.processData = processData

    scroller.scrollerLoop()
