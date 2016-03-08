## -*- coding: utf-8 -*-
import maya.cmds as cmds
def smartBake():
    #スタートとエンドのフレームを取得
    StartFrame = cmds.playbackOptions(q=1,min=1)
    EndFrame = cmds.playbackOptions(q=1,max=1)
    #アクティブなパネルを取得
    WfPanel = cmds.getPanel(wf=1)
    WfPanelType = cmds.getPanel(to=WfPanel)
    
    selArray = cmds.ls(sl=1,l=1)
    
    #isolate selectionモードにして処理の負荷を低減させる
    if WfPanelType == "modelPanel":
        cmds.select(cl=1)
        cmds.isolateSelect(WfPanel,state=1)
    
    #ベイク処理を行う
    cmds.bakeResults(selArray,simulation=1,pok=1,t=(StartFrame,EndFrame))
    cmds.filterCurve()
    
    #ビューの表示を元に戻す
    if WfPanelType == "modelPanel":
        cmds.isolateSelect(WfPanel,state=0)
    cmds.select(selArray)
