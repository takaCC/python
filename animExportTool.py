## -*- coding: utf-8 -*-
import maya.cmds as cmds

#指定したアニメーションレイヤーを書き出す関数.pathは書き出すファイル名のフルパスを記入する
def exportAnimLayer(path,exportLayer):
    cmds.select(cl=1)
    cmds.animLayer(exportLayer,e=1,writeBlendnodeDestinations=1)
    layerCurves = cmds.animLayer(exportLayer,q=1,animCurves=1)
    layerBlendNodes = cmds.animLayer(exportLayer,q=1,blendNodes=1)
    
    cmds.select(exportLayer,add=1,noExpand=1)
    
    for Acurve in layerCurves:
        cmds.select(Acurve,add=1)
    for blendNode in layerBlendNodes:
        cmds.select(blendNode,add=1)
    
    cmds.file(path,force=1,exportSelected=1,channels=0,constructionHistory=0,expressions=0,constraints=0,type="mayaBinary")

#アニメーション書き出し関数
def animExport(path,mode="Connection",layerName=None):
    if mode == "Connection":
        #もし拡張子.maが無い場合は、強制的に末尾に.maを加える
        if path.find(".ma") == -1:
            path = path+".ma"
        #選択したノードから、アニメーションを書き出し
        try:
            cmds.file(path,exportSelectedAnim=1,typ="mayaAscii",f=1)
        except:
            cmds.error("アニメーションファイルが書き出せませんでした")
        #fileの行全てを格納する配列の作成
        fileStr = []
        #ファイルを読み込み専用で開く
        f = open(path,"r")
        #ファイルを行単位に分割し、connectAttrがある行で、アニメーションノード接続先のノード名に":"を追加する
        for line in f:
            if line.find("connectAttr") > -1:
                fileStr.append(line.split(" ")[0]+" "+line.split(" ")[1]+" "+"\":"+line.split(" ")[2].split("\"")[1]+"\";\n")
            else:
                fileStr.append(line)
        #ファイルを閉じる
        f.close()
        
        #fileを書き込み専用で開く
        f = open(path,"w")
        #変換した文字列で、既存のファイルを置き換え
        for work in fileStr:
            f.write(work)
        #ファイルを閉じる
        f.close()
    elif mode == "Layer":
        #もし拡張子.mbが無い場合は、強制的に末尾に.mbを加える
        if path.find(".mb") == -1:
            path = path+".mb"
        #キーを保存
        cmds.copyKey()
        
        #スタートフレームに移動
        cmds.currentTime(cmds.playbackOptions(q=1,min=1))
        
        #レイヤーネームの指定がある場合はそのままに、ない場合はデフォルトネームを指定する
        if layerName == None:
            layerName = "MotionLayer"
        
        #モーションの入ったアニムレイヤーを作成
        MotionLayer = cmds.animLayer(layerName, mute=False, solo=False, override=True, passthrough=False, lock=False)
        cmds.animLayer(cmds.animLayer(q=1,root=1),e=True,sel=False)
        #アニムレイヤーを設定
        cmds.animLayer(MotionLayer,e=True,aso=True,passthrough=True)
        #アニムレイヤーを選択&キーのペースト
        cmds.animLayer(MotionLayer,e=True,sel=True,preferred=True)
        cmds.pasteKey(al=MotionLayer)
        
        exportAnimLayer(path,MotionLayer)
        
        cmds.delete(MotionLayer)

#書き出し先を指定する関数
def AnimExportTool_Path_Func():
    expPath = cmds.fileDialog2(fm=0,dialogStyle=2)
    cmds.textField("AnimExportTool_Path_UI",e=1,tx=expPath[0])

#アニメーションファイルを書き出す関数
def AnimExportTool_ExportFile_Func():
    #Export Anim Modeの場合
    if cmds.radioButton("AnimExportTool_ModeAnim_UI",q=1,sl=1):
        #書き出し先の代入
        path = cmds.fileDialog2(fm=0,dialogStyle=2,ff='Maya ASCII (*.ma)')[0]
        print path
        animExport(path,mode="Connection",layerName=None)
    #Export Layer Modeの場合
    elif cmds.radioButton("AnimExportTool_ModeLayer_UI",q=1,sl=1):
        #書き出し先の代入
        path = cmds.fileDialog2(fm=0,dialogStyle=2,ff='Maya Binary (*.mb)')[0]
        print path
        animExport(path,mode="Layer",layerName=path.split("/")[-1])

#UI作成
if cmds.window("AnimExportTool",ex=1):
    cmds.deleteUI("AnimExportTool")
cmds.window("AnimExportTool",h=150,w=800,s=1)
cmds.columnLayout(adj=1)
cmds.intSlider(en=0)
cmds.text("選択したノードのアニメーションを書き出します")
cmds.intSlider(en=0)
cmds.setParent("..")
cmds.columnLayout(adj=1,rs=10)
cmds.rowLayout(nc=2)
cmds.radioCollection()
cmds.radioButton("AnimExportTool_ModeAnim_UI",l="Export Anim Mode (.ma File)",sl=0)
cmds.radioButton("AnimExportTool_ModeLayer_UI",l="Export Layer Mode (.mb File)",sl=1)
cmds.setParent("..")
cmds.button("run",c="AnimExportTool_ExportFile_Func()")
cmds.showWindow("AnimExportTool")
