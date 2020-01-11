#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/25 11:10
@ description:
    

'''
import os,sys
from PySide import QtCore, QtGui
# import sgtk
# from sgtk.platform.qt import QtCore, QtGui
class ShotTabWidget(QtGui.QTabWidget):
    def __init__(self,parent = None):
        super(ShotTabWidget, self).__init__(parent)

        self._layout = QtGui.QGridLayout(self)
        self._shot_tab = QtGui.QWidget()
        self._shot_tab_layout = QtGui.QGridLayout(self._shot_tab)

        self.addTab(self._shot_tab,"Shot")

        self.setLayout(self._layout)




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = ShotTabWidget()
    win.show()
    sys.exit(app.exec_())

