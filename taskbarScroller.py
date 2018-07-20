#!/bin/python
import sys
import time
import colour


class Scroller():
    def __init__(self, textlength, timestep, step, interspace):
        self.textlength = textlength
        self.timestep = timestep
        self.interspace = interspace
        self.step = step
        self.dataEntities = []

    def selectColor(self, entity):
        _color = 'grey' if not entity[2] else 'white'
        hexColor = colour.Color(_color).hex

        return hexColor

    def parseWords(self, entity):
        return entity[0]

    def parseAction(self, entity):
        return entity[1]

    def processData(self, data):
        return data

    def renderScroller(self):
        xmobarBase = "<fc=%s>%s</fc>"
        actionWrapper = "<action=`%s`>%s</action>"

        outputText = ""
        positionMarker = 0

        for E, entity in enumerate(self.dataEntities):
            totalLength = 0
            view = True

            words = self.parseWords(entity) + (" "*self.interspace)
            if not E:
                words = words[self.position:]

            totalLength = len(words)
            positionMarker += totalLength

            # ELIMINATE ENTIRE ENTRY;
            if not words:
                view = False
                self.dataEntities[E] = None

            # CUT THE REAR END OF THE TEXTPIECE;
            elif positionMarker >= self.textlength:
                words = words[:self.textlength-positionMarker]
                if not words:
                    view = False
                    break

            # IF IT WILL SHOW GIVEN BLOCK;
            if view:
                hexColor = self.selectColor(entity)

                W = len(list(set(words)))
                if W > 1 or " " not in words:
                    segmentOutput = xmobarBase % (hexColor, words)
                    Action = self.parseAction(entity)
                    if Action:
                        segmentOutput = actionWrapper % (
                            Action, segmentOutput)
                else:
                    segmentOutput = words

                outputText += segmentOutput

        print(outputText)
        sys.stdout.flush()

    def scrollerLoop(self):
        self.position = 0
        self.runCount = 0
        while True:
            if len(self.dataEntities) < 7:
                rawData = self.gatherData()
                self.dataEntities += self.processData(rawData)

            self.renderScroller()
            while self.dataEntities[0] == None:
                del self.dataEntities[0]
                self.position = 0
            self.position += self.step
            time.sleep(self.timestep)
