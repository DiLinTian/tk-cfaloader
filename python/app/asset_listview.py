#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/25 10:50
@ description:
    

'''
import sgtk
from sgtk.platform.qt import QtCore, QtGui
# from PySide import QtCore, QtGui
import shotgun_data.cfa_shotgun_api as csa
class AssetsListview(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(AssetsListview, self).__init__(parent)
    
    def getAllItems(self):
        _asset_items = []
        for i in xrange(self.count()):
            item = self.item(i)
            if item is None:
                continue
            _asset_items.append(item)
        return _asset_items
    def setHiddenByDataType(self,display_type_list):
        asset_items = self.getAllItems()
        if not asset_items:
            return
        if not display_type_list:
            for item in asset_items:
                item.setHidden(True)
            return

        for item in asset_items:
            itemdata = item.itemData()
            if itemdata.get("published_file_type").get('name') in display_type_list:
                item.setHidden(False)
            else:
                item.setHidden(True)
        # self.hide_ma_file_items(asset_items)
    def setHiddenByStep(self,step_str,display_type_list,search_line_text=""):
        if not display_type_list:
            return None
        data_type_items = self.getAssetItemsByDataType(display_type_list)
        if not step_str:
            for item in data_type_items:
                item.setHidden(True)
            return "no step selected"
        # filter step
        regexp_str = step_str.strip().lower()
        regexp = QtCore.QRegExp("(_%s)" % regexp_str)
        self.hidde_file_item_by_regexp(regexp, data_type_items)
        # filter text
        if search_line_text:
            current_items = self.getDisplayAssetItems()
            if not current_items:
                return None
            regexp_str = search_line_text.strip().lower()
            regexp = QtCore.QRegExp("(%s)" % regexp_str)
            self.hidde_file_item_by_regexp(regexp, current_items)

    def getAssetItemsByDataType(self, display_type_list):
        # data_type = self.get_data_type_by_ui()
        asset_items = self.getAllItems()
        _checked = QtCore.Qt.CheckState.Checked
        _unchecked = QtCore.Qt.CheckState.Unchecked
        _checked_type = []
        _checked_items = []
        for item in asset_items:
            itemdata = item.itemData()
            if itemdata.get("published_file_type").get('name') in display_type_list:
                _checked_items.append(item)
        return _checked_items
    def hidde_file_item_by_regexp(self, regexp, source_items):
        # item name : asset_SHD.v001.abc table_ANM.abc
        # regexp = QtCore.QRegExp("(_%s)" % regexp_str)
        # print regexp.pattern()
        for item in source_items:
            item_name = item.itemName()
            pos = regexp.indexIn(item_name.lower())
            if pos == -1:
                item.setHidden(True)
            else:
                item.setHidden(False)
        # self.hide_ma_file_items(source_items)
    def hide_ma_file_items(self,items):
        # rig,preshot,keylight,animation
        sgdata = csa.getSceneSGData()
        need_ma_step = [135, 134, 144]
        if sgdata.get('project').get('id') in [105]:
            need_ma_step.append(106)
        for item in items:
            item_data = item.itemData()
            item_step = csa.getStepByTask(item_data.get('task').get('id'))
            item_step_id = item_step.get('id')
            if item_step_id not in need_ma_step:
                if item_data.get("published_file_type").get('name') == "Maya Scene":
                    item.setHidden(True)

    def getDisplayAssetItems(self):
        _asset_items = self.getAllItems()
        _display_asset_items = []
        for item in _asset_items:
            if not item.isHidden():
                _display_asset_items.append(item)
        return _display_asset_items
    def getDisplayAssetItemsTypeData(self,_asset_items):
        '''

        :return: data:{"Alembic Cache":[item1,item2,...]}
        '''
        #_asset_items = self.getDisplayAssetItems()
        item_type_data = {}
        for item in _asset_items:
            itemdata = item.itemData()
            item_type = itemdata.get("published_file_type").get('name')
            if item_type == "Alembic Cache":
                item_type_data.setdefault("Alembic Cache",[]).append(item)
            elif item_type == "Maya Scene":
                item_type_data.setdefault("Maya Scene",[]).append(item)
            elif item_type == "MAYA XGGeometry":
                item_type_data.setdefault("MAYA XGGeometry",[]).append(item)
            elif item_type == "Maya Shader Network":
                item_type_data.setdefault("Maya Shader Network",[]).append(item)
            elif item_type == "MAYA XGShader":
                item_type_data.setdefault("MAYA XGShader",[]).append(item)
            elif item_type == "Maya XGen":
                item_type_data.setdefault("Maya XGen",[]).append(item)
            elif item_type == "MAYA LightRig":
                item_type_data.setdefault("MAYA LightRig",[]).append(item)
            elif item_type == "Maya SIMCRV":
                item_type_data.setdefault("Maya SIMCRV",[]).append(item)
            elif item_type == "MAYA Camera":
                item_type_data.setdefault("MAYA Camera", []).append(item)
            # elif item_type == "MayaAssembly":
            #     item_type_data.setdefault("MayaAssembly",[]).append(item)
            # elif item_type == "MayaAssemblyReference":
            #     item_type_data.setdefault("MayaAssemblyReference",[]).append(item)

        return item_type_data