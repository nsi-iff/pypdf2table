# -*- coding: utf-8 -*-

class GetOutputStringIOList:
    
    def getOutputList(self, outputFilePathList):
        stringIOList =[]
        for filePathString in outputFilePathList:
            file = open(filePathString)
            stringIOList.append(file.read())
            file.close()
        return stringIOList
