#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2020/1/14 15:25
@ description:
    

'''
import os
import re
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import xgenm as xg
from func import replace_special_character as rsc

def createReference(filepath,namesapce = None):
    if not os.path.exists(filepath):
        raise Exception("File not found on disk - '%s'" % filepath)
    if namesapce is None:
        basename = os.path.basename(filepath)
        namespace = basename.split('.')[0]
    pm.system.createReference(filepath, loadReferenceDepth="all",
                              mergeNamespacesOnClash=False,
                              namespace=namespace)

    reference_node = cmds.referenceQuery(filepath, referenceNode=True)
def importMayaFile(path,namespace = ":"):
    cmds.file(path, i=True, renameAll=True, namespace=namespace, loadReferenceDepth="all", preserveReferences=True)
def _shader_hookup_data(hookup_prefix):
    shader_hookups = {}  # {geo:shader}
    for node in cmds.ls(type="script"):
        node_parts = node.split(":")
        node_base = node_parts[-1]
        node_namespace = ":".join(node_parts[:-1])
        if not node_base.startswith(hookup_prefix):
            continue
        obj_pattern = node_base.replace(hookup_prefix, "")  # + "\d*"
        obj_pattern = "^" + obj_pattern + "$"
        shader = cmds.scriptNode(node, query=True, beforeScript=True)
        shader_hookups[obj_pattern] = node_namespace + ":" + shader

    return shader_hookups
def _hookup_xgshaders(xgshader_items):
    XGSHADER_HOOKUP = "XGSHADER_HOOKUP_"
    for item in xgshader_items:
        item_data = item.itemData()
        _file_path = item_data.get('path').get('local_path_windows')
        _name = item_data.get('code')
        collection = _name.split("_GRM")[0]
        if not cmds.objExists(collection):
            cmds.file(_file_path, rr=True)
            raise Exception("%s dose not exists!" % collection)
        _hookup_shaders(XGSHADER_HOOKUP, 'xgmDescription', collection)

    palettes = xg.palettes()
    for palette in palettes:
        descriptions = list(xg.descriptions(str(palette)))
        mel.eval('xgmDensityComp -f -pb {"%s"};' % descriptions[-1])
def _hookup_shaders(hookup_prefix,node_type,collection = None):

    # find all shader hookup script nodes and extract the mesh object info
    # print "reference node:", reference_node
    # hookup_prefix = "SHADER_HOOKUP_"
    shader_hookups = _shader_hookup_data(hookup_prefix)
    # if the object name matches an object in the file, connect the shaders
    if node_type == "mesh":
        nodes = cmds.ls(transforms=True) or []
    elif node_type == "xgmDescription":
        try:
            import xgenm as xg
        except Exception, e:
            raise Exception(e)
        if collection is None:
            raise Exception("The keyword 'collection' is None!")
        nodes = xg.descriptions(collection)

    for node in nodes:
        node_shape = cmds.listRelatives(node, type=node_type, c=True)
        if not node_shape:
            continue
        node_base = node.split(":")[-1]
        node_long_name = cmds.ls(node, l=True)[0]
        sp = node_long_name.split("|")
        node_temp = None
        node_parents = sp[:-1]
        node_parent_base_list = []
        for pa in node_parents:
            if pa == "":
                continue
            node_parent_base_list.append(pa.split(":")[-1])
        node_parent_base_list.append(node_base)
        node_temp = "_".join(node_parent_base_list)

        for (obj_pattern, shader) in shader_hookups.iteritems():
            if re.search(obj_pattern, node_temp, re.IGNORECASE):
                # assign the shader to the object
                # print obj_pattern,node_temp
                if not cmds.objExists(shader):
                    continue
                cmds.select(node, replace=True)
                cmds.hyperShade(assign=shader)

def _hookup_xgen(path):

    try:
        import xgenm as xg
        import xgenm.ui.dialogs.xgImportFile as xif

    except Exception, e:
        raise Exception(e)
    from func import cfaXgenAPI
    from cfa_widgets import CFAUI
    from cfa_widgets import *
    import shutil
    work_file = cmds.file(q=True, sn=True)
    if not work_file:
        CFAUI.messageBox("Please save the file first!")
        return
    current_dir = os.path.dirname(work_file)
    # all_files = os.listdir(current_dir)
    # if "xgen" in all_files:
    #     shutil.rmtree(current_dir + "/xgen")
    basename = os.path.basename(path)
    collection = (basename.split('__')[-1]).split('.')[0]
    collection_path = current_dir + "/xgen/collections/" +collection
    if os.path.isdir(collection_path):
        # ret = CFAUI.warningBox("---%s--- already exists in \n\t Will you delete it and continue?" % (collection_path))
        # if ret == QMessageBox.Ok:
        #     shutil.rmtree(collection_path)
        # else:
        #     return False
        shutil.rmtree(collection_path)
    path = rsc.replaceSpecialCharacter(path)
    print "xgen-path:", path
    validator = xif.Validator(xg.ADD_TO_NEW_PALETTE, None)
    cfaXgenAPI.importBindPalette(str(path), '', validator, True)
    return True


def _hookup_simcrv(path):
    try:
        import xgenm as xg
        import xgenm.xgGlobal as xgg
    except Exception, e:
        raise Exception(e)
    print "link sim curve..."
    path = str(rsc.replaceSpecialCharacter(path))
    basename = os.path.basename(path)
    _SIMCRV = "_SIMCRV"

    description = str(basename.split(_SIMCRV)[0])
    palette = str(xg.palette(description))
    _object_type = str(xg.objects(palette, description)[2])
    de = xgg.DescriptionEditor
    # use cache
    xg.setAttr(
        str("useCache"),
        str("1"),
        palette,
        description,
        _object_type
    )
    # live mode :0
    xg.setAttr(
        str("liveMode"),
        str("0"),
        palette,
        description,
        _object_type
    )
    xg.setAttr(
        str("cacheFileName"),
        path,
        palette,
        description,
        _object_type
    )

    de.update()