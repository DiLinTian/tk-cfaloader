#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/24 14:31
@ description:
    

'''
import sgtk
import os
import connect_shotgun
logger = sgtk.platform.get_logger(__name__)
def getSceneSGData():
    _engine = sgtk.platform.current_engine()
    _context = _engine.context
    _entity = _context.entity
    _task = _context.task
    _step = _context.step
    _user = _context.user
    _project = _context.project

    data = {"engine":_engine,
            "context":_context,
            "entity":_entity,
            "task":_task,
            "step":_step,
            "user":_user,
            "project":_project}
    return data

sg = connect_shotgun._shotgun()

# project_id = 113
def getShotEntity(fields,shot_id):
    shot = sg.find_one("Shot",[["id","is",shot_id]],fields)
    return shot

def getSequenceEntity(fields,project_id):
    sequence = sg.find("Sequence",[["project.Project.id","is",project_id]],fields)
    return sequence
def getSequenceEntity2(fields,sequence_id):
    sequence = sg.find_one("Sequence",[["id","is",sequence_id]],fields)
    return sequence

def getSequenceData():
    scene_data = getSceneSGData()
    project_id = scene_data.get("project").get("id")

    fields = ["shots","code"]
    sequence_data = getSequenceEntity(fields,project_id)
    return sequence_data
def getSequenceData2(sequence_id):
    fields = ["shots", "code"]
    sequence_data = getSequenceEntity2(fields, sequence_id)
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
                          ["image", "published_file_type", "version_number", "path", "task", "code",'entity'])

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
        if p_type == "Alembic Cache":
            task = pf.get('task')
            task_find = sg.find_one('Task', [['id', 'is', task.get('id')]], ['step'])
            step_id = task_find.get('step').get('id')
            if step_id in [15]:
                continue
        publish_file_data.setdefault(p_type,[]).append(pf)
    _file_data = {}
    # publishtype , publishfiles
    for k,v in publish_file_data.iteritems():
        # print k
        temp_data = {}
        for vv in v:

            if k in ["Maya Shader Network"]:
                task = vv.get('task')
                task_find = sg.find_one('Task',[['id','is',task.get('id')]],['step'])
                step_code = task_find.get('step').get('code')
                temp_data.setdefault(k,{}).setdefault(step_code,[]).append(vv)
            else:
                code = vv.get('code').split('.')[0]
                temp_data.setdefault(k,{}).setdefault(code,[]).append(vv)
        for pt,pfs_data in temp_data.iteritems():
            for ac,pfs in pfs_data.iteritems():
                last_file_data = getMaxNumberPublishedFile(pfs)
                pub_path = last_file_data.get('path')
                if pub_path is None:
                    continue
                win_path = pub_path.get('local_path_windows')
                if win_path is None:
                    continue
                if os.path.exists(win_path):
                    _file_data.setdefault(k,[]).append(last_file_data)
                else:
                    logger.warn('File not found on disk. -"%s"-'%win_path)
                    # print ('File not found on disk. -"%s"-'%win_path)
    return _file_data
def getMaxNumberPublishedFile(published_files):
    last_published_file = None
    max = 0
    for pf in published_files:
        vn = pf.get("version_number")
        if max < vn:
            max = vn
            last_published_file = pf
    return last_published_file
def getStepByTask(task_id):
    task = sg.find_one("Task",[['id','is',task_id]],['step'])
    return task.get('step')
if __name__ == '__main__':
    for k,v in getPublishFilesFun(2004,106,"Shot").iteritems():
        for vv in v:
            print k,vv.get('code')
