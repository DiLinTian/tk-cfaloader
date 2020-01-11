#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/24 9:54
@ description:
    

'''

# import sgtk
# from sgtk.platform.qt import QtCore, QtGui
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import sys,os

class CfaLoaderShotViewItemModel(QtCore.QAbstractItemModel):
    sortRole = QtCore.Qt.UserRole + 99
    filterRole = QtCore.Qt.UserRole + 101
    def __init__(self,item,parent = None):
        super(CfaLoaderShotViewItemModel, self).__init__(parent)
        self._rootNode = item
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()
    def columnCount(self, parent):
        return 1
    def flags(self,index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def data(self,index,role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return node.name()

        if role == self.filterRole:
            return node.name()

        if role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(QtGui.QPixmap(node.icon()))
    # def headerData(self,section,orientation,role):
    #     if role == QtCore.Qt.DisplayRole:
    #         if section == 0:

    def index(self,row,column,parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row,column,childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self,index):
        node = self.getNode(index)
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(),0,parentNode)
    def getNode(self,index):
        if index.isValid():
            node = index.internalPointer()
            if node :
                return node
        return self._rootNode



