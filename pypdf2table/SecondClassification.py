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
from Output import Output
from MyNode import MyNode
from Table import Table
from MultilineBlock import MultilineBlock
from Line import Line
from Font import Font
from TextElement import TextElement
from Column import Column



class SecondClassification:
    """This is the second part of the table recognition"""
    def __init__(self, path, fontsList=[], fontCounterList=[], linesList=[], multiLineBlocksList=[]):
        
        self.__path = path
        self.__fontsList = fontsList
        self.__fontCounterList = fontCounterList
        self.__linesList = linesList
        self.__multiLineBlocksList = multiLineBlocksList
        self.__tableList = []


    def run(self):
        self.decomposeTables()
        return self.__tableList, self.__fontsList, self.__path
        

    def decomposeTables(self):
        
        for multiLineBlock in self.__multiLineBlocksList:
            linesBefore = 0
            lineCount = 0
            if (multiLineBlock.getEnd() - multiLineBlock.getBegin()) >= 2:
                # multiline blocks with less than 3 lines will be ignored
                myRootNode = MyNode(level = -1, content = "root") 
                for begin in range(int(multiLineBlock.getBegin()), int(multiLineBlock.getEnd())+1):
                    line = self.__linesList[begin]
                    for textElement in line.getTextList():
                        self.insertIntoTree(textElement, myRootNode, linesBefore)
                    linesBefore += 1
                # end of while (begin <= multiLineBlock.getEnd())

                #self.printTree(myRootNode)
                newTable = Table()
                self.convertToTable(myRootNode, None, newTable.getColumnList(), linesBefore)
                for pos in range(0, len(newTable.getColumnList())-1):
                    firstColumn =  newTable.getColumnListElement(pos)
                    secondColumn = newTable.getColumnListElement(pos+1)

                    nextColumn = firstColumn.clone()
                    if firstColumn.getLeft() <= secondColumn.getLeft() and \
                       firstColumn.getRight() >= secondColumn.getLeft():
                    # merge columns because they overlap
                        merge = True
                        for posCounter in range(0, len(firstColumn.getCellsList())):

                            firstTextElement = firstColumn.getCellsListElement(posCounter)
                            secondTextElement = secondColumn.getCellsListElement(posCounter)
                            nextTextElement = nextColumn.getCellsListElement(posCounter)

                            if firstTextElement.getValue() == "null" or secondTextElement.getValue() == "null":	
                                newValue = ""
                                if firstTextElement.getValue() != "null":
                                    nextTextElement.setValue(firstTextElement.getValue())
                                    if firstTextElement.getColspan() > 1:
                                        nextTextElement.setColspan(nextTextElement.getColspan() -1)
                                    else:
                                        self.updateColumnValues(nextColumn, firstTextElement)
                                else:
                                    nextTextElement.setValue(secondTextElement.getValue())
                                    if (secondTextElement.getColspan() > 1):
                                        nextTextElement.setColspan(nextTextElement.getColspan() -1)
                                    else:
                                        self.updateColumnValues(nextColumn,secondTextElement)

                            else:
                                merge = False
                                break

                        if merge == True:
                            newTable.insertColumnAt(pos, nextColumn)
                            newTable.removeColumnAt(pos+1)
                            newTable.removeColumnAt(pos+1)


                newTable.setDatarowBegin(0) #data_row_begin

                header = True
                sumTotal = 0
                if len(newTable.getColumnList()) > 0:
                    firstColumn = newTable.getColumnListElement(0)
                    for pos in range(0, len(firstColumn.getCellsList())):
                        if header == True:
                            for counter in range(0, len(newTable.getColumnList())):
                                currentColumn = newTable.getColumnListElement(counter)
                                textElement = currentColumn.getCellsListElement(pos)

                                if textElement.isArtificial() == False:
                                    sumTotal = sumTotal + textElement.getColspan()
                                    if sumTotal >= multiLineBlock.getMaxElements():
                                        header = False
                                        newTable.setDatarowBegin(pos+1)



                newTable.setPage(multiLineBlock.getPage())
                self.__tableList.append(newTable)
                
                
                
    def insertIntoTree(self, textElement, myNode, level):
        
        if myNode.getContent() == "null":
            if self.insertIntoTree(textElement, myNode.getNodeListElement(0), level) == True:
                return True

        else:
            if self.inBoundaries(textElement.getLeft(), textElement.getRight(), myNode.getLeft(), myNode.getRight()) == True or \
            myNode.getContent() == "root":
                pos = 0
                for nextNode in myNode.getNodeList():
                  # it was textElement.getLeft() > nextNode.getRight() which means completely on the right side
                    if textElement.getLeft() > nextNode.getLeft():
                        pos += 1                  	
                    if (self.inBoundaries(textElement.getLeft(), textElement.getRight(), nextNode.getLeft(),
                    nextNode.getRight()) == True and nextNode.getLevel() < level) or nextNode.getContent() == "null":
                        if self.insertIntoTree(textElement, nextNode, level) == True:
                            return True


                for posCounter in range(myNode.getLevel(), level-1):
                    dummyNode = MyNode(level = posCounter+1, content = "null", \
                    textElement = textElement)
                    myNode.insertNodeAt(pos, dummyNode)
                    myNode = dummyNode
                    pos = 0

                currentNode = MyNode(level = level, textElement = textElement)
                myNode.insertNodeAt(pos, currentNode)
                return True

        return False
        
    def printTree(self, myNodeObj):

        for node in myNodeObj.getNodeList():           
            self.printTree(node)

        
    def convertToTable(self, myNodeObj, columnObj, listObj, length):
        
        if columnObj == None:
            #root node
            spanning = 0
            for node in myNodeObj.getNodeList():
                newColumn = Column()
                listObj.append(newColumn)
                spanning += self.convertToTable(node, newColumn, listObj, length)
            return spanning

        else:
            #not root node
            pos = 0
            if myNodeObj.getContent() != "null":
                columnObj.addCell(myNodeObj.getTextElement())
                pos = len(columnObj.getCellsList())
                if myNodeObj.getTextElement().getColspan() == 1:
                    self.updateColumnValues(columnObj, myNodeObj.getTextElement())

            else:
                textElement = TextElement()
                columnObj.addCell(textElement)
                pos = len(columnObj.getCellsList())

            if len(myNodeObj.getNodeList()) >= 1:
                columnClone = columnObj.clone()
                spanning = 0
                spanning += self.convertToTable(myNodeObj.getNodeElement(0), columnObj, listObj, length)
                for posCounter in range(1, len(myNodeObj.getNodeList())):
                    newColumn = Column()
                    newColumn.setCellsList(columnClone.getCellsList())
                    listObj.append(newColumn)
                    spanning +=self.convertToTable(myNodeObj.getNodeElement(posCounter),\
                    newColumn, listObj, length)
                    
                textElement = columnObj.getCellsListElement(pos-1)
                textElement.setColspan(spanning)

                return spanning

            else:
                # no children means that we are at the leaf of a branch
                while len(columnObj.getCellsList()) < length:
                    textElement = TextElement()
                    columnObj.addCell(textElement)
                return 1

    def updateColumnValues(self, columnObj, textElement):

        if columnObj.getLeft() ==  -1:
            columnObj.setLeft(textElement.getLeft())

        else:
            min(columnObj.getLeft(),textElement.getLeft())
        
        columnObj.setRight(max(columnObj.getRight(),(textElement.getLeft() + textElement.getWidth())))

    def updateColumnValuesWithAnotherColumn(self, firstColumn, secondColumn):
        firstColumn.setLeft(min(firstColumn.getLeft(), secondColumn.getLeft()))
        firstColumn.setRight(max(firstColumn.getRight(), secondColumn.getRight()))
    
    def inBoundaries(self, textElementLeft, textElementRight, nodeLeft, nodeRight):
        if (textElementLeft >= nodeLeft and textElementRight <= nodeRight) or \
        (textElementLeft >= nodeLeft and textElementLeft <= nodeRight and \
        textElementRight > nodeRight) or (textElementLeft < nodeLeft and \
        textElementRight >= nodeLeft and textElementRight <= nodeRight) or \
        (nodeLeft >= textElementLeft and nodeRight <= textElementRight):
            return True
       
        return False


