#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/25 10:50
@ description:
    

'''
# import sgtk
# from sgtk.platform.qt import QtCore, QtGui
from PySide import QtCore, QtGui

class AssetsListview(QtGui.QListView):
    def __init__(self, parent=None):
        super(AssetsListview, self).__init__(parent)
