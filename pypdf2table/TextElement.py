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

class TextElement:

    def __init__(self, value="null", top=None, left=None, width=None, height=None,                 font=None,format="", typ=None):
        
        self.__value = value
        self.__top = top
        self.__left = left
        self.__width = width
        self.__height = height
        self.__font = font
        self.__format = format
        self.__typ = typ
        self.__elementList = []
        self.__lastTop = top
        self.__firstTop = top
        self.__countLines = 1
        self.__colspan = 1
        
        if value == "null":
            self.__artificial = True
            self.__right = None
        else:
            self.__artificial = False
            self.__right = left + width
        
        
        

    def clone(self):
        """As the name suggests, clone the object itself"""
        textElement = TextElement(self.__value, self.__top, self.__left, self.__width,
                                  self.__height, self.__font, self.__format, self.__typ)
                                  
        return textElement
        
    def isArtificial(self):
        return self.__artificial
        
    def sortElementList(self, comparator=None):
        self.__elementList.sort(cmp=comparator)
        

    def addElement(self, element=None):
        self.__elementList.append(element)
        
    def setElementList(self, elementList): 
        self.__elementList =  elementList
        
    def setValue(self, value):
        self.__value = value
        
    def setFont(self, font):
        self.__font = font
        
    def setTop(self, top): 
        self.__top = top
        
    def setLeft(self, left): 
        self.__left = left
    
    def setRight(self, right):
        self.__right = right
    
    def setWidth(self, width):
        self.__width = width
    
    def setFormat(self, format):
        self.__format = format
    
    def setFirstTop(self, firstTop): 
        self.__firstTop = firstTop
        
    def setLastTop(self, lastTop): 
        self.__lastTop = lastTop
        
    def setCountLines(self, countLines):
        self.__countLines = countLines
        
    def setColspan(self, colspan):
        self.__colspan = colspan

    def getValue(self):
        if type(self.__value) is unicode:
            return self.__value.encode('utf-8')
        return self.__value
        
    def getFont(self):
        return self.__font
        
    def getTop(self): 
        return int(self.__top)
        
    def getLeft(self): 
        return int(self.__left)
    
    def getRight(self):
        return self.__right
        
    def getHeight(self): 
        return int(self.__height)
        
    def getWidth(self): 
        return int(self.__width)
        
    def getFirstTop(self):
        return int(self.__firstTop)
        
    def getLastTop(self): 
        return int(self.__lastTop)
    
    def getElementList(self):
        return self.__elementList
    
    def getTyp(self):
        return self.__typ
    
    def getCountLines(self):
        return self.__countLines
    
    def getColspan(self):
        return self.__colspan
    
    def getFormat(self):
        return self.__format



