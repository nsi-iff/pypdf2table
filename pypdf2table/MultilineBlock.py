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

class MultilineBlock:

    def __init__(self, begin=None, end=None, leftMost=None, rightMost=None, maxElements=None, avgDistance=None, page=None, usedSpace=0):
        
        self.__begin = begin
        self.__end = end
        self.__leftmost = leftMost
        self.__rightmost = rightMost
        self.__maxElements = maxElements
        self.__avgDistance = avgDistance
        self.__page = page
        self.__usedSpace = usedSpace

    def setBegin(self, begin):
        self.__begin = begin
    
    def setEnd(self, end):
        self.__end = end
    
    def setLeftmost(self, leftMost):
        self.__leftMost = leftMost
        
    def setRightmost(self, rightMost): 
        self.__rightMost = rightMost
        
    def setMaxElements(self, maxElements): 
        self.__maxElements = maxElements
    
    def setAvgDistance(self, avgDistance): 
        self.__avgDistance = avgDistance
        
    def setPage(self, page): 
        self.__page = page
        
    def setUsedSpace(self, usedSpace): 
        self.__usedSpace = usedSpace
        
    #gets
        
    def getBegin(self):
        return self.__begin
    
    def getEnd(self):
        return self.__end
    
    def getLeftmost(self):
        return self.__leftMost
        
    def getRightmost(self): 
        return self.__rightMost
        
    def getMaxElements(self): 
        return self.__maxElements
    
    def getAvgDistance(self): 
        return self.__avgDistance
        
    def getPage(self): 
        return self.__page
        
    def getUsedSpace(self): 
        return self.__usedSpace
    
    



