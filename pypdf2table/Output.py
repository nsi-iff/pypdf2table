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

import os
from TextElement import TextElement
from Table import Table
from Font import Font
from Column import Column
from GetOutputFilePathList import GetOutputFilePathList
from GetOutputStringIOList import GetOutputStringIOList

class Output:
    """Creates the output File"""
    def __init__(self,tableList=[], fontList=[], path=""):
        self.__tableList = tableList
        self.__fontList = fontList
        self.__path = path

        self.createStylesheet()
        self.createTablesDtd()


    def createStylesheet(self):
        """Creates the XML Stylesheet. that is, a XSL File that will define the table Layout"""

        stylesheetFile = open(self.__path + "/table_view.xsl", "w")
        #variable to keep the xml stylesheet (xsl file) information
        xslValue = "<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>\n" + \
        "<xsl:stylesheet xmlns:xsl=\"" + \
        "http://www.w3.org/1999/XSL/Transform\" version=\"1.0\">\n" + \
        "<xsl:output method=\"html\" />\n" + \
        "<xsl:template match=\"/\">" + \
        "<html>\n" + \
        "<body>\n" + \
        "<xsl:for-each select=\"tables/table\">\n" + \
        "<table border=\"1\">\n" +  \
        "<caption>\n" + \
        "<xsl:value-of select=\"title\"/>\n" + \
        "</caption>\n" + \
        "<xsl:for-each select=\"header/header_line\">\n" + \
        "<tr>\n" + \
        "<xsl:for-each select=\"header_element\">\n" + \
        "<th bgcolor=\"#ccdddd\" colspan=\"{@colspan}\">\n" + \
        "<xsl:value-of select=\".\" /> \n" + \
        "</th>\n" + \
        "</xsl:for-each>\n" + \
        "</tr>\n" + \
        "</xsl:for-each>\n" +  \
        "<xsl:for-each select=\"tbody/data_row\">\n" + \
        "<tr>\n" + \
        "<xsl:for-each select=\"cell\">\n" +  \
        "<td colspan=\"{@colspan}\">\n" +  \
        "<xsl:if test=\"@format='bold'\">\n" +  \
        "<b>\n" +  \
        "<xsl:value-of select=\".\" />\n" +  \
        "</b>\n" + \
        "</xsl:if>\n" + \
        "<xsl:if test=\"@format='italic'\">\n" + \
        "<i>\n" +  \
        "<xsl:value-of select=\".\" />\n" +  \
        "</i>\n" +  \
        "</xsl:if>\n" +  \
        "<xsl:if test=\"@format='bolditalic'\">\n" +  \
        "<b><i>\n" +  \
        "<xsl:value-of select=\".\" />\n" +  \
        "</i></b>\n" +  \
        "</xsl:if>\n" +  \
        "<xsl:if test=\"@format=''\">\n" +  \
        "<xsl:value-of select=\".\" />\n" +  \
        "</xsl:if>\n" +  \
        "</td>\n" +  \
        "</xsl:for-each>\n" +  \
        "</tr>\n" +  \
        "</xsl:for-each>\n" +  \
        "<BR>   </BR>\n" +  \
        "<BR>   </BR>\n" + \
        "<BR>   </BR>\n" +  \
        "</table>\n" +  \
        "</xsl:for-each>\n" +  \
        "</body>\n" +  \
        "</html>\n" + \
        "</xsl:template>\n" +  \
        "</xsl:stylesheet>\n" \


        stylesheetFile.write(xslValue)
        stylesheetFile.close()

    def createTablesDtd(self):
        """Creates a DTD File"""
        dtdFile = open(self.__path + "/tables.dtd", "w")
        dtdValue = "<?xml version=\"1.0\" encoding=\"iso-8859-1\"?>\n" + \
        "<!ELEMENT tables(table+,fontspec*)>\n" +  \
        "<!ELEMENT fontspec EMPTY>\n" + \
        "<!ATTLIST fontspec\n" + \
            "id CDATA #REQUIRED\n" + \
            "size CDATA #REQUIRED\n" + \
            "family CDATA #REQUIRED\n" +  \
            "color CDATA #REQUIRED\n" + \
        ">\n" + \
        "<!ELEMENT table (header,tbody)>\n" + \
        "<!ELEMENT header (header_element)*>\n" + \
        "<!ELEMENT header_element (#PCDATA)>\n" +  \
        "<!ATTLIST header_element\n" + \
            "id CDATA #REQUIRED\n" + \
            "sh CDATA #REQUIRED\n" +  \
            "font CDATA #REQUIRED\n" +  \
            "colspan CDATA #REQUIRED\n" + \
        ">\n" + \
        "<!ELEMENT tbody (data_row)*>\n" + \
        "<!ELEMENT data_row (cell)*>\n" +  \
        "<!ELEMENT cell (#PCDATA)>\n" + \
        "<!ATTLIST cell\n" + \
            "sh CDATA #REQUIRED\n" + \
            "font CDATA #REQUIRED\n" + \
            "colspan CDATA #REQUIRED\n" + \
            "format CDATA #REQUIRED\n" + \
        ">\n"

        dtdFile.write(dtdValue)
        dtdFile.close()

    def createOutput(self):
        """Creates a HTML file for each table"""
        tableNumber = 1
        self.__outputFilesList = []
        for tableObj in self.__tableList:
            #creating the output files
            outputFilePathString = self.__path + "/table_" + str(tableNumber) + ".xml"
            outputFile = open(outputFilePathString, "w")
            outputFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>" + "\n")
            outputFile.write("<?xml-stylesheet href=\"table_view.xsl\" type=\"text/xsl\" ?>" + "\n")
            outputFile.write("<tables>" + "\n")
            #Fonts
            for fontObj in self.__fontList:
                outputFile.write("<fontspec id=\"" + fontObj.getFontId() + \
                "\" size=\"" + str(fontObj.getSize()) + "\" family=\"" + \
                fontObj.getFamily() + "\" color=\"" + fontObj.getColor() + "\"/>")
            cellsOnColumn = 0
            outputFile.write("<table>" + "\n")
            outputFile.write("<title>" + "TABLE ON PAGE " + tableObj.getPage() + "</title>" +"\n")
            outputFile.write("<header>" + "\n")

            for j in range(0, tableObj.getDatarowBegin()):
                p = 0
                outputFile.write("<header_line>" + "\n")
                while p < len(tableObj.getColumnList()):
                    columnObj = tableObj.getColumnListElement(p)
                    cellsOnColumn = len(columnObj.getCellsList())
                    columnObj.setHeader(p+j)
                    textElementObj = columnObj.getCellsListElement(j)
                    outputFile.write("<header_element id=\"" + str(p+j) + "\" sh=\"" + str(columnObj.getHeader()))
                    outputFile.write("\" font=\"" + str(textElementObj.getFont()) + "\" colspan=\"" + \
                    str(textElementObj.getColspan()) + "\">" + "\n")
                    outputFile.write("<![CDATA[")
                    if textElementObj.getValue() != "null":
                        outputFile.write(textElementObj.getValue())
                    outputFile.write("]]>" + "\n")
                    outputFile.write("</header_element>" + "\n")
                    p = p + int(textElementObj.getColspan())
                outputFile.write("</header_line>" + "\n")
            outputFile.write("</header>" + "\n")
            outputFile.write("<tbody>" + "\n")

            for counter in range(tableObj.getDatarowBegin(), cellsOnColumn):

                outputFile.write("<data_row>" + "\n")
                k = 0
                while k < len(tableObj.getColumnList()):
                    columnObj = tableObj.getColumnListElement(k)
                    try:
                        textElement = columnObj.getCellsListElement(counter)
                    except:
                        break
                    outputFile.write("<cell sh=\"" + str(columnObj.getHeader()) + "\" font=\"" + str(textElement.getFont()))
                    outputFile.write("\" colspan=\"" + str(textElement.getColspan()) + "\" format=\"" + textElement.getFormat() + "\">" + "\n")
                    outputFile.write("<![CDATA[")
                    if textElement.getValue() != "null":
                        outputFile.write(textElement.getValue())                        
                    outputFile.write("]]>" + "\n")
                    outputFile.write("</cell>" + "\n")
                    k = k + textElement.getColspan()



                outputFile.write("</data_row>" + "\n")

            outputFile.write("</tbody>" + "\n")
            outputFile.write("</table>" + "\n")
            outputFile.write("</tables>" + "\n")
            outputFile.close()
            tableNumber += 1
            os.system('xmlto -x "' + os.path.join(self.__path, 'table_view.xsl') +  '" -o  ' + self.__path + ' html-nochunks ' + outputFilePathString + ' --skip ')
            os.system("rm " + os.path.join(self.__path, "*.xml"))
            self.__outputFilesList.append(outputFilePathString.replace(".xml", ".html"))
        os.system("rm " + os.path.join(self.__path, "*.dtd"))
        os.system("rm " + os.path.join(self.__path, "table_view.xsl"))


    def setOutputType(self, outputTypeObj):
        self.__outputType = outputTypeObj

    def getOutputList(self):
         return self.__outputType.getOutputList(self.__outputFilesList)
