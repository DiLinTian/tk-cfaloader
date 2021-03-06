# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_dialog.ui'
#
# Created: Mon Jan 13 14:54:46 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(944, 845)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.shot_tree_layout = QtGui.QGridLayout(self.layoutWidget)
        self.shot_tree_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.shot_tree_layout.setContentsMargins(0, 0, 0, 0)
        self.shot_tree_layout.setObjectName("shot_tree_layout")
        self.filter_layout = QtGui.QVBoxLayout()
        self.filter_layout.setObjectName("filter_layout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.step_filter_lab = QtGui.QLabel(self.layoutWidget)
        self.step_filter_lab.setObjectName("step_filter_lab")
        self.horizontalLayout_2.addWidget(self.step_filter_lab)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.filter_layout.addLayout(self.horizontalLayout_2)
        self.shot_tree_layout.addLayout(self.filter_layout, 2, 0, 1, 1)
        self.shot_tab_lay = QtGui.QVBoxLayout()
        self.shot_tab_lay.setObjectName("shot_tab_lay")
        self.shot_tab_widget = QtGui.QTabWidget(self.layoutWidget)
        self.shot_tab_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.shot_tab_widget.setTabPosition(QtGui.QTabWidget.North)
        self.shot_tab_widget.setObjectName("shot_tab_widget")
        self.tab_shot = QtGui.QWidget()
        self.tab_shot.setMinimumSize(QtCore.QSize(0, 0))
        self.tab_shot.setObjectName("tab_shot")
        self.gridLayout = QtGui.QGridLayout(self.tab_shot)
        self.gridLayout.setObjectName("gridLayout")
        self.shot_view = QtGui.QTreeView(self.tab_shot)
        self.shot_view.setMinimumSize(QtCore.QSize(0, 0))
        self.shot_view.setObjectName("shot_view")
        self.gridLayout.addWidget(self.shot_view, 0, 0, 1, 1)
        self.shot_tab_widget.addTab(self.tab_shot, "")
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName("tab2")
        self.shot_tab_widget.addTab(self.tab2, "")
        self.shot_tab_lay.addWidget(self.shot_tab_widget)
        self.shot_tree_layout.addLayout(self.shot_tab_lay, 0, 0, 1, 1)
        self.shot_filter_edit = QtGui.QLineEdit(self.layoutWidget)
        self.shot_filter_edit.setInputMask("")
        self.shot_filter_edit.setObjectName("shot_filter_edit")
        self.shot_tree_layout.addWidget(self.shot_filter_edit, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.step_sel_all = QtGui.QPushButton(self.layoutWidget)
        self.step_sel_all.setFlat(True)
        self.step_sel_all.setObjectName("step_sel_all")
        self.horizontalLayout_3.addWidget(self.step_sel_all)
        self.step_sel_non = QtGui.QPushButton(self.layoutWidget)
        self.step_sel_non.setFlat(True)
        self.step_sel_non.setObjectName("step_sel_non")
        self.horizontalLayout_3.addWidget(self.step_sel_non)
        self.shot_tree_layout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.asset_layout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.asset_layout.setContentsMargins(0, 0, 0, 0)
        self.asset_layout.setObjectName("asset_layout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_type_layout = QtGui.QHBoxLayout()
        self.file_type_layout.setObjectName("file_type_layout")
        self.asset_icon = QtGui.QLabel(self.layoutWidget1)
        self.asset_icon.setText("")
        self.asset_icon.setObjectName("asset_icon")
        self.file_type_layout.addWidget(self.asset_icon)
        self.horizontalLayout.addLayout(self.file_type_layout)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.asset_search_line = QtGui.QLineEdit(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_search_line.sizePolicy().hasHeightForWidth())
        self.asset_search_line.setSizePolicy(sizePolicy)
        self.asset_search_line.setMinimumSize(QtCore.QSize(50, 0))
        self.asset_search_line.setObjectName("asset_search_line")
        self.horizontalLayout.addWidget(self.asset_search_line)
        self.list_mode_tb = QtGui.QToolButton(self.layoutWidget1)
        self.list_mode_tb.setObjectName("list_mode_tb")
        self.horizontalLayout.addWidget(self.list_mode_tb)
        self.icon_mode_tb = QtGui.QToolButton(self.layoutWidget1)
        self.icon_mode_tb.setObjectName("icon_mode_tb")
        self.horizontalLayout.addWidget(self.icon_mode_tb)
        self.asset_layout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.btn_layout = QtGui.QHBoxLayout()
        self.btn_layout.setObjectName("btn_layout")
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.btn_layout.addItem(spacerItem4)
        self.load_all_btn = QtGui.QPushButton(Form)
        self.load_all_btn.setObjectName("load_all_btn")
        self.btn_layout.addWidget(self.load_all_btn)
        self.load_sel_btn = QtGui.QPushButton(Form)
        self.load_sel_btn.setObjectName("load_sel_btn")
        self.btn_layout.addWidget(self.load_sel_btn)
        self.gridLayout_2.addLayout(self.btn_layout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.shot_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.step_filter_lab.setText(QtGui.QApplication.translate("Form", "Filter by Task step", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_tab_widget.setTabText(self.shot_tab_widget.indexOf(self.tab_shot), QtGui.QApplication.translate("Form", "Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_tab_widget.setTabText(self.shot_tab_widget.indexOf(self.tab2), QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.step_sel_all.setText(QtGui.QApplication.translate("Form", "select All", None, QtGui.QApplication.UnicodeUTF8))
        self.step_sel_non.setText(QtGui.QApplication.translate("Form", "select None", None, QtGui.QApplication.UnicodeUTF8))
        self.list_mode_tb.setText(QtGui.QApplication.translate("Form", "list", None, QtGui.QApplication.UnicodeUTF8))
        self.icon_mode_tb.setText(QtGui.QApplication.translate("Form", "icon", None, QtGui.QApplication.UnicodeUTF8))
        self.load_all_btn.setText(QtGui.QApplication.translate("Form", "Load All", None, QtGui.QApplication.UnicodeUTF8))
        self.load_sel_btn.setText(QtGui.QApplication.translate("Form", "Load Selection", None, QtGui.QApplication.UnicodeUTF8))

