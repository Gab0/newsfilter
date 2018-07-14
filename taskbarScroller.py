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

    def selectColor(self, E, entity):
        _color = 'grey' if not entity[2] else 'white'
        return _color

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
        bcutIndex = 0

        for E, entity in enumerate(self.dataEntities):
            totalLength = 0
            view = True

            words = self.parseWords(entity) + (" "*self.interspace)

            totalLength = len(words)
            positionMarker += totalLength
            if self.position > positionMarker:
                view = False
                self.dataEntities[E] = None

            # CUT THE BEGGINING OF THE TEXTPIECE;
            elif self.position + totalLength > positionMarker:
                bcutIndex = self.position + totalLength - positionMarker
                words = words[bcutIndex:]

            # CUT THE REAR OF THE TEXTPIECE;
            elif positionMarker - bcutIndex > self.textlength:
                ecutIndex = self.textlength - (positionMarker - bcutIndex)
                if len(words) + ecutIndex < 1:
                    view = False
                words = words[:ecutIndex]
            if view:
                _color = self.selectColor(E, entity)
                hexColor = colour.Color(_color).hex

                segmentOutput = xmobarBase % (hexColor, words)
                if entity[1]:
                    segmentOutput = actionWrapper % (
                        self.parseAction(entity), segmentOutput)
                outputText += segmentOutput

            if positionMarker - bcutIndex > self.textlength:
                break

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
