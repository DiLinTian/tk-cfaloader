#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2020/1/13 15:22
@ description:
    

'''
import sgtk
from sgtk.platform.qt import QtCore, QtGui
# from PySide import QtCore, QtGui
class CreateFileTypeCheckUI(QtGui.QWidget):
    FileTypeState = QtCore.Signal(dict)

    def __init__(self, file_type,parent=None):
        super(CreateFileTypeCheckUI, self).__init__(parent)
        self.setFileType(file_type)
        self.setupUi()
    def setupUi(self):
        self._layout = QtGui.QHBoxLayout()
        self.check_ui_list = []
        _keys = self._file_type.keys()
        _keys.sort()
        for k in _keys:
            _checkui = QtGui.QCheckBox(k, self)
            _checkui.clicked.connect(self.emit_type_state)
            _checkui.setObjectName(self._file_type[k])
            self.check_ui_list.append(_checkui)
            self._layout.addWidget(_checkui)
        self.setLayout(self._layout)
        # self.check_ui_list[0].setCheckState(QtCore.Qt.CheckState.Checked)

    def emit_type_state(self):
        _check_type = self.getCheckedType()
        self.FileTypeState.emit(_check_type)
    def getCheckedType(self):
        _check_type = []
        for check in self.check_ui_list:
            if check.isHidden():
                continue
            if check.isChecked():
                _check_type.append(check.objectName())
        return _check_type

    def _type_list(self):
        return [v for k,v in self._file_type.iteritems()]
    def getUilist(self):
        return self.check_ui_list

    def setCheckUiState(self,):
        for check in self.check_ui_list:
            if check.isHidden():
                check.setChecked(QtCore.Qt.Unchecked)
            else:
                check.setChecked(QtCore.Qt.Checked)


    def setFileType(self,file_type):
        if not file_type:
            return
        if not isinstance(file_type,dict):
            return
        self._file_type = file_type
