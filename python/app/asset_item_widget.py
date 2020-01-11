#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/24 15:48
@ description:
    

'''
# from sgtk.platform.qt import QtCore, QtGui
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import sys,os
import requests
class AssetItemWidget(QtGui.QWidget):
    SelSignal = QtCore.Signal()
    AllSignal = QtCore.Signal()

    def __init__(self,data,parent = None):

        super(AssetItemWidget, self).__init__(parent)
        self.setObjectName("asset_item_widget")
        self._item_data = data
        self.setWindowFlags(QtCore.Qt.Window)

        self._layout = QtGui.QHBoxLayout()
        # self._image_label = QtGui.QLabel(self)

        self._label_layout = QtGui.QVBoxLayout()
        self._name_label = QtGui.QLabel(self)
        self._description_label = QtGui.QLabel("",self)
        # self._action = QtGui.QPushButton("Actions>",self)
        # self._action.setFlat(True)

        self._label_layout.addWidget(self._description_label)
        self._label_layout.addWidget(self._name_label)


        # self._layout.addWidget(self._name_label)
        self._layout.addLayout(self._label_layout)
        # self._layout.addWidget(self._action)
        # spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # self._layout.addItem(spacerItem)
        self.setData()
        self.setLayout(self._layout)

    def setName(self,name):
        self._name_label.setText(name)

    def setDescription(self,description):
        self._description_label.setText(description)

    def setData(self):
        published_file = self._item_data.get("file_data")
        self.setName((published_file["published_file_type"]["name"]))
        # self.setImage(self._item_data["image"])
        # self.setDescription(self._item_data["description"])
    def data(self):
        return self._item_data
    def name(self):
        return self._name_label.text()
    def image(self):
        return self._image_label.text()
    def description(self):
        return self._description_label.text()

class AssetListItem(QtGui.QListWidgetItem):
    def __init__(self,item_data,parent = None):
        super(AssetListItem, self).__init__(parent)
        self._parent = parent
        self._item_data = item_data

    def itemData(self):
        return self._item_data
    def getPixmap(self,url):
        pixmap = QtGui.QPixmap()
        r = requests.get(url)
        pixmap.loadFromData(r.content)
        return pixmap#.scaled(QtCore.QSize(60,40))
    def itemName(self):
        return self.text()
    def setItemsName(self):
        file_name = self._item_data.get("code")
        publish_type = self._item_data.get("published_file_type").get("name")
        _name = file_name + "\n" + publish_type
        self.setText(_name)
    def setItemIcon(self):
        self.setIcon(self.getPixmap(self._item_data.get("image")))
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)


    aa =[{'version_number': 4, 'task': {'type': 'Task', 'id': 16911, 'name': 'model'}, 'image': 'http://sg.anime.com/thumbnail/api_image/24873?AccessKeyId=uTbPnnWUNhn2nSG7Agrp&Expires=1569402037&Signature=%2FvvvepGJ8EFvzhupxSjqJMg5V845SEY7BrSb%2BDCwj0s%3D', 'published_file_type': {'type': 'PublishedFileType', 'id': 2, 'name': 'Maya Scene'}, 'code': 'table_MDL.v004.ma', 'path': {'local_path_windows': '\\\\3par\\ibrix01\\shotgun\\shotgun_work\\configtest\\assets\\Prop\\table\\MDL\\publish\\maya\\table_MDL.v004.ma', 'name': 'table_MDL.v004.ma', 'local_path_linux': '/shotgun/shotgun_work/configtest/assets/Prop/table/MDL/publish/maya/table_MDL.v004.ma', 'url': 'file://\\\\3par\\ibrix01\\shotgun\\shotgun_work\\configtest\\assets\\Prop\\table\\MDL\\publish\\maya\\table_MDL.v004.ma', 'local_storage': {'type': 'LocalStorage', 'id': 2, 'name': 'CFA  LocalStorage'}, 'local_path': '\\\\3par\\ibrix01\\shotgun\\shotgun_work\\configtest\\assets\\Prop\\table\\MDL\\publish\\maya\\table_MDL.v004.ma', 'content_type': None, 'local_path_mac': None, 'type': 'Attachment', 'id': 21515, 'link_type': 'local'}, 'type': 'PublishedFile', 'id': 4678}, {'version_number': 1, 'task': {'type': 'Task', 'id': 16897, 'name': 'mod'}, 'image': 'http://sg.anime.com/thumbnail/api_image/24694?AccessKeyId=uTbPnnWUNhn2nSG7Agrp&Expires=1569402037&Signature=3SGVdjxMhhirYQOckx4%2B1XRH7OJ40PpY%2BJIjfLSsELg%3D', 'published_file_type': {'type': 'PublishedFileType', 'id': 2, 'name': 'Maya Scene'}, 'code': 'testball_MDL.v001.ma', 'path': {'local_path_windows': '\\\\3par\\ibrix01\\shotgun\\shotgun_work\\configtest\\assets\\Prop\\testball\\MDL\\publish\\maya\\testball_MDL.v001.ma', 'name': 'testball_MDL.v001.ma', 'local_path_linux': '/shotgun/shotgun_work/configtest/assets/Prop/testball/MDL/publish/maya/testball_MDL.v001.ma', 'url': 'file://\\\\3par\\ibrix01\\shotgun\\shotgun_work\\configtest\\assets\\Prop\\testball\\MDL\\publish\\maya\\testball_MDL.v001.ma', 'local_storage': {'type': 'LocalStorage', 'id': 2, 'name': 'CFA  LocalStorage'}, 'local_path': '\\\\3par\\ibrix01\\shotgun\\shotgun_work\\configtest\\assets\\Prop\\testball\\MDL\\publish\\maya\\testball_MDL.v001.ma', 'content_type': None, 'local_path_mac': None, 'type': 'Attachment', 'id': 21315, 'link_type': 'local'}, 'type': 'PublishedFile', 'id': 4608}]
    win = AssetItemWidget(aa[0])
    win.show()
    # print win._name_label.text()
    sys.exit(app.exec_())