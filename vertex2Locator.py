## -*- coding: utf-8 -*-

import maya.cmds as cmds

#vtxのポジションにロケータを作成する
for work in cmds.ls(sl=1,fl=1,l=1):
    loc = cmds.spaceLocator()[0]
    expStr = '$pos = `xform -q -ws -t "'+work+'"`;'+'\n'
    expStr += loc+'.tx = $pos[0];'+'\n'+loc+'.ty = $pos[1];'+'\n'+loc+'.tz = $pos[2];'
    print expStr
    cmds.expression(s=expStr,o=loc,ae=1,uc=all)
