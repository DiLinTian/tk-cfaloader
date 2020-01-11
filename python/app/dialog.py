import os
import sys
import threading
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
# import sgtk
# from sgtk.platform.qt import QtCore, QtGui
from ui.my_dialog import Ui_Dialog
from ui.step_filter_listwidget import StepFilterWidget
import asset_item_widget
from cmodel.ctree_view_model import CfaLoaderShotViewItemModel
from cmodel.shot_proxy_model import ShotProxyModel
from cmodel.shot_view_item import SequenceItemNode,ShotItemNode,ItemNode
from cmodel import step_relationship
import ui.resources_rc
import shotgun_data.cfa_shotgun_api as csa
import shotgun_data.connect_shotgun as consg
# import pymel.core as pm
# import maya.cmds as cmds

# standard toolkit logger
# logger = sgtk.platform.get_logger(__name__)
# def show_dialog(app_instance):
#     app_instance.engine.show_dialog("CFA Loader...", app_instance, AppDialog)

_Step_data = step_relationship.getData()
class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # self._app = sgtk.platform.current_bundle()
        # logger.info("Launching CFA Loader Application...")

        self._tab_widget = self.ui.shot_tab_widget
        self._tab_shot = self.ui.tab_shot
        self._shot_view = self.ui.shot_view
        self._asset_view = self.ui.asset_view
        self._asse_icon_label = self.ui.asset_icon

        pixmap = QtGui.QPixmap(":/res/asset_thumb_dark.png")
        self._asse_icon_label.setPixmap(pixmap.scaled(QtCore.QSize(35,35)))
        self.icon_mode_tb = self.ui.icon_mode_tb
        self.list_mode_tb = self.ui.list_mode_tb
        self._shot_filter_line = self.ui.shot_filter_edit
        self.step_filter_layout = self.ui.filter_layout

        self._step_sel_all = self.ui.step_sel_all
        self._step_sel_non = self.ui.step_sel_non
        self._search_asset_line = self.ui.asset_search_line
        # self._abc_box = self.ui.abc_box
        # self._maya_box = self.ui.maya_box
        # self._abc_box.setCheckState(QtCore.Qt.Checked)

        self._file_type_layout = self.ui.file_type_layout

        self.createFiletypeCheckUi()

        # self._step_sel_all.setHidden(True)
        # self._step_sel_non.setHidden(True)

        self.ui.splitter.setStretchFactor(0, 30)
        self.ui.splitter.setStretchFactor(1, 70)

        self.__abc = "abc"
        self.__maya = "maya"
        self.__xggeometry = "MAYA XGGeometry"
        self._task_templates = step_relationship.task_templates
        self._abc_items = list()
        self._maya_items = list()
        self._step_id_data = _Step_data.get('step_id')
        self._step_code_data = _Step_data.get('step_code')
        self._step_relationship = _Step_data.get("relationship")
        self._step_data = _Step_data.get('step')
        self._step_template = _Step_data.get("template")
        self.__layout = self._step_id_data.get("Layout")
        self.__animation = self._step_id_data.get("Animation")
        self.__preshot = self._step_id_data.get("Preshot")
        self.__light = self._step_id_data.get("Light")
        self.__cfx = self._step_id_data.get("CFX")

        style = """
            QLineEdit
            { 
                border-width: 1px; 
                background-image: url(:/res/search.png);
                background-repeat: no-repeat;
                background-position: center left;
                border-radius: 5px; 
                padding-left:20px;
                margin:4px;
                height:22px;
            }        
        """
        self._shot_filter_line.setStyleSheet(style)
        self._shot_filter_line.setPlaceholderText("Search Shot...")
        self._search_asset_line.setStyleSheet(style)
        self._search_asset_line.setPlaceholderText("Search File Name...")
        # self._shot_filter_line.setClearButtonEnabled(True)
        # self._search_asset_line.setClearButtonEnabled(True)


        self._step_listwidget = StepFilterWidget(self._step_data,self)
        self.step_filter_layout.addWidget(self._step_listwidget)

        self._asset_view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self._step_sel_all.clicked.connect(lambda:self._select_step_mode(QtCore.Qt.Checked))
        self._step_sel_non.clicked.connect(lambda:self._select_step_mode(QtCore.Qt.Unchecked))

        self.icon_mode_tb.clicked.connect(self._switch_icon_mode)
        self.list_mode_tb.clicked.connect(self._switch_list_mode)
        self.ui.load_sel_btn.clicked.connect(self.load_selection)
        self.ui.load_all_btn.clicked.connect(self.load_all)

        self._shot_view.setHeaderHidden(True)
        self._root_item_data = {"name":"shottree"}
        self._root_item = ItemNode(self._root_item_data)
        self.getSceneData()
        self.createShotItems()
        self.shot_model = CfaLoaderShotViewItemModel(self._root_item)
        self.shot_proxymodel = ShotProxyModel(self)
        self.shot_proxymodel.setSourceModel(self.shot_model)
        self.shot_proxymodel.setFilterKeyColumn(0)
        self.shot_proxymodel.setFilterRole(self.shot_model.filterRole)
        self.shot_proxymodel.setDynamicSortFilter(True)
        self._shot_view.setModel(self.shot_proxymodel)
        self._shot_view.clicked.connect(self._click_shot_item)
        self._shot_view.setFocus()
        self.setStepItemsFlags()
        self._step_listwidget.StepChanged.connect(self._receive_step_data)
        self._asset_view.itemSelectionChanged.connect(self._click_asset_item)
        self._asset_view.setViewMode(QtGui.QListView.IconMode)

        self._shot_filter_line.textChanged.connect(self._shot_filter_func)
        self._search_asset_line.textChanged.connect(self.setFileItemVisibilityByText)

        # self._abc_box.toggled.connect(self.setFileItemVisibilityByFilter)
        # self._maya_box.toggled.connect(self.setFileItemVisibilityByFilter)
        # self.expand_shot_item()
        # self._switch_list_mode()
    def createFiletypeCheckUi(self):
        _file_type = {
            "Alembic": "Alembic Cache",
            "Maya": "Maya Scene",
            "XGGeometry": "MAYA XGGeometry",
            "Shader": "Maya Shader Network"
        }
        _keys = _file_type.keys()
        _keys.sort()
        self._file_type_ui = []
        self._data_type = []
        for k in _keys:
            _checkui = QtGui.QCheckBox(k, self)
            _checkui.setObjectName(_file_type[k])
            self._file_type_ui.append(_checkui)
            self._file_type_layout.addWidget(_checkui)
            self._data_type.append(_file_type[k])

        self._file_type_ui[0].setChecked(True)

    def getSceneData(self):
        # self._scene_data = csa.getSceneSGData()
        # self._current_step_id = self._scene_data.get("step").get("id")
        self._current_step_id = 35
    def createShotItems(self):
        self._sequence_data = csa.getSequenceData()
        for seq in self._sequence_data:
            seq["item_name"] = seq["code"]
            seq["item_icon"] = ":/res/icon_Sequence_dark.png"
            seq_item = SequenceItemNode(seq,self._root_item)
            shot_entity_list = seq.get("shots")
            if not shot_entity_list:
                continue
            for shot in shot_entity_list:
                shot_data = csa.getShotData(shot["id"])
                shot_data["item_name"] = shot_data["code"]
                shot_data["item_icon"] = ":/res/icon_Shot_dark.png"
                shot_item = ShotItemNode(shot_data,seq_item)
    def _shot_filter_func(self,text):
        if not text:
            self._shot_view.collapseAll()
        self.shot_proxymodel.setFilterRegExp(text)
        self._shot_view.expandAll()
    def _click_shot_item(self):
        index = self._shot_view.currentIndex()
        source_index = self.shot_proxymodel.mapToSource(index)
        item_node = self.shot_model.getNode(source_index)
        item_type = item_node.typeInfo()
        item_data = item_node.data()
        shot_id = item_data.get("id")
        # current_step = "Layout"
        if item_type == "SHOTITEM":
            self.createShotRelatedItems(item_data["assets"],self._current_step_id,shot_id)
        self.setFileItemVisibilityByFilter()

    def createShotRelatedItems(self,asset_entity_list,current_step,shot_id):
        self._asset_view.clear()
        self.initAssetView()
        self._abc_items = list()
        self._maya_items = list()
        template = self.getStepTemplate(current_step)

        self.createRelatedItemForAssets(asset_entity_list,
                                        self._step_relationship.get(template))
        if current_step in [self.__preshot,self.__light,self.__cfx]:
            self.createRelatedItemForShots(shot_id,self._step_relationship.get(template))
                    
    def createRelatedItemForAssets(self,asset_entity_list,related_step):
        for asset in asset_entity_list:
            asset_id = asset.get("id")
            # asset_data = csa.getPublishFilesFun(related_step, asset_id)
            for step in related_step:

                step_id = self._step_id_data.get(step)
                asset_task_data = csa.getPublishFilesFun(asset_id, step_id)

                for data_type,file_data in asset_task_data.iteritems():
                    if data_type not in self._data_type:
                        continue

                    self.createShotRelatedItemFun(file_data,step_id,step,data_type)
                

    def createRelatedItemForShots(self,shot_id,related_step):
        for step in related_step:
            if step == "Shading":
                continue
            step_id = self._step_id_data.get(step)
            shot_task_data = csa.getPublishFilesFun(shot_id, step_id)
            for data_type, file_data in shot_task_data.iteritems():
                if data_type not in self._data_type:
                    continue
                self.createShotRelatedItemFun(file_data, step_id, step, data_type)

    def createShotRelatedItemFun(self,file_data,step_id,step,data_type):
        item_data = {}
        item_data["file_data"] = file_data
        item_data["item_step_id"] = step_id
        item_data["item_step"] = step
        item_data["item_data_type"] = data_type
        asset_item = asset_item_widget.AssetListItem(file_data,self._asset_view)
        asset_item.setSizeHint(QtCore.QSize(90, 70))
        asset_item.setItemsName()
        asset_item.setItemIcon()
        self._asset_view.addItem(asset_item)
        return asset_item
    def getStepTemplate(self,step_id):
        _step = None
        for k,v in self._step_id_data.iteritems():
            if v == step_id:
                _step = k
                break
        if _step is None:
            raise Exception("Step '%d' error!"%step_id)
        return self._step_template.get(_step)

    def get_data_type_by_ui(self):
        abc_state = self._abc_box.checkState()
        maya_state = self._maya_box.checkState()
        if maya_state == QtCore.Qt.Checked and abc_state == QtCore.Qt.Checked:
            emit_data = "all"
        elif maya_state == QtCore.Qt.Checked and abc_state == QtCore.Qt.Unchecked:
            emit_data =  "maya"
        elif abc_state == QtCore.Qt.Checked and maya_state == QtCore.Qt.Unchecked:
            emit_data = "abc"
        else:
            emit_data = None
        return emit_data

    def setFileItemVisibilityByDataType(self):
        _items = self.getAllAssetItems()
        if not _items:
            return
        data_type = self.get_data_type_by_ui()
        if data_type is None:
            for item in _items:
                item.setHidden(True)
            return
        # get items by data type
        data_type_items = self.getAssetItemsByDataType(data_type)
        for item in data_type_items:
            item.setHidden(False)
        # get other type items
        other_type_items = []
        types = [self.__abc, self.__maya]
        if data_type in types:
            types.remove(data_type)
            other_type = types[-1]
            other_type_items = self.getAssetItemsByDataType(other_type)
        # set other type items hidden True
        if other_type_items:
            for item in other_type_items:
                item.setHidden(True)

    def setFileItemVisibilityByStep(self,step_item_list,search_line_text = ""):
        '''
            filter : 1.data type 2.step short code 3. search edit
        :return:
        '''
        data_type = self.get_data_type_by_ui()
        if not data_type:
            return None
        data_type_items = self.getAssetItemsByDataType(data_type)
        step_filter_str = self.getStepFilterStr(step_item_list)
        print "step:",step_filter_str
        if not step_filter_str:
            for item in data_type_items:
                item.setHidden(True)
            return "no step selected"
        # filter step
        regexp_str = step_filter_str.strip().lower()
        regexp = QtCore.QRegExp("(%s)" % regexp_str)
        self.hidde_file_item_by_regexp(regexp,data_type_items)
        # filter text
        if search_line_text:
            current_items = self.get_display_file_items()
            if not current_items:
                return None
            regexp_str = search_line_text.strip().lower()
            regexp = QtCore.QRegExp("(%s)" % regexp_str)
            self.hidde_file_item_by_regexp(regexp, current_items)
    def setFileItemVisibilityByText(self,text):
        if not text:
            self.setFileItemVisibilityByDataType()
            self.setFileItemVisibilityByStep(self._step_listwidget.getItemsData())
            return "restore"
        self.setFileItemVisibilityByStep(self._step_listwidget.getItemsData(),text)


    def setFileItemVisibilityByFilter(self):
        self.setFileItemVisibilityByDataType()
        self.setFileItemVisibilityByStep(self._step_listwidget.getItemsData(),
                                         self._search_asset_line.text())

    def get_display_file_items(self):
        _display_items = []
        current_items = self.getAssetItemsByDataType(self.get_data_type_by_ui())
        for item in current_items:
            if not item.isHidden():
                _display_items.append(item)
        return _display_items
    def hidde_file_item_by_regexp(self,regexp,source_items):
        # item name : asset_SHD.v001.abc table_ANM.abc
        for item in source_items:
            item_name = item.itemName()
            pos = regexp.indexIn(item_name.lower())
            if pos == -1:
                item.setHidden(True)
            else:
                item.setHidden(False)
                

    def getAssetItemsByDataType(self,data_type):
        # data_type = self.get_data_type_by_ui()
        if data_type == "all":
            return self.getAllAssetItems()
        if data_type == self.__abc:
            return self._abc_items
        elif data_type == self.__maya:
            return self._maya_items
    def getAllAssetItems(self):
        return self._abc_items + self._maya_items

    def _receive_step_data(self, step_item_list):
        '''

        :param step_item_list: receive stpe listwidget data
                find related file item by step list
        '''

        search_text = self._search_asset_line.text()
        self.setFileItemVisibilityByStep(step_item_list,search_text)

    def getStepFilterStr(self, step_item_list):
        '''

        :param step_item_list:
        :return: short code filter str e.g. mdl|shd
        '''
        # step_item_list = self._step_listwidget.getItemsData()
        if not step_item_list:
            return ""
        # step_short_code = _Step_data.get("step_code")
        short_code_list = list()
        for step in step_item_list:
            short_code = self._step_code_data.get(step)
            short_code_list.append(short_code)
        short_code_str = "|".join(short_code_list)
        return short_code_str

    def getRelatedAssetsData(self,related_step,asset_id):
        # related_step_data = _Step_data.get(task_template)
        _data = []
        for step in related_step:
            step_id = self._step_id_data.get(step)
            asset_task_data = csa.getPublishFilesFun(asset_id, step_id)
            if asset_task_data:
                asset_task_data["item_step_id"] = step_id
                asset_task_data["item_step"] = step
                _data.append(asset_task_data)

        return _data
    def getRelatedShotsData(self,related_step,shot_id):
        # _task = "preshot_task"
        # related_step_data = _Step_data.get(task_template)
        shot_data = []
        for step in related_step:
            if step == "Shading":
                continue
            step_id = self._step_id_data.get(step)
            shot_task_data = csa.getPublishFilesFun(shot_id, step_id)
            if shot_task_data:
                # print "shot_taks_data:",shot_task_data
                shot_task_data["item_step_id"] = step_id
                shot_task_data["item_step"] = step
                shot_data.append(shot_task_data)
        return shot_data


    def _click_asset_item(self):
        item = self._asset_view.currentItem()
        item_data = item.itemData()
        path =  item_data.get("path")
        win_path = path.get("local_path_windows")
        name = item_data.get("code")
        print name,win_path

    def load_selection(self):
        selected_items = self._asset_view.selectedItems()
        for item in selected_items:
            item_data = item.itemData()
            createReference(item_data)
    def load_all(self):
        display_items = self.get_display_file_items()
        if not display_items:
            return None
        for item in display_items:
            createReference(item.itemData())
    def _switch_icon_mode(self):
        self.initAssetView()
        self._asset_view.setViewMode(QtGui.QListView.IconMode)
        self._asset_view.setIconSize(QtCore.QSize(100,100))
        self.setItemSize(self._asset_view)

    def _switch_list_mode(self):
        self._asset_view.setViewMode(QtGui.QListView.ListMode)
        self.initAssetView()
        self.setItemSize(self._asset_view, 80, 60)

    def setItemSize(self,view,width = 130,height = 130):
        for i in range(view.count()):
            view.item(i).setSizeHint(QtCore.QSize(width,height))

    def initAssetView(self):
        self._asset_view.setIconSize(QtCore.QSize(70, 50))
        self._asset_view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self._asset_view.setResizeMode(QtGui.QListWidget.Adjust)
        self._asset_view.setMovement(QtGui.QListWidget.Static)
        self._asset_view.setSpacing(2)
    def expand_shot_item(self):
        shot_id = self._scene_data.get('entity').get("id")
        # shot_id = 2112
        shot_data = csa.getShotData(shot_id)
        seq_code = shot_data.get("sg_sequence").get("name")
        # print "scene_info:",shot_data.get("code"),seq_code
        for seq_item in self._root_item.childItems():
            if seq_item.name() == seq_code:
                row = seq_item.row()
                seq_index = self.shot_proxymodel.index(row,0)
                for shot_item in seq_item.childItems():
                    if shot_item.name() == shot_data.get("code"):
                        row = shot_item.row()
                        shot_index = self.shot_proxymodel.index(row,0,seq_index)
                        break
        try:
            self._shot_view.expand(seq_index)
            self._shot_view.setCurrentIndex(shot_index)
        except:
            pass
        self._click_shot_item()
    def setStepItemsFlags(self):

        step_items = self.getStepItems()
        template = self.getStepTemplate(self._current_step_id)
        def_step = "All"
        if self._current_step_id in [self.__layout, self.__animation]:
            def_step = "Model"
        self.setupStepItems(step_items,self._step_relationship.get(template),def_step)


    def setupStepItems(self,step_items,step_data,def_step):
        '''

        :param step_items:
        :param step_data:
        :param def_step: one in  [step_name,"All",None]
        :return:
        '''
        for item in step_items:
            item_name = item.text()
            if item_name not in step_data:
                item.setCheckState(QtCore.Qt.Unchecked)
                self._step_listwidget.setItemTextColor(item,self._step_listwidget._unrelated_uncheck_color)
            else:
                if def_step == item_name:
                    item.setCheckState(QtCore.Qt.Checked)
                elif def_step == "All":
                    item.setCheckState(QtCore.Qt.Checked)

                self._step_listwidget.setItemTextColor(item,self._step_listwidget._is_related_color)

        self._step_listwidget.setRelatedStep(step_data)


    def getStepItems(self):
        step_items = []
        for i in range(self._step_listwidget.count()):
            step_items.append(self._step_listwidget.item(i))

        return step_items
    def setStepItemsState(self,state):
        step_items = self.getStepItems()
        for item in step_items:
            self._step_listwidget.setItemsState(self._step_listwidget.row(item),state)

    def _select_step_mode(self,checked):
        for i in range(self._step_listwidget.count()):
            item = self._step_listwidget.item(i)
            item.setCheckState(checked)
            self._step_listwidget.checkItemState(item)

        
class CreateFileTypeCheckUI(QtGui.QCheckBox):

    def __init__(self,display_name,object_name,parent = None):
        super(CreateFileTypeCheckUI, self).__init__(parent)
        self.display_name = display_name
        self.object_name = object_name
        self.setText(self.display_name)
        self.setObjectName(self.object_name)
    # def _click_(self):






def createReference(sg_data):
    path = sg_data.get("path")
    win_path = path.get("local_path_windows")
    # win_path = win_path.replace("\\","/")

    if not os.path.exists(win_path):
        raise Exception("File not found on disk - '%s'" % win_path)
    name = sg_data.get("code")
    namespace = name.split('.')[0]
    namespace = namespace.replace(" ", "_")

    pm.system.createReference(win_path,loadReferenceDepth="all",
                              mergeNamespacesOnClash=False,
                              namespace=namespace)

    reference_node = cmds.referenceQuery(win_path, referenceNode=True)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = AppDialog()
    win.show()
    sys.exit(app.exec_())
