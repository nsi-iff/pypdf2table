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

from TextElement import TextElement

class MyNode:

    def __init__(self, level=None, content="null", textElement=None):
        self.__content = content
        self.__level = level
        self.__nodeList = []
        self.__textElement = textElement
        self.__left = None
        self.__right = None
        
        if textElement is not None:
            self.__left = textElement.getLeft()
            self.__right = textElement.getRight()

            if content == "null":
                self.__content = textElement.getValue()

        
    
    
            
    def insertNodeAt(self, pos, obj):
        self.__nodeList.insert(pos, obj)
        
    def setLevel(self, level):
        self.__level = level
        
    def addNode(self, node):
        self.__nodeList.append(node)
    
    def setLeft(self, left): 
        self.__left = left
        
    def setRight(self, right):
        self.__right = right
        
    def setTextElement(self, textElement):
        self.__ = textElement
    
    def setContent(self, content):
        self.__content = content
        
        
    def getLevel(self):
        return self.__level
        
    def getNodeList(self):
        return self.__nodeList
    
    def getLeft(self): 
        return self.__left
        
    def getRight(self,):
        return self.__right
        
    def getTextElement(self): 
        return self.__textElement
        
    def getNodeElement(self, pos): 
        return self.__nodeList[pos]
    
    def getContent(self):
        return self.__content
    
      



