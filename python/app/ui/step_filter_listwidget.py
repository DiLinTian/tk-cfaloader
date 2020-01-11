#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/10/14 15:35
@ description:
    

'''
# import sgtk
# from sgtk.platform.qt import QtCore, QtGui
from PySide import QtCore, QtGui

class StepFilterWidget(QtGui.QListWidget):

    StepChanged = QtCore.Signal(list)
    def __init__(self,items = [],parent = None):

        super(StepFilterWidget, self).__init__(parent)
        self.setObjectName("step_filter_widget")
        self._items_data = items
        self.addItems(self._items_data)
        self.setInitState()
        self._is_related_color = QtGui.QColor("#6d71ad")
        self._unrelated_check_color = QtGui.QColor("#dadada")
        self._unrelated_uncheck_color = QtGui.QColor("#89898b")
        self._related_step = list()
    def setItemsState(self,row,state = QtCore.Qt.Checked):
        self.item(row).setCheckState(state)
    def setItemInitFlags(self,row):
        self.item(row).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
    def setInitState(self):
        count = self.count()
        for i in range(count):
            self.setItemInitFlags(i)
            self.setItemsState(i, QtCore.Qt.Unchecked)
        return True

    def getItemsData(self):
        count = self.count()
        state = QtCore.Qt.Checked
        item_data = []
        for i in range(count):
            current_item = self.item(i)
            if current_item.checkState() == state:
                item_data.append(current_item.data(QtCore.Qt.DisplayRole))
        return item_data
    def setRelatedStep(self,related_step):
        self._related_step = related_step
    def mouseReleaseEvent(self, event):
        super(StepFilterWidget, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.StepChanged.emit(self.getItemsData())
            current_item = self.itemAt(event.pos())
            self.checkItemState(current_item)
    def checkItemState(self,current_item):
        if current_item is None:
            return
        state = current_item.checkState()
        _step = current_item.text()
        if _step in self._related_step:
            current_item.setForeground(self._is_related_color)
        else:
            if state == QtCore.Qt.Unchecked:
                current_item.setForeground(self._unrelated_uncheck_color)
            elif state == QtCore.Qt.Checked:
                current_item.setForeground(self._unrelated_check_color)

    def setItemTextColor(self,item,color):
        item.setForeground(color)

