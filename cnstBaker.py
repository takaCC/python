## -*-  coding: utf-8 -*-
import maya.cmds as cmds

#選択したノードにコンストが張ってあるなら、ベイクする関数
#使い方：ノードを選択した状態で実行

def cnstBaker():
    #ベイク用関数
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
        cmds.bakeResults(selArray,simulation=1,t=(StartFrame,EndFrame))
        
        #ビューの表示を元に戻す
        if WfPanelType == "modelPanel":
            cmds.isolateSelect(WfPanel,state=0)
    
    #コンスト削除関数
    def delConst():
        for sel in cmds.ls(sl=1,fl=1,l=1):
            if cmds.objExists(sel):
                childList = cmds.listRelatives(sel,c=1,f=1)
                if childList != None:
                    for child in cmds.listRelatives(sel,c=1,f=1):
                        type = cmds.objectType(child)
                        if type.find("Constraint") > 0:
                            cmds.delete(child)
                else:
                    print "noting constraint\r"
    #コンストの張ってあるノードを取得
    ConstList = []
    for sel in cmds.ls(sl=1,fl=1,l=1):
        if cmds.listRelatives(sel,c=1,f=1):
            for child in cmds.listRelatives(sel,c=1,f=1):
                type = cmds.objectType(child)
                if type.find("Constraint") > 0:
                    ConstList.append(sel)
    
    #コンストの張ってあるノードをベイク処理
    if len(ConstList) > 0:
        cmds.select(ConstList)
        smartBake()
        cmds.select(ConstList)
        delConst()
        cmds.filterCurve()
