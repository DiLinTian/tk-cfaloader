#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/10/16 9:50
@ description:
    

'''

# import sgtk
# from sgtk.platform.qt import QtCore, QtGui
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import sys,os

class ShotProxyModel(QtGui.QSortFilterProxyModel):

    def __init__(self,parent = None):
        super(ShotProxyModel, self).__init__(parent)

    def filterAcceptsRow(self, source_row,source_parent):
        source_model = self.sourceModel()
        source_index = source_model.index(source_row,0,source_parent)
        row_count = source_model.rowCount(source_index)
        if row_count > 0:
            return True
        else:
            return super(ShotProxyModel, self).filterAcceptsRow(source_row,source_parent)
