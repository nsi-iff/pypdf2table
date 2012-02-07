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
import fileMover
from FirstClassification import FirstClassification
from Output import Output
from GetOutputFilePathList import GetOutputFilePathList
from GetOutputStringIOList import GetOutputStringIOList


class ExecuteConverter:
    def __init__(self):
        self.__resultTuple = None

    def extractTables(self, path, target):
        """
            Starts the table extraction. Using only this method, nothing will be returned,
            but the HTML output Files will be created in the specified output folder.
        """
        try:
            os.mkdir(target)
        except OSError:
            pass
        os.chdir(target)
        self.__dtdFile = open(target + "/pdf2xml.dtd", "w")
        self.buildDtd()
        self.__cmdLine = "pdftohtml -xml " + path
        print(self.__cmdLine)
        os.system(self.__cmdLine)
        xmlFile = os.path.basename(path).rstrip(".pdf") + ".xml"
        fileMover.moveXmlFile(path = path, target = target)

        #starting the extraction
        firstClassification = FirstClassification(target)
        self.__resultTuple = firstClassification.run(target + "/" + xmlFile)

        tableList = self.__resultTuple[0]
        fontsList = self.__resultTuple[1]
        path = self.__resultTuple[2]

        self.__outputObj = Output(tableList, fontsList, path)
        self.__outputObj.createOutput()

    def getTableList(self, outputTypeObj = GetOutputStringIOList()):
        """
            Return a list. The output type depends of the parameter.
            The default return type is a list of stringIO's containing the content of
            the generate HTML output files
        """
        self.__outputObj.setOutputType(outputTypeObj)
        outputFilesList = self.__outputObj.getOutputList()

        return outputFilesList

    def buildDtd(self):
        dtd = "<?xml version=\"1.0\" encoding=\"iso-8859-1\"?>\n" + \
            "<!ELEMENT pdf2xml (page+,line*,fontspec*)>\n" + \
            "<!ELEMENT page (fontspec*, text*)>\n" + \
            "<!ATTLIST page\n" + \
                "number CDATA #REQUIRED\n" + \
                "position CDATA #REQUIRED\n" + \
                "top CDATA #REQUIRED\n" + \
                "left CDATA #REQUIRED\n" + \
                "height CDATA #REQUIRED\n" + \
                "width CDATA #REQUIRED\n" + \
            ">\n" + \
            "<!ELEMENT fontspec EMPTY>\n" + \
            "<!ATTLIST fontspec\n" + \
                "id CDATA #REQUIRED\n" + \
                "size CDATA #REQUIRED\n" + \
                "family CDATA #REQUIRED\n" + \
                "color CDATA #REQUIRED\n" + \
            ">\n" + \
            "<!ELEMENT text (#PCDATA | b | i)*>\n" + \
            "<!ATTLIST text\n" + \
                "top CDATA #REQUIRED\n" + \
                "left CDATA #REQUIRED\n" + \
                "width CDATA #REQUIRED\n" + \
                "height CDATA #REQUIRED\n" + \
                "font CDATA #REQUIRED\n" + \
            ">\n" + \
            "<!ELEMENT b (#PCDATA)>\n" + \
            "<!ELEMENT i (#PCDATA)>\n" + \
            "<!ELEMENT line (text+)>\n" + \
            "<!ATTLIST line\n" + \
                "typ CDATA #REQUIRED\n" + \
                "top CDATA #REQUIRED\n" + \
                "left CDATA #REQUIRED\n" + \
                "font CDATA #REQUIRED\n" + \
            ">"
        self.__dtdFile.write(dtd)
        self.__dtdFile.close()


