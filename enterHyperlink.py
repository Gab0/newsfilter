import mmap
import csv
import webbrowser
from os import path, chdir

import optparse


parser = optparse.OptionParser()
parser.add_option('-s', dest='screenTextSpan', type='int', default=112)
parser.add_option('-l', dest='linkAddress')
options,args = parser.parse_args()
chdir(path.dirname(path.realpath(__file__)))


def readScrollerPosition():
    with open('/dev/shm/scrollerPos', 'r') as f:
        with mmap.mmap(f.fileno(), 0,
                       access=mmap.ACCESS_READ) as m:
            W = m.read()
            c = W.index(b'scrollerPos')

            print(c)
            B = W[c-5:c]
            print(B)
            NBRS = []
            for N in range(4):
                SLICE = B[N:N+1]
                print(SLICE)
                Number = ord(SLICE)
                NBRS.append(Number)
    return NBRS


def getHyperlink(scrollerPosition):
    LINK_INFO = csv.reader(open("LINK_INFO"))
    LINK_INFO = list(LINK_INFO)
    for w, W in enumerate(LINK_INFO):
        print(W)
        if scrollerPosition < int(W[0]):
            deltaNext = int(W[0]) - scrollerPosition
            deltaPrevious = scrollerPosition - int(LINK_INFO[w-1][0])

            MostAlignedLinkIndex = w-1 if deltaPrevious > deltaNext else w
            return LINK_INFO[MostAlignedLinkIndex][1]

    return None

if __name__ == '__main__':
    if options.linkAddress:
        webbrowser.open(options.linkAddress)
    scrollerPosition = readScrollerPosition()
    print(scrollerPosition)

    scrollerPosition = scrollerPosition[2] * 256 + scrollerPosition[1]
    print(scrollerPosition)
    hyperLink = getHyperlink(scrollerPosition)
    print(hyperLink)
    if hyperLink and hyperLink != 'None':
        webbrowser.open(hyperLink)
