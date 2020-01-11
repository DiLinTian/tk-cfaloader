#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/24 14:31
@ description:
    

'''

import connect_shotgun
# import sgtk
# def getSceneSGData():
#     _engine = sgtk.platform.current_engine()
#     _context = _engine.context
#     _entity = _context.entity
#     _task = _context.task
#     _step = _context.step
#     _user = _context.user
#     _project = _context.project
#
#     data = {"engine":_engine,
#             "context":_context,
#             "entity":_entity,
#             "task":_task,
#             "step":_step,
#             "user":_user,
#             "project":_project}
#     return data

sg = connect_shotgun._shotgun()

project_id = 99
def getShotEntity(fields,shot_id):
    shot = sg.find_one("Shot",[["id","is",shot_id]],fields)
    return shot

def getSequenceEntity(fields,project_id):
    sequence = sg.find("Sequence",[["project.Project.id","is",project_id]],fields)
    return sequence

def getSequenceData():
    # scene_data = getSceneSGData()
    # project_id = scene_data.get("project").get("id")

    fields = ["shots","code"]
    sequence_data = getSequenceEntity(fields,project_id)
    return sequence_data

def getShotData(shot_id):
    fields = ["assets","code","sg_sequence"]
    shot_data = getShotEntity(fields,shot_id)
    return shot_data
def getPublishFilesFun(entity_id,step_id,mode = "Asset"):
    # id = 14: model
    # id = 15: shading
    # id = 106: animation
    # id = 35:layout
    publishFiles = sg.find("PublishedFile",
                          [["entity.%s.id"%mode, "is", entity_id], ["task.Task.step.Step.id", "is", step_id]],
                          ["image", "published_file_type", "version_number", "path", "task", "code"])

    publish_file_data = {}
        # Maya Scene :[{publishfiledata},]
        #
        # MAYA XGGeometry:[{publishfiledata},]
        # MAYA XGShader:[{publishfiledata},]
        # Maya XGen:[{publishfiledata},]
        # publishfiledata: {'version_number': 1, 'task': {'type': 'Task', 'id': 26268, 'name': 'groom'},
        # 'image': 'http://sg.anime.com/thumbnail/api_image/40996?AccessKeyId=uTbPnnWUNhn2nSG7Agrp&Expires=1578649444&Signature=fmXKhKVb6ux752a%2Fb9B66X5p%2FJX5cVZh2pxG3eKI7l0%3D',
        # 'published_file_type': {'type': 'PublishedFileType', 'id': 2, 'name': 'Maya Scene'}, 'code': 'huahua_GRM.v001.ma',
        # 'path': {'local_path_windows': '\\\\3par\\ibrix01\\shotgun\\shotgun_work\\tdprojects\\assets\\Character\\huahua\\GRM\\publish\\maya\\huahua_GRM.v001.ma',
        # 'name': 'huahua_GRM.v001.ma', 'local_path_linux': '/shotgun/shotgun_work/tdprojects/assets/Character/huahua/GRM/publish/maya/huahua_GRM.v001.ma',
        # 'url': 'file://\\\\3par\\ibrix01\\shotgun\\shotgun_work\\tdprojects\\assets\\Character\\huahua\\GRM\\publish\\maya\\huahua_GRM.v001.ma',
        # 'local_storage': {'type': 'LocalStorage', 'id': 2, 'name': 'CFA  LocalStorage'},
        # 'local_path': '\\\\3par\\ibrix01\\shotgun\\shotgun_work\\tdprojects\\assets\\Character\\huahua\\GRM\\publish\\maya\\huahua_GRM.v001.ma',
        # 'content_type': None, 'local_path_mac': None, 'type': 'Attachment', 'id': 41787, 'link_type': 'local'}, 'type': 'PublishedFile', 'id': 8762}


    for pf in publishFiles:
        p_type = pf.get("published_file_type").get("name")
        publish_file_data.setdefault(p_type,[]).append(pf)
    _file_data = {}
    for k,v in publish_file_data.iteritems():
        last_file = getMaxNumberPublishedFile(v)
        _file_data[k] = last_file


    return _file_data
    # return publishFiles
def getAssetPublishFiles(entity_id,step_id = 14):
    # id = 14: model
    # id = 15: shading
    # id = 106: animation
    # id = 35:layout

    ma_files,abc_files = getPublishFilesFun(entity_id,step_id)
    if not ma_files and not abc_files:
        return None

    last_abc_files = getMaxNumberPublishedFile(abc_files)
    last_ma_files = getMaxNumberPublishedFile(ma_files)
    last_files = {"maya":last_ma_files,
                  "abc":last_abc_files}
    return last_files
def getShotPublishFiles(entity_id,step_id):
    # entity_id = 2112
    ma_files,abc_files = getPublishFilesFun(entity_id,step_id,"Shot")
    if not ma_files and not abc_files:
        return None
    last_abc_files = delSameFiles(abc_files)
    last_ma_files = getMaxNumberPublishedFile(ma_files)
    last_files = {"maya": last_ma_files,
                  "abc": last_abc_files}

    return last_files
def delSameFiles(files_data):
    del_same_file = {}
    for file in files_data:
        code = file.get("code")
        del_same_file[code] = file

    last_files= []
    for k, v in del_same_file.iteritems():
        last_files.append(v)
    return last_files
def getMaxNumberPublishedFile(published_files):
    last_published_file = None
    max = 0
    for pf in published_files:
        vn = pf.get("version_number")
        if max < vn:
            max = vn
            last_published_file = pf
    return last_published_file

if __name__ == '__main__':
    for k,v  in  getPublishFilesFun(1984,138).iteritems():
        print getMaxNumberPublishedFile(v).get('code')
    # print getAssetPublishFiles(1773)