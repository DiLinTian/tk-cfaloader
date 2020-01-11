#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/25 10:47
@ description:
    

'''
# import sgtk
# from sgtk.platform.qt import QtCore, QtGui
from PySide import QtCore, QtGui

class ShotTreeview(QtGui.QTreeView):
    def __init__(self,parent = None):
        super(ShotTreeview, self).__init__(parent)
