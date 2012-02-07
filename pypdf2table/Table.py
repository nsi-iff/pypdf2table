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

from Column import Column

class Table:

    def __init__(self, page=None, datarowBegin=None, title=None):
        
        self.__columnList = []
        self.__page = page
        self.__datarowBegin = datarowBegin
        self.__title = title
        
    def clone(self):
        table = Table()
        table.setColumnList(self.__columnList)
        table.setPage(self.__page)
        table.setDatarowBegin(self.__datarowBegin)
        
        return table
        
    def addColumn(self, column):
        self.__columnList.append(column)
        
    def insertColumnAt(self, pos, obj):
        self.__columnList.insert(pos, obj)
        
    def removeColumnAt(self, pos):
        self.__columnList.pop(pos)        
        
    def setColumnList(self, columnList):
        self.__columnList = columnList
    
    def setPage(self, page):
        self.__page = page
        
    def setDatarowBegin(self, datarowBegin): 
        self.__datarowBegin = datarowBegin
        
    def getPage(self): 
        return self.__page

    def getDatarowBegin(self): 
        return self.__datarowBegin
        
    def getColumnList(self):
        return self.__columnList
        
    def getColumnListElement(self,position=0): 
        return self.__columnList[position]
        
       

