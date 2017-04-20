## -*- coding:utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
def returnPose(SelectList):
    AttrValue = 0
    #AttrCmd = "scriptToShelf \"Pose\" \""
    AttrCmd = ""
    for work in SelectList:
        for Attr in cmds.listAttr(work,k=1,u=1,se=1):
            AttrValue = cmds.getAttr(work+"."+Attr)
            if AttrValue == True:
                AttrValue = 1
            elif AttrValue == False:
                AttrValue = 0
            AttrCmd += "catch(`setAttr \""+work+"."+Attr+"\" "+str(AttrValue)+"`);"
    return AttrCmd
