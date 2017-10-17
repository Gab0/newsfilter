#!/bin/python

import webbrowser

from os import chdir, path
chdir(path.dirname(path.realpath(__file__)))

def getCursor_Info():
    Cursor = open('scroll').read()
    Cursor = Cursor.split('>')[0]

    LinkInfoData =  open('LINK_INFO').read()
    LinkInfo = eval(LinkInfoData)

    return Cursor, LinkInfo




Cursor, LinkInfo = getCursor_Info()
print(Cursor)
#print(LinkInfo)
for W in LinkInfo.keys():
    if W.index(Cursor) > -1:
        webbrowser.open_new(LinkInfo[W])
        break
