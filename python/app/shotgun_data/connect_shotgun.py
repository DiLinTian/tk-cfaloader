#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/24 14:26
@ description:
    

'''

# from tank_vendor import shotgun_api3
import shotgun_api3

login = "script_it_2"
password = "wrcduwrnsdiyzz6Aeatmwp^if"
server = "http://sg.anime.com"
def _shotgun():
    return shotgun_api3.Shotgun(server,login,password)

# from sgtk.util import shotgun
# def _shotgun():
#     sg = shotgun.create_sg_connection()
#     return sg