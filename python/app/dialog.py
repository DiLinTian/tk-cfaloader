import os
import sys
# import PySide.QtGui as QtGui
# import PySide.QtCore as QtCore
from tank.platform.qt import QtCore, QtGui
from ui.my_dialog import Ui_Dialog
from ui.step_filter_listwidget import StepFilterWidget
import asset_item_widget
import asset_listview
import file_type_checkui as ftc
import _hooks
# reload(_hooks)
from cmodel.ctree_view_model import CfaLoaderShotViewItemModel
from cmodel.shot_proxy_model import ShotProxyModel
from cmodel.shot_view_item import SequenceItemNode, ShotItemNode, ItemNode
from cmodel import step_relationship,file_type_parse
import ui.resources_rc
import shotgun_data.cfa_shotgun_api as csa
import shotgun_data.connect_shotgun as shotgun
import maya.cmds as cmds

# standard toolkit logger
import sgtk
logger = sgtk.platform.get_logger(__name__)
def show_dialog(app_instance):
    app_instance.engine.show_dialog("CFA Loader", app_instance, AppDialog)

_Step_data = step_relationship.getData()
class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # init data
        self._initData()
        self._app = sgtk.platform.current_bundle()
        logger.info("Launching CFA Loader Application...")

        self._tab_widget = self.ui.shot_tab_widget
        self._tab_shot = self.ui.tab_shot
        self._shot_view = self.ui.shot_view
        self._asset_view = asset_listview.AssetsListview(self)
        self._asset_layout = self.ui.asset_layout
        self._asset_layout.addWidget(self._asset_view)
        self._asse_icon_label = self.ui.asset_icon

        pixmap = QtGui.QPixmap(":/res/asset_thumb_dark.png")
        self._asse_icon_label.setPixmap(pixmap.scaled(QtCore.QSize(35, 35)))
        self.icon_mode_tb = self.ui.icon_mode_tb
        self.list_mode_tb = self.ui.list_mode_tb
        self._shot_filter_line = self.ui.shot_filter_edit
        self.step_filter_layout = self.ui.filter_layout

        self._step_sel_all = self.ui.step_sel_all
        self._step_sel_non = self.ui.step_sel_non
        self._search_asset_line = self.ui.asset_search_line

        self._file_type_layout = self.ui.file_type_layout

        self._file_type_ui = ftc.CreateFileTypeCheckUI(self._file_type,self)
        self._file_type_layout.addWidget(self._file_type_ui)
        self._data_type = self._file_type_ui._type_list()
        self._file_type_ui.FileTypeState.connect(self.setFileItemVisibility)

        self._checked_state = QtCore.Qt.CheckState.Checked
        self.un_checked_state = QtCore.Qt.CheckState.Unchecked


        self.ui.splitter.setStretchFactor(0, 30)
        self.ui.splitter.setStretchFactor(1, 70)

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

        self._step_listwidget = StepFilterWidget(self._step_data, self)
        self.step_filter_layout.addWidget(self._step_listwidget)

        self._asset_view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self._step_sel_all.clicked.connect(lambda: self._select_step_mode(QtCore.Qt.Checked))
        self._step_sel_non.clicked.connect(lambda: self._select_step_mode(QtCore.Qt.Unchecked))

        self.icon_mode_tb.clicked.connect(self._switch_icon_mode)
        self.list_mode_tb.clicked.connect(self._switch_list_mode)
        self.ui.load_sel_btn.clicked.connect(self.load_selection)
        self.ui.load_all_btn.clicked.connect(self.load_all)

        self._shot_view.setHeaderHidden(True)
        self._root_item_data = {"name": "shottree"}
        self._root_item = ItemNode(self._root_item_data)
        
        # self.createShotItems()
        self.createCurrentShotItem()
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

        self.expand_shot_item()
        self.setFileTypeVisibility()
        self._switch_list_mode()

    def _initData(self):
        self._scene_data = csa.getSceneSGData()
        self._current_step_id = self._scene_data.get("step").get("id")
        self.sg_project = self._scene_data.get("project")
        # self.sg_project = {'type': 'Project', 'id': 113}
        # self._current_step_id = 134
        self._task_templates = step_relationship.task_templates
        self._step_id_data = _Step_data.get('step_id')#{Animation:106}
        self._step_code_data = _Step_data.get('step_code')#[ANM,CFX]
        self._step_relationship = _Step_data.get("relationship")

        self._step_data = _Step_data.get('step')#[Animation,CFX]
        self.__layout = self._step_id_data.get("Layout")
        self.__animation = self._step_id_data.get("Animation")
        self.__preshot = self._step_id_data.get("Preshot")
        self.__light = self._step_id_data.get("Light")
        self.__cfx = self._step_id_data.get("CFX")
        self.__keylight = self._step_id_data.get('KeyLight')
        self._step_template_data = _Step_data.get("template")
        self._current_template = self.getStepTemplate(self._current_step_id)
        self._related_step = self._step_relationship.get(self._current_template)
        self._file_type = file_type_parse.get_file_map()

        self._shot_ralated_steps = [self.__preshot, self.__light, self.__cfx,self.__keylight]


    def getCurrentShotItemData(self):
        index = self._shot_view.currentIndex()
        source_index = self.shot_proxymodel.mapToSource(index)
        item_node = self.shot_model.getNode(source_index)
        item_type = item_node.typeInfo()
        item_data = item_node.data()
        return item_type,item_data
    def setFileTypeVisibility(self):
        item_type,item_data = self.getCurrentShotItemData()
        if not item_data:
            return
        shot_id = item_data.get("id")
        _file_type = []
        # asset data
        for asset in item_data["assets"]:
            for step in self._related_step:
                pub = csa.getPublishFilesFun(asset.get("id"),self._step_id_data[step],"Asset")
                if not pub:
                    continue
                for k,v in pub.iteritems():
                    if k not in _file_type:
                        _file_type.append(k)
        # shot data
        if self._current_step_id in self._shot_ralated_steps:
            for step in self._related_step:
                _spub = csa.getPublishFilesFun(shot_id,self._step_id_data[step],"Shot")
                if not _spub:
                    continue
                for kk,vv in _spub.iteritems():
                    if kk not in _file_type:
                        _file_type.append(kk)

        file_ui_list = self._file_type_ui.getUilist()
        for ui in file_ui_list:
            if ui.objectName() not in _file_type:
                ui.setHidden(True)

        self._file_type_ui.setCheckUiState()
        self.setFileItemVisibility()
    # def createShotItems(self):
    #     self._sequence_data = csa.getSequenceData()
    #     if not self._sequence_data:
    #         raise Exception("No sequence data!")
    #     for seq in self._sequence_data:
    #         seq["item_name"] = seq["code"]
    #         seq["item_icon"] = ":/res/icon_Sequence_dark.png"
    #         seq_item = SequenceItemNode(seq, self._root_item)
    #         shot_entity_list = seq.get("shots")
    #         if not shot_entity_list:
    #             continue
    #         for shot in shot_entity_list:
    #             shot_data = csa.getShotData(shot["id"])
    #             shot_data["item_name"] = shot_data["code"]
    #             shot_data["item_icon"] = ":/res/icon_Shot_dark.png"
    #             shot_item = ShotItemNode(shot_data, seq_item)

    def createCurrentShotItem(self):
        # shot_id = 8128
        shot_id = self._scene_data.get('entity').get('id')
        self._current_shot_data = csa.getShotData(shot_id)
        _sequence = self._current_shot_data.get("sg_sequence").get('id')
        self._sequence_data = csa.getSequenceData2(_sequence)
        if not self._sequence_data:
            raise Exception("No sequence data!")
        self._sequence_data['item_name'] = self._sequence_data['code']
        self._sequence_data['item_icon'] = ":/res/icon_Sequence_dark.png"
        self._sequence_item = SequenceItemNode(self._sequence_data, self._root_item)

        self._current_shot_data["item_name"] = self._current_shot_data["code"]
        self._current_shot_data["item_icon"] = ":/res/icon_Shot_dark.png"
        self._shot_item = ShotItemNode(self._current_shot_data, self._sequence_item)

    def _shot_filter_func(self, text):
        if not text:
            self._shot_view.collapseAll()
        self.shot_proxymodel.setFilterRegExp(text)
        self._shot_view.expandAll()

    def _click_shot_item(self):
        item_type,item_data = self.getCurrentShotItemData()
        shot_id = item_data.get("id")
        # current_step = "Layout"
        if item_type == "SHOTITEM":
            self.createShotRelatedItems(item_data["assets"],
                                        self._current_step_id,
                                        shot_id,
                                        self._related_step)
        self.setFileItemVisibility()

    def createShotRelatedItems(self, asset_entity_list, current_step, shot_id,related_step):
        self._asset_view.clear()
        self.initAssetView()
        for asset in asset_entity_list:
            asset_id = asset.get("id")
            self.createRelatedItem(asset_id,related_step)
        if current_step in self._shot_ralated_steps:
            self.createRelatedItem(shot_id, related_step)

    def getEntityType(self,entity_id):
        sg = shotgun._shotgun()
        mode = "Asset"
        _find = sg.find_one("Shot", [['id', 'is', entity_id], ["project", 'is', self.sg_project]])
        if _find:
            mode = "Shot"
        return mode
    def createRelatedItem(self,entity_id, related_step):
        mode = self.getEntityType(entity_id)
        for step in related_step:
            if mode == "Shot":
                if step == "Shading":
                    continue
            step_id = self._step_id_data.get(step)
            _task_data = csa.getPublishFilesFun(entity_id, step_id,mode)
            # print entity_id,step_id,_task_data
            for data_type, file_data in _task_data.iteritems():
                if data_type not in self._data_type:
                    continue
                for fd in file_data:
                    self.createShotRelatedItemFun(fd)

    def createShotRelatedItemFun(self, file_data):
        asset_item = asset_item_widget.AssetListItem(file_data, self._asset_view)
        asset_item.setSizeHint(QtCore.QSize(90, 70))
        asset_item.setItemsName()
        asset_item.setItemIcon()
        self._asset_view.addItem(asset_item)
        return asset_item

    def getStepTemplate(self, step_id):
        _step = None
        for k, v in self._step_id_data.iteritems():
            if v == step_id:
                _step = k
                break
        if _step is None:
            raise Exception("Step '%d' error!" % step_id)
        return self._step_template_data.get(_step)

    def setFileItemVisibilityByText(self):
        step_item_list = self._step_listwidget.getItemsData()
        self._receive_step_data(step_item_list)

    def setFileItemVisibility(self):
        file_type_list = self._file_type_ui.getCheckedType()
        # print "checked file:",file_type_list
        self._receive_type_state(file_type_list)
        current_step_list = self._step_listwidget.getItemsData()
        self._receive_step_data(current_step_list)

    def _receive_step_data(self,step_item_list):
        '''

        :param step_item_list: receive stpe listwidget data
                find related file item by step list
        '''

        search_text = self._search_asset_line.text()
        # print "search:",search_text
        step_str = self.getStepFilterStr(step_item_list)
        print "receive step:", step_str
        self._asset_view.setHiddenByStep(step_str,
                                         self._file_type_list,
                                         search_text)
    def _receive_type_state(self, file_type_list):

        self._file_type_list = file_type_list
        self._asset_view.setHiddenByDataType(self._file_type_list)


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
    def update_scene_time(self):
        engine = sgtk.platform.current_engine()
        context = engine.context
        project = context.project
        entity = context.entity

        if entity.get('type') == "Shot":
            from func import _shotgun_server
            import __Maya.common.maya_func as maya_func
            sg = _shotgun_server._shotgun()
            project_find = sg.find_one("Project",[['id','is',project.get('id')]],['sg_time'])
            rate = int(project_find.get('sg_time'))
            index = 0
            if rate == 24:
                index = 1
            if rate == 25:
                index =0
            if rate == 30:
                index = 2
            maya_func.setFPS(index)
            shot_entity = sg.find_one(entity.get("type"), [['id', 'is', entity.get('id')], ['project', 'is', project]],
                                      ['sg_cut_in', 'sg_cut_out'])

            start = shot_entity.get('sg_cut_in')
            end = shot_entity.get('sg_cut_out')
            if start is not None:
                cmds.playbackOptions(e=True, min=int(start))
            if end is not None:
                cmds.playbackOptions(e=True, max=int(end))
            print "Set scene time."
    def _click_asset_item(self):
        item = self._asset_view.currentItem()
        item_data = item.itemData()
        path = item_data.get("path")
        win_path = path.get("local_path_windows")
        name = item_data.get("code")
        print name,win_path

    def load_selection(self):
        selected_items = self._asset_view.selectedItems()
        self.loadObjectsFunction(selected_items)
        self.update_scene_time()
    def load_all(self):
        display_items = self._asset_view.getDisplayAssetItems()
        if not display_items:
            return None
        self.loadObjectsFunction(display_items)
        self.update_scene_time()
    def loadPublishFiles(self,select_items,typ):
        if not select_items:
            return False
        for item in select_items:
            item_data = item.itemData()
            _file_path = item_data.get('path').get('local_path_windows')
            if typ == "Maya XGen":
                _isImport = _hooks._hookup_xgen(_file_path)
                if not _isImport:
                    return False
            elif typ == "MAYA XGGeometry":
                _hooks.importMayaFile(_file_path)
            elif typ == "Maya SIMCRV":
                _hooks._hookup_simcrv(_file_path)
            else:
                _hooks.createReference(_file_path)
                # if "_ANM." in _file_path or "_LAY." in _file_path:
                #     _hooks.importMayaFile(_file_path)
                # else:
                #     _hooks.createReference(_file_path)
        return True
    def loadObjectsFunction(self,select_items):
        item_type_data = self._asset_view.getDisplayAssetItemsTypeData(select_items)
        alembic_items = item_type_data.get("Alembic Cache",[])
        maya_items = item_type_data.get("Maya Scene",[])
        xggeo_items = item_type_data.get("MAYA XGGeometry",[])
        shader_items = item_type_data.get("Maya Shader Network",[])
        xgshader_items = item_type_data.get("MAYA XGShader",[])
        xgen_items = item_type_data.get("Maya XGen",[])
        lightrig_items = item_type_data.get("MAYA LightRig",[])
        simcrv_items = item_type_data.get("Maya SIMCRV",[])
        camera_items = item_type_data.get('MAYA Camera',[])
        xgshader_is_loaded = 0
        shader_is_loaded = 0
        xgen_is_import = False
        # load order: alembic,maya,xgeo,xgen,simcrv,xgshader,lightrig,shader
        if alembic_items:
            print "load abc..."
            self.loadPublishFiles(alembic_items,"Alembic Cache")
        if maya_items:
            print "load maya..."
            self.loadPublishFiles(maya_items,"Maya Scene")
        if xggeo_items:
            print "load xggeo..."
            self.loadPublishFiles(xggeo_items,"MAYA XGGeometry")
        if xgen_items:
            print "load xgen..."
            xgen_is_import = self.loadPublishFiles(xgen_items,"Maya XGen")
        if simcrv_items:
            if xgen_is_import:
                print "load simcrv..."
                self.loadPublishFiles(simcrv_items,"Maya SIMCRV")
        if xgshader_items:
            if xgen_is_import:
                print "load xgshader..."
                self.loadPublishFiles(xgshader_items,"MAYA XGShader")
                xgshader_is_loaded = 1
        if lightrig_items:
            print "load lightrig..."
            self.loadPublishFiles(lightrig_items,"MAYA LightRig")
        if shader_items:
            print "load shader..."
            self.loadPublishFiles(shader_items,"Maya Shader Network")
            shader_is_loaded=1
        if camera_items:
            print "load camera..."
            self.loadPublishFiles(camera_items,"MAYA Camera")
        # connect shaders
        SHADER_HOOKUP = "SHADER_HOOKUP_"
        if xgshader_is_loaded:
            print "connect xgshader..."
            _hooks._hookup_xgshaders(xgshader_items)
        if shader_is_loaded:
            print "connect shader..."
            _hooks._hookup_shaders(SHADER_HOOKUP,'mesh')

    def _switch_icon_mode(self):
        self.initAssetView()
        self._asset_view.setViewMode(QtGui.QListView.IconMode)
        self._asset_view.setIconSize(QtCore.QSize(100, 100))
        self.setItemSize(self._asset_view)

    def _switch_list_mode(self):
        self._asset_view.setViewMode(QtGui.QListView.ListMode)
        self.initAssetView()
        self.setItemSize(self._asset_view, 80, 60)

    def setItemSize(self, view, width=130, height=130):
        for i in range(view.count()):
            view.item(i).setSizeHint(QtCore.QSize(width, height))

    def initAssetView(self):
        self._asset_view.setIconSize(QtCore.QSize(70, 50))
        self._asset_view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self._asset_view.setResizeMode(QtGui.QListWidget.Adjust)
        self._asset_view.setMovement(QtGui.QListWidget.Static)
        self._asset_view.setSpacing(2)

    # def expand_shot_item(self):
    #     shot_id = self._scene_data.get('entity').get("id")
    #     # shot_id = 2004
    #     shot_data = csa.getShotData(shot_id)
    #     seq_code = shot_data.get("sg_sequence").get("name")
    #     # print "scene_info:",shot_data.get("code"),seq_code
    #     for seq_item in self._root_item.childItems():
    #         if seq_item.name() == seq_code:
    #             row = seq_item.row()
    #             seq_index = self.shot_proxymodel.index(row, 0)
    #             for shot_item in seq_item.childItems():
    #                 if shot_item.name() == shot_data.get("code"):
    #                     row = shot_item.row()
    #                     shot_index = self.shot_proxymodel.index(row, 0, seq_index)
    #                     break
    #     try:
    #         self._shot_view.expand(seq_index)
    #         self._shot_view.setCurrentIndex(shot_index)
    #     except:
    #         pass
    #     self._click_shot_item()
    def expand_shot_item(self):
        seq_row = self._sequence_item.row()
        seq_index = self.shot_proxymodel.index(seq_row, 0)
        shot_row = self._shot_item.row()
        shot_index = self.shot_proxymodel.index(shot_row, 0, seq_index)
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
        # if self._current_step_id in [self.__layout, self.__animation]:
        #     def_step = "Model"
        self.setupStepItems(step_items, self._step_relationship.get(template))
        # self.setupStepItems(step_items, self._step_relationship.get(template),def_step)

    def setupStepItems(self, step_items, step_data):
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
                item.setHidden(True)
                self._step_listwidget.setItemTextColor(item, self._step_listwidget._unrelated_uncheck_color)
            else:
                # if def_step == item_name:
                #     item.setCheckState(QtCore.Qt.Checked)
                # elif def_step == "All":
                item.setCheckState(QtCore.Qt.Checked)

                self._step_listwidget.setItemTextColor(item, self._step_listwidget._is_related_color)

        self._step_listwidget.setRelatedStep(step_data)

    def getStepItems(self):
        step_items = []
        for i in range(self._step_listwidget.count()):
            step_items.append(self._step_listwidget.item(i))

        return step_items

    def setStepItemsState(self, state):
        step_items = self.getStepItems()
        for item in step_items:
            self._step_listwidget.setItemsState(self._step_listwidget.row(item), state)

    def _select_step_mode(self, checked):
        for i in range(self._step_listwidget.count()):
            item = self._step_listwidget.item(i)
            if item.isHidden():
                continue
            item.setCheckState(checked)
            self._step_listwidget.checkItemState(item)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = AppDialog()
    win.show()
    sys.exit(app.exec_())
