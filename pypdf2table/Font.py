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

class Font:

    def __init__(self, page=None, fontId=None, size=None, family=None, color=None):
        self.__page = page
        self.__fontId = fontId
        self.__size = size   
        self.__family = family
        self.__color = color
    
    def setPage(self, page):
        self.__page = page
    def setFontId(self, fontId):
        self.__fontId = fontId
    def setSize(self, size):
        self.__size = size
        
    def setFamily(self, family):
        self.__family = family
        
    def setColor(self, color): 
        self.__color = color
        
    #gets   
        
    def getPage(self):
        return self.__page
        
    def getFontId(self):
        return self.__fontId
        
    def getSize(self):
        return int(self.__size)
        
    def getFamily(self):
        return self.__family
        
    def getColor(self):
        return self.__color

