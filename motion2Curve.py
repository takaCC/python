## -*- coding:utf8 -*-
import maya.cmds as cmds

from Script.smartBake import *
from Script.delConst import *

def motion2Curve():
    for work in cmds.ls(sl=1,l=1):
        ValueArray = []
        loc = cmds.spaceLocator()[0]
        cmds.parentConstraint(work,loc,mo=0)
        cmds.select(loc)
        smartBake()
        delConst()
        for i in range(int(cmds.playbackOptions(q=1,min=1)),int(cmds.playbackOptions(q=1,max=1))):
            x = cmds.getAttr(loc+".tx",t=i)
            y = cmds.getAttr(loc+".ty",t=i)
            z = cmds.getAttr(loc+".tz",t=i)
            ValueArray.append((x,y,z))
        cmds.curve(p=ValueArray)
        cmds.delete(loc)
