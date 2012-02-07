# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2008 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                              Vanderson Mota dos Santos <vanderson.mota@gmail.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from TopComparator import TopComparator
from TextColumn import TextColumn
from TextElement import TextElement
from Line import Line
from LeftComparator import LeftComparator
from TopComparatorForTexts import TopComparatorForTexts
from MultilineBlock import MultilineBlock
from SecondClassification import SecondClassification
from math import fabs
from Font import Font
from BeautifulSoup import BeautifulStoneSoup

class FirstClassification:

    def __init__(self, path):

        self.__fontsList = []
        self.__linesList = []
        self.__fontCounterList = []
        self.__multiLineBlocksList = []
        self.__path = path
        self.__modus = False
        self.__pageTextColumnsCount = 1
        self.__textColumnsList = []
        self.__removedElementsBefore = 0
        self.__removedElementsAfter = 0
        self.__pageNumber = 0

    def run(self, filename=""):

        self.__xmlDocument = BeautifulStoneSoup(open(filename, 'r').read())

        self.__pagesList = self.__xmlDocument.findAll("page")
        self.__linesBefore = 0

        for page in self.__pagesList:
            self.__textColumnsList = []
            self.__pageNumber = page.get("number")
            self.__pageHeight = page.get("height")
            self.__pageWidth = page.get("width")

            self.__textColunmsWidth = int(self.__pageWidth) / int(self.__pageTextColumnsCount)

            for txtColumnsCounter in range(0,self.__pageTextColumnsCount + 1):
                self.__txtColumn = TextColumn(self.__textColunmsWidth)
                self.__textColumnsList.append(self.__txtColumn)

            self.__currentFontElementsList = page.findAll("fontspec")

            self.createFontAndAddToList(self.__currentFontElementsList)

            self.__currentTextElements = page.findAll("text")
            self.__currentTextElements.sort(cmp=TopComparator().compare)
            self.__distance = 0

            self.addLineToTextColumn(self.__currentTextElements, self.__textColunmsWidth)

            for textColumnObj in self.__textColumnsList:
                for line in textColumnObj.getLinesList():
                    self.__linesList.append(line)

            self.__multiModus = False
            self.__d = 0
            self.__sumOfDistances = 0

            self.__counter = self.__linesBefore
            while self.__counter < len(self.__linesList):

                lineObj = self.__linesList[self.__counter]
                lineObj.sortTextList(comparator=LeftComparator().compare)

                self.mergeTextElements(lineObj)
                self.updateTextElementsValues(lineObj)

                if len(lineObj.getTextList()) > 1:
                    # multi-line
                    self.markLineAsMultiLine(lineObj)

                elif len(lineObj.getTextList()) == 1:
                    # single-line
                    if self.__multiModus == True:

                        previousLine = self.__linesList[self.__counter-1]
                        self.__sumOfDistances += self.__d
                        textElement = lineObj.getTextElement(0)
                        topDistance = int(lineObj.getFirstTop()) - int(previousLine.getBottom())

                        control = False
                        belongs = 0

                        for nTextElement in previousLine.getTextList():

                            leftDistance = abs(nTextElement.getLeft() - textElement.getLeft())
                            rightDistance = abs((nTextElement.getLeft() + nTextElement.getWidth()) \
                                                - (textElement.getLeft() + textElement.getWidth()))

                            if topDistance < (textElement.getHeight()/2) and \
                            self.__nextTextElement.getTyp() == self.__textElement.getTyp() and \
                            self.__nextTextElement.getTyp() == "text" and \
                            (leftDistance < 3 or rightDistance < 3):

                                stringValue = nTextElement.getValue() + \
                                "\n" + textElement.getValue()

                                nTextElement.setValue(stringValue)

                                nTextElement.setCountLines(nTextElement.getCountLines() + 1)

                                self.__linesList.pop(self.__counter)
                                self.__counter -= 1
                                self.updateTextValues(nTextElement, textElement)
                                self.updateLineValues(textElement, previousLine)
                                control = True

                            if self.inBoundaries(textElement, nTextElement) == 1:
                                belongs += 1


                        if (control == False):
                            currentMultiLineBlock = self.__multiLineBlocksList[-1]
                            multiLineBlockElementCount = currentMultiLineBlock.getEnd() \
                                                        - currentMultiLineBlock.getBegin()
                            if multiLineBlockElementCount > 0:
                                currentMultiLineBlock.setAvgDistance(self.__sumOfDistances / multiLineBlockElementCount)

                            else:
                                currentMultiLineBlock.setAvgDistance(self.__d)

                            self.__multiModus = False
                    else:
                        pass

                self.__counter += 1

            self.__multiModus = False
            self.__linesBefore = len(self.__linesList)


        # MERGE MULTILINE BLOCKS

        self.mergeMultilineBlock()
        self.__xmlDocument = None
        secondClassificationObj = SecondClassification(self.__path, self.__fontsList, self.__fontCounterList, self.__linesList, self.__multiLineBlocksList)
        resultTuple = secondClassificationObj.run()

        return resultTuple


    def markLineAsMultiLine(self, lineObj):

        if self.__multiModus == True:
            currentMultiLineBlock = self.__multiLineBlocksList[-1]
            self.__sumOfDistances += self.__d
            self.updateMultilineBlockValues(currentMultiLineBlock, lineObj)

        else:
            multiLineBlockObj = MultilineBlock()
            self.__sumOfDistances = 0
            self.setMultiLineBlockValues(multiLineBlockObj, lineObj, self.__counter, self.__pageNumber)
            self.__multiLineBlocksList.append(multiLineBlockObj)
            self.__multiModus = True

    def updateTextElementsValues(self, lineObj):
        """
            updates the textElement objects in a given Line instance
        """
        for textElement in lineObj.getTextList():
            if len(textElement.getElementList()) > 0:
                elementList = textElement.getElementList()
                elementList.sort(cmp=TopComparatorForTexts().compare)
                value=""
                for element in elementList:
                    value += element.getValue() + " "
                textElement.setValue(value)
                textElement.setElementList([])

    def mergeTextElements(self, lineObj):
        """
            Gets the a textElement and the next one inside of a line.
            Then, checks if they belong together and merge them.
        """
        position = 0
        while position < (len(lineObj.getTextList())-1):
            self.__textElement = lineObj.getTextElement(pos=position)
            self.__nextTextElement = lineObj.getTextElement(pos=position+1)

            result = self.belongingTogether(self.__textElement,self.__nextTextElement)

            if result != -1:
                lineObj.removeTextElement(pos=position+1)
                if result == 1:
                    if len(self.__textElement.getElementList()) == 0:
                        self.__textElement.addElement(self.__textElement)
                    if len(self.__nextTextElement.getValue()) > 0:
                        self.__textElement.addElement(self.__nextTextElement)
                elif result == 0:
                    self.__textElement.setValue(self.__textElement.getValue() + " " + \
                                        self.__nextTextElement.getValue())
                self.updateTextValues(self.__textElement, self.__nextTextElement)

                position -= 1

            position += 1

    def addLineToTextColumn(self, currentTextElementsList, textColumnsWidth):
        """
            Creates a TextElement object and adds it to a line
        """
        for xmlTextElement in currentTextElementsList:
            currentTxtColumn = None
            currentTextElement = self.createTextElement(xmlTextElement)
            self.__rightColumn = abs(currentTextElement.getLeft()/textColumnsWidth)

            if (int(self.__rightColumn) < len(self.__textColumnsList)):
                currentTxtColumn = self.__textColumnsList[int(self.__rightColumn)]

                if (len(currentTxtColumn.getLinesList())) > 0:
                    line = currentTxtColumn.getLine(-1) #returns the value in the last position

                    if self.inTheLine(currentTextElement, line) == True:
                        # exactly in the boundaries of the line
                        line.addText(currentTextElement)
                        self.updateLineValues(currentTextElement, line)
                    else:
                        newLine = Line()
                        newLine.addText(currentTextElement)
                        self.setNewLineValues(currentTextElement, newLine)
                        currentTxtColumn.addLine(newLine)
                        self.__distance += int(newLine.getFirstTop()) - int(line.getLastTop())

                else:
                    newLine = Line()
                    newLine.addText(currentTextElement)
                    self.setNewLineValues(currentTextElement, newLine)
                    currentTxtColumn.addLine(newLine)

    def createFontAndAddToList(self, xmlFontList):
        for fontElement in xmlFontList:
            id = fontElement.get("id")
            size = fontElement.get("size")
            family = fontElement.get("family")
            color = fontElement.get("color")
            self.__fontObj = Font(self.__pageNumber, id, size, family, color);
            self.__fontsList.append(self.__fontObj)


    def inBoundaries(self, textElementObj, nextTextElementObj):
        textElementLeft = textElementObj.getLeft()
        textElementRight = textElementObj.getLeft() + textElementObj.getWidth()

        nextTextElementLeft = nextTextElementObj.getLeft()
        nextTextElementRight = nextTextElementObj.getLeft() + nextTextElementObj.getWidth()

        if (textElementLeft >= nextTextElementLeft and textElementRight <= nextTextElementRight) or \
        (textElementLeft >= nextTextElementLeft and textElementLeft <= nextTextElementRight \
        and textElementRight > nextTextElementRight) or (textElementLeft < nextTextElementLeft \
        and textElementRight >= nextTextElementLeft and textElementRight <= nextTextElementRight) or \
        (nextTextElementLeft >= textElementLeft and nextTextElementRight <= nextTextElementLeft):

            return 1


        return 0


    def inTheLine(self, textElementObj, lineObj):
        fontObj = self.__fontsList[int(textElementObj.getFont())]

        textBottom = textElementObj.getTop() + fontObj.getSize()

        if textElementObj.getTop() >= lineObj.getFirstTop() and \
        textElementObj.getTop() <= lineObj.getBottom():

            return True

        elif textBottom >= lineObj.getFirstTop() and textBottom <= lineObj.getBottom():
            return True

        elif textElementObj.getTop() <= lineObj.getFirstTop() and \
            textBottom >= lineObj.getBottom():

            return True

        else:
            return False

    def updateLineValues(self, textElementObj, lineObj):
        minTop = min(textElementObj.getTop(), lineObj.getTop())#olhaaa!!
        lineObj.setTop(minTop)
        fontObj = self.__fontsList[int(textElementObj.getFont())]
        b = textElementObj.getTop() + textElementObj.getHeight()
        lineObj.setBottom(max(b, lineObj.getBottom()))
        lineObj.setHeight(lineObj.getBottom() - lineObj.getTop())
        lineObj.setLeftmost(min(textElementObj.getLeft(),lineObj.getLeftmost()))
        sumLeftWidth = textElementObj.getLeft()+textElementObj.getWidth()
        lineObj.setRightmost(max(lineObj.getRightmost(),sumLeftWidth))
        lineObj.setFont(textElementObj.getFont())
        lineObj.setLastTop(max(textElementObj.getTop(),lineObj.getLastTop()))
        lineObj.setFirstTop(min(textElementObj.getTop(),lineObj.getFirstTop()))
        lineObj.increaseUsedSpace(textElementObj.getWidth()*textElementObj.getHeight())

    def setNewLineValues(self, textElementObj, lineObj):
        lineObj.setTop(textElementObj.getTop())
        fontObj = self.__fontsList[int(textElementObj.getFont())]
        lineObj.setBottom(textElementObj.getTop() + textElementObj.getHeight())
        lineObj.setHeight(lineObj.getBottom() - lineObj.getTop())
        lineObj.setLeftmost(textElementObj.getLeft())
        lineObj.setRightmost(textElementObj.getLeft() + textElementObj.getWidth())
        lineObj.setFont(textElementObj.getFont())
        lineObj.setLastTop(textElementObj.getTop())
        lineObj.setFirstTop(textElementObj.getTop())
        lineObj.setUsedSpace(textElementObj.getWidth() * textElementObj.getHeight())

    def belongingTogether(self, textElement, self__nextTextElement):
        merge = False
        nextTextElementLetterWidth = 0
        textElementLetterWidth = 0

        nextTextElementValue = self__nextTextElement.getValue()
        nextTextElementWidth = int(self__nextTextElement.getWidth())
        nextTextElementLeft = int(self__nextTextElement.getLeft())

        textElementValue = textElement.getValue()
        textElementWidth = int(textElement.getWidth())
        textElementLeft = int(textElement.getLeft())

        if len(self__nextTextElement.getValue()) != 0:
            nextTextElementLetterWidth = nextTextElementWidth/len(nextTextElementValue)

            if len(textElementValue) != 0:
                textElementLetterWidth = textElementWidth/len(textElementValue)

            distance = nextTextElementLeft - (textElementLeft + textElementWidth)
            textElementRight = textElementLeft + textElementWidth
            nextTextElementRight = nextTextElementLeft + nextTextElementWidth

            if textElementLeft > nextTextElementLeft and \
            textElementRight < nextTextElementRight:

                return 1

            elif nextTextElementLeft > textElementLeft and  \
            nextTextElementRight < textElementRight:

                return 1

            elif nextTextElementRight > textElementLeft and  \
            nextTextElementRight < textElementRight:

                return 1

            elif nextTextElementLeft > textElementLeft and \
            nextTextElementLeft < textElementRight:

                return 1

            elif distance <= nextTextElementLetterWidth and \
            distance <= textElementLetterWidth:

                return 0

            elif len(textElementValue) == 0:
                return 0

        return -1

    def updateTextValues(self, pTextElement, textElement):
        pTextElement.setLastTop(max(pTextElement.getLastTop(), textElement.getLastTop()))
        pTextElement.setFirstTop(min(pTextElement.getFirstTop(), textElement.getFirstTop()))
        textElementRight = textElement.getLeft() + textElement.getWidth()
        pTextElement.setWidth(textElementRight - pTextElement.getLeft())

    def updateMultilineBlockValues(self, multilineBlockObj, lineObj=None, secondMultilineBlockObj=None):
        # actualize multilineBlockObj values after adding a new line to the multilineBlockObj
        if lineObj is not None and secondMultilineBlockObj == None:

            end = multilineBlockObj.getEnd() + 1
            multilineBlockObj.setEnd(end)
            multilineBlockObj.setLeftmost(min(multilineBlockObj.getLeftmost(), lineObj.getLeftmost()))

            multilineBlockObj.setRightmost(max(multilineBlockObj.getRightmost(), lineObj.getRightmost()))

            multilineBlockObj.setMaxElements(max(multilineBlockObj.getMaxElements(), len(lineObj.getTextList())))

            usedSpace = multilineBlockObj.getUsedSpace() + lineObj.getUsedSpace()
            multilineBlockObj.setUsedSpace(usedSpace)

        elif secondMultilineBlockObj is not None and lineObj == None:
            # actualize mlb values after merging two mlbs
            multilineBlockObj.setLeftmost(min(multilineBlockObj.getLeftmost(), secondMultilineBlockObj.getLeftmost()))
            multilineBlockObj.setRightmost(max(multilineBlockObj.getRightmost(), secondMultilineBlockObj.getRightmost()))
            multilineBlockObj.setMaxElements(max(multilineBlockObj.getMaxElements(), secondMultilineBlockObj.getMaxElements()))
            multilineBlockObj.setUsedSpace(multilineBlockObj.getUsedSpace() + secondMultilineBlockObj.getUsedSpace())
            multilineBlockObj.setAvgDistance((multilineBlockObj.getAvgDistance() + secondMultilineBlockObj.getAvgDistance())/2)

    def setMultiLineBlockValues(self, multiLineBlockObj, lineObj, begin, page):
        multiLineBlockObj.setBegin(begin)
        multiLineBlockObj.setEnd(begin)
        multiLineBlockObj.setLeftmost(lineObj.getLeftmost())
        multiLineBlockObj.setRightmost(lineObj.getRightmost())
        multiLineBlockObj.setMaxElements(len(lineObj.getTextList()))
        multiLineBlockObj.setAvgDistance(0)
        multiLineBlockObj.setPage(page)
        multiLineBlockObj.setUsedSpace(lineObj.getUsedSpace())

    def createTextElement(self, xmlTextElementObj):

        value = self.__getTextNode(xmlTextElementObj)
        if value == None:
            value = ""
        top = int(xmlTextElementObj.get("top"))
        left = int(xmlTextElementObj.get("left"))
        width = int(xmlTextElementObj.get("width"))
        height = int(xmlTextElementObj.get("height"))
        font = int(xmlTextElementObj.get("font"))
        textFont = self.__fontsList[font]
        textSize = textFont.getSize()

        typ = "number"
        try:
            intOrNot = int(value)
            floatOrNot = float(value)
        except ValueError:
            typ = "text"

        formatList = xmlTextElementObj.findAll("b")
        secondFormatList = xmlTextElementObj.findAll("i")
        format = ""
        if len(formatList) > 0:
            format = "bold"

        elif len(secondFormatList) > 0:
            format = "italic"

        elif len(formatList) > 0 and len(secondFormatList.size) > 0:
            format = "bolditalic"

        return TextElement(value,top,left,width,height,font,format,typ)

    def __getTextNode(self, tag):
        """
            Get text in a given tag
        """
        text = ''
        for child in tag.contents:
            if isinstance(child, basestring):
                text += child                
            else:
                self.__getTextNode(child)

            return text

    def mergeMultilineBlock(self):
        b = 0
        begin = True
        stepsBackward = 0
        stepsForward = 0
        before = 0
        after = 0

        self.__removedElementsBefore = 0
        self.__removedElementsAfter = 0

        index=0
        while index < len(self.__multiLineBlocksList):
            secondMultilineBlock = self.__multiLineBlocksList[index]
            secondMultilineBlock.setBegin(secondMultilineBlock.getBegin() - self.__removedElementsBefore \
            - self.__removedElementsAfter)
            secondMultilineBlock.setEnd(secondMultilineBlock.getEnd() - self.__removedElementsBefore \
            - self.__removedElementsAfter)

            before = self.__removedElementsBefore
            after = self.__removedElementsAfter

            if index == 0:
                # first multiline block
                if (secondMultilineBlock.getBegin() -10) > 0:
                    stepsBackward = 10

                else:
                    stepsBackward = secondMultilineBlock.getBegin() - 1

                stepsForward = 0
                self.lineMerge(index, stepsBackward, stepsForward)
                secondMultilineBlock.setBegin(secondMultilineBlock.getBegin() - (self.__removedElementsBefore - before))
                secondMultilineBlock.setEnd(secondMultilineBlock.getEnd() - (self.__removedElementsBefore - before))

            elif index == (len(self.__multiLineBlocksList)-1):
            #last multiline block
                if (secondMultilineBlock.getEnd()+10) < len(self.__linesList):
                    stepsForward = 10

                else:
                    stepsForward = len(self.__linesList) - secondMultilineBlock.getEnd() -1

                stepsBackward = 0
                self.lineMerge(index, stepsBackward, stepsForward)

            else:
            # every other multiline block between the first and the last
                firstMultilineBlock = self.__multiLineBlocksList[index-1]
                thirdMultilineBlock = self.__multiLineBlocksList[index+1]

                stepsForward = thirdMultilineBlock.getBegin() - secondMultilineBlock.getEnd()-1
                stepsBackward = secondMultilineBlock.getBegin() - firstMultilineBlock.getEnd()-1

                if secondMultilineBlock.getPage() == thirdMultilineBlock.getPage() and \
                secondMultilineBlock.getPage() != firstMultilineBlock.getPage():
                    stepsBackward = 0
                    self.lineMerge(index, stepsBackward, stepsForward)

                elif secondMultilineBlock.getPage() == firstMultilineBlock.getPage() and \
                secondMultilineBlock.getPage() != thirdMultilineBlock.getPage():
                    stepsForward = 0
                    self.lineMerge(index, stepsBackward, stepsForward)

                elif secondMultilineBlock.getPage == firstMultilineBlock.getPage() and \
                secondMultilineBlock.getPage() == thirdMultilineBlock.getPage():
                    # if self.__multiLineBlocksList on the same page
                    self.lineMerge(index, stepsBackward, stepsForward)


                mergeWithBefore = False

                if (secondMultilineBlock.getBegin() - firstMultilineBlock.getEnd()) <= 3 and \
                secondMultilineBlock.getPage() == firstMultilineBlock.getPage() and \
                (abs(secondMultilineBlock.getMaxElements() - firstMultilineBlock.getMaxElements())) <=1:

                    firstMultilineBlock.setEnd(secondMultilineBlock.getEnd() - (self.__removedElementsBefore - before))
                    self.__multiLineBlocksList.pop(index)
                    mergeWithBefore = True
                    self.updateMultilineBlockValues(firstMultilineBlock, None, secondMultilineBlock)
                    index -= 1

                if (thirdMultilineBlock.getBegin() - secondMultilineBlock.getEnd()) <= 3 and \
                thirdMultilineBlock.getPage() == secondMultilineBlock.getPage() and  \
                abs(secondMultilineBlock.getMaxElements() - thirdMultilineBlock.getMaxElements()) <=1:

                    if mergeWithBefore == False:
                        secondMultilineBlock.setBegin(secondMultilineBlock.getBegin() - (self.__removedElementsBefore - before))
                        secondMultilineBlock.setEnd(thirdMultilineBlock.getEnd() - \
                        (self.__removedElementsBefore - before) - (self.__removedElementsAfter - after))
                        self.updateMultilineBlockValues(secondMultilineBlock, None, thirdMultilineBlock)
                        self.__multiLineBlocksList.pop(index+1)

                    else:
                        firstMultilineBlock.setEnd(thirdMultilineBlock.getEnd() - \
                        (self.__removedElementsBefore - before) - (self.__removedElementsAfter - after))
                        self.updateMultilineBlockValues(firstMultilineBlock, None, thirdMultilineBlock)
                        self.__multiLineBlocksList.pop(index+1)
            index += 1

    def lineMerge(self, position, stepsBack, stepsForward):
        multilineBlockObj = self.__multiLineBlocksList[position]
        firstLine = self.__linesList[multilineBlockObj.getBegin()]
        lastLine = self.__linesList[multilineBlockObj.getEnd()]
        count = 0
        mergeControl = True

        for pos in range(1, stepsBack+1):
            if mergeControl == True:

                previousLine = self.__linesList[multilineBlockObj.getBegin() - pos]
                storageList = firstLine.getTextList()

                topDistance = firstLine.getFirstTop() - previousLine.getBottom()

                for textElement in storageList:
                    for self.__nextTextElement in firstLine.getTextList():
                        leftDistance = abs(self.__nextTextElement.getLeft() - textElement.getLeft())
                        rightDistance = abs((self.__nextTextElement.getLeft() + self.__nextTextElement.getWidth()) \
                        - (textElement.getLeft() + textElement.getWidth()))
                        if topDistance < (textElement.getHeight()/2) and textElement.getTyp() ==  \
                        self.__nextTextElement.getTyp() and \
                        textElement.getTyp() == "text" and (leftDistance < 3 or rightDistance < 3):
                            stringValue = self.__nextTextElement.getValue() + " " + textElement.getValue()
                            textElement.setValue(stringValue)
                            textElement.setCountLines(textElement.getCountLines() + 1)
                            self.updateTextValues(textElement, self.__nextTextElement)
                            count += 1

                if count == len(previousLine.getTextList()):
                    firstLine.setTextList(storageList)
                    for textElement in firstLine.getTextList():
                        self.updateLineValues(textElement, firstLine)
                    self.__linesList.pop(multilineBlockObj.getBegin() - pos)
                    self.__removedElementsBefore += 1

                else:
                    mergeControl = False

            count = 0

        mergeControl = True

        for pos in range (1, stepsForward + 1):
            if mergeControl == True:
                nextLine = self.__linesList[multilineBlockObj.getEnd() + pos]
                storageList = lastLine.getTextList()

                topDistance = nextLine.getFirstTop() - lastLine.getBottom()

                for textElement in lastLine.getTextList():
                    for self.__nextTextElement in nextLine.getTextList():
                        leftDistance = abs(self.__nextTextElement.getLeft() - textElement.getLeft())
                        rightDistance = abs((self.__nextTextElement.getLeft() + self.__nextTextElement.getWidth()) \
                            - (textElement.getLeft() + textElement.getWidth()))

                        if topDistance < (textElement.getHeight()/2) and textElement.getTyp()  == self.__nextTextElement.getTyp() and \
                        textElement.getTyp() == "text" and ((leftDistance < 3) or (rightDistance < 3)):

                            stringValue = textElement.getValue() + " " + self.__nextTextElement.getValue()
                            textElement.setValue(stringValue)
                            textElement.setCountLines(textElement.getCountLines() + 1)
                            self.updateTextValues(textElement, self.__nextTextElement)
                            count += 1

                if count == len(nextLine.getTextList()):
                    lastLine.setTextList(storageList)
                    for textElement in lastLine.getTextList():
                        self.updateLineValues(textElement, lastLine)
                    self.__linesList.pop(multilineBlockObj.getEnd() + pos)
                    self.__removedElementsAfter += 1
                else:
                    mergeControl = False
                count = 0


