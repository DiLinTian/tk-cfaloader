#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@ author：huangsheng
@ date: 2019/9/24 11:08
@ description:
    

'''
import sys,os

class ItemNode(object):
    def __init__(self,data,parent = None):
        '''
        
        :param data: 
                
            shotgun entity data
            {code:code,type:entity_code,id:id}
        :param parent: 
        '''
        if not isinstance(data,dict):
            raise RuntimeError,"The input data should be a dictionary!"
        self._parent_item = parent
        self._data = data
        self._child_items = []
        if parent is not None:
            parent.addChild(self)

    def addChild(self,item):
        self._child_items.append(item)
    def typeInfo(self):
        return "ITEM"
    def insertChild(self,position,child):
        if position < 0 or position > len(self._child_items):
            return False
        self._child_items.insert(position,child)
        child._parent = self
        return True

    def removeChild(self,position):
        if position < 0 or position > len(self._child_items):
            return False
        child = self._child_items.pop(position)
        child._parent = None
        return True
    def name(self):
        return self._data["item_name"]
    def icon(self):
        return self._data["item_icon"]
    def setName(self,name):
        self._data["item_name"] = name
    def child(self,row):
        return self._child_items[row]
    def childCount(self):
        return len(self._child_items)
    def parent(self):
        return self._parent_item
    def row(self):
        if self._parent_item is not None:
            return self._parent_item._child_items.index(self)

    def data(self):
        return self._data
    def childItems(self):
        return self._child_items
class SequenceItemNode(ItemNode):
    def __init__(self,sequence_data,parent = None):
        super(SequenceItemNode, self).__init__(sequence_data,parent)

    def typeInfo(self):
        return "SEQUENCEITEM"


class ShotItemNode(ItemNode):
    def __init__(self, shot_data, parent=None):
        super(ShotItemNode, self).__init__(shot_data,parent)

    def typeInfo(self):
        return "SHOTITEM"

