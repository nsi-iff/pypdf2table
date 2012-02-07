# -*- coding: utf-8 -*-
import shutil

def moveXmlFile(path, target):
    """workarounding a pdftohtml 0.36 bug"""
    try:
        shutil.move(path.rstrip(".pdf") + ".xml", target)
    except IOError:
        pass
