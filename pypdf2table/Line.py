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

from TopComparatorForTexts import TopComparatorForTexts
class Line:
    
    def __init__(self):
    
        self.__textList = []
        self.__top = None
        self.__bottom = None
        self.__height = None
        self.__leftmost = None
        self.__rightmost = None
        self.__font = None
        self.__lastTop = None
        self.__firstTop = None
        self.__usedSpace = None
        self.__typ = None
        
    def sortTextList(self, comparator=None):
        self.__textList.sort(cmp=comparator)
        
    def removeTextElement(self,pos=-1):
        self.__textList.pop(pos)
    
    #first, the sets/adds methods
    def addText(self, text):
        self.__textList.append(text)
    
    def setTextList(self, textList):
        self.__textList = textList
    
    def setTop(self, top):
        self.__top = top
        
    def setBottom(self, bottom):
        self.__bottom = bottom
        
    def setHeight(self, height):
        self.__height = height
        
    def setLeftmost(self, leftmost): 
        self.__leftmost = leftmost
        
    def setRightmost(self, rightmost):
        self.__rightmost = rightmost
    
    def setFont(self, font):
        self.__font = font
        
    def setLastTop(self, lastTop): 
        self.__lastTop = lastTop
        
    def setFirstTop(self, firstTop):
        self.__firstTop = firstTop
    
    def setUsedSpace(self, usedSpace):
        self.__usedSpace = usedSpace
        
    def increaseUsedSpace(self, usedSpace):
        self.__usedSpace += usedSpace   
    
    def setTyp(self, typ): 
        self.__typ = typ
        
    #now, the gets
    
    def getTextList(self):
        return self.__textList

    def getTextElement(self, pos=0):
        return self.__textList[pos]
    
    def getTop(self):
        return int(self.__top)
        
    def getBottom(self):
        return int(self.__bottom) 
        
    def getHeight(self):
        return int(self.__height)
        
    def getLeftmost(self): 
        return int(self.__leftmost) 
        
    def getRightmost(self):
        return int(self.__rightmost)
    
    def getFont(self):
        return self.__font
        
    def getLastTop(self): 
        return self.__lastTop
        
    def getFirstTop(self):
        return self.__firstTop
    
    def getUsedSpace(self):
        return self.__usedSpace
    
    def getTyp(self):
        return self.__typ

