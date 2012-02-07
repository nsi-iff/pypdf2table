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

class Column:
    
    def __init__(self, left=-1, right=-1):
        
        self.__cellsList = []
        self.__left = left
        self.__right = right
        self.__emptyCells = 0
        self.__header = -1      
    
    def addCell(self, cell):
        self.__cellsList.append(cell)
    
    def setLeft(self, left):
        self.__left = left
    
    def setRight(self, right):
        self.__right = right
    
    def setEmptyCells(self, emptyCells):
        self.__emptyCells = emptyCells
    
    def setHeader(self, header):
        self.__header = header
    
    def setCellsList(self, cellsList):
        self.__cellsList = cellsList
    
    def getCellsList(self):
        return self.__cellsList
        
    def getCellsListElement(self, pos=0):
        return self.__cellsList[pos]
    
    def getLeft(self):
        return int(self.__left)
    
    def getRight(self):
        return int(self.__right)
    
    def getEmptyCells(self):
        return self.__emptyCells
        
    def getHeader(self):
        return self.__header     
      
    
    def clone(self):
        columnObj = Column(self.getLeft(), self.getRight())
        columnObj.setCellsList(self.getCellsList())
        
        return columnObj
