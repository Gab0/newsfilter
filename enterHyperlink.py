import mmap
import csv
import webbrowser
from os import path, chdir

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
            return LINK_INFO[w-1][1]

    return None


scrollerPosition = readScrollerPosition()
print(scrollerPosition)

scrollerPosition = scrollerPosition[2] * 256 + scrollerPosition[1] + 70
print(scrollerPosition)
hyperLink = getHyperlink(scrollerPosition)
print(hyperLink)
if hyperLink and hyperLink != 'None':
    webbrowser.open(hyperLink)
