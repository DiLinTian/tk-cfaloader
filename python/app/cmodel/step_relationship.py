#!/urelationship/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/10/14 16:40
@ description:
    

'''
import os
import yaml
dir = os.path.dirname(__file__)
relationship = dir + "/step_relationship.yml"
step_code = dir + '/step_code.yml'
step_id = dir + '/step_id.yml'
task_templates = dir + '/_template.yml'
def getData():
    step_data = {}
    with open(relationship,"r") as f:
        relationship_data = yaml.load(f,Loader = yaml.FullLoader)
        step_data['relationship'] = relationship_data
    with open(step_code,'r') as f:
        step_code_data = yaml.load(f,Loader = yaml.FullLoader)
        step_data['step_code'] = step_code_data
    with open(step_id,'r') as f:
        step_id_data = yaml.load(f,Loader = yaml.FullLoader)
        step_data['step_id'] = step_id_data
        step_data["step"] = step_id_data.keys()

    with open(task_templates) as f:
        task_template = yaml.load(f,Loader = yaml.FullLoader)
        step_data['template'] = task_template


    return step_data

# print getData().get("step")
if __name__ == '__main__':
    with open(relationship,"r") as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        print data

