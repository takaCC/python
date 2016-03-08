## -*- coding: utf-8 -*-
import maya.cmds as cmds
import time
from Script.smartBake import smartBake

def smartBake_TEST():
    startTime = time.time()
    
    #フレーム範囲を取得
    minFrame = int(cmds.playbackOptions(q=1,min=1))
    maxFrame = int(cmds.playbackOptions(q=1,max=1))
    
    #選択ノードの取得
    Sel = cmds.ls(sl=1,l=1)
    
    #Attr格納用の配列[frame][trans:0 or rotate:1][X:0 or Y:1 or Z:2]という多重配列の構造
    Sel_Attr = []
    
    
    #------------------------ベイク処理----------------------------------
    for work in cmds.ls(sl=1,l=1):
        Sel_Attr = [[[cmds.getAttr(work+".tx",t=frame),cmds.getAttr(work+".ty",t=frame),cmds.getAttr(work+".tz",t=frame)],[cmds.getAttr(work+".rx",t=frame),cmds.getAttr(work+".ry",t=frame),cmds.getAttr(work+".rz",t=frame)]] for frame in range(minFrame,maxFrame)]
        
        for frame in range(minFrame,maxFrame+1):
            cmds.setKeyframe(work+".tx",t=frame,v=Sel_Attr[frame][0][0])
            cmds.setKeyframe(work+".ty",t=frame,v=Sel_Attr[frame][0][1])
            cmds.setKeyframe(work+".tz",t=frame,v=Sel_Attr[frame][0][2])
            cmds.setKeyframe(work+".rx",t=frame,v=Sel_Attr[frame][1][0])
            cmds.setKeyframe(work+".ry",t=frame,v=Sel_Attr[frame][1][1])
            cmds.setKeyframe(work+".rz",t=frame,v=Sel_Attr[frame][1][2])
    
    endTime = time.time() - startTime
    print endTime
