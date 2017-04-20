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

if len(cmds.ls(sl=1)):
    #変数の初期化
    poseCmds = []
    frames = []
    
    aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
    animCurves = cmds.timeControl( aPlayBackSliderPython, q=True, animCurveNames=True)
    
    #アニメーションのあるフレームを取得
    if animCurves != None:
        for work in animCurves:
            for frame in cmds.keyframe(work,q=1,tc=1):
                frames.append(frame)
    frames = list(set(frames))
    frames.sort()
    
    #フレーム毎のポーズを取得
    for frame in frames:
        cmds.currentTime(frame)
        poseCmds.append(returnPose(cmds.ls(sl=1)))
    
    #現在のアニメーションレイヤのモードを切り替える(add,overrideのToggle)
    for work in cmds.ls(typ="animLayer"):
        if cmds.animLayer(work,q=1,sel=1):
            value = cmds.getAttr(work+".override")
            cmds.setAttr(work+".override",not value)
    
    #取得しておいたポーズを各フレームに反映させる
    i = 0
    for frame in frames:
        cmds.currentTime(frame)
        mel.eval(poseCmds[i])
        i += 1
