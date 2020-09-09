#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2020/5/22 13:47
@ description:
    

'''
import os
import yaml
dir = os.path.dirname(__file__)
# file_type = dir + "/file_type.yml"
file_type_map = dir + '/file_type_map.yml'

# def get_file_data(step):
#     _file_type_data = {}
#     _step_file_type = None
#     with open(file_type,'r') as f:
#         _data = yaml.load(f,Loader = yaml.FullLoader)
#         _step_file_type = _data.get(step)
#         _file_type_data[step] = _step_file_type
#
#     return _file_type_data
def get_file_map():

    with open(file_type_map,'r') as f:
        _data = yaml.load(f,Loader=yaml.FullLoader)

    return _data


if __name__ == '__main__':
    # print get_file_data("Preshot")
    print get_file_map()