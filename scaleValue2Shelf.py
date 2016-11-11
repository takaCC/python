## -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel

def myCmdWindow():
    # this will create a tiny window with a command history reporter
    if cmds.window("scale2Shelf_window",q=1,ex=1):
        cmds.deleteUI("scale2Shelf_window")
    cmds.window("scale2Shelf_window")
    cmds.columnLayout(adj=1)
    cmdWindow = cmds.cmdScrollFieldReporter("scale2Shelf_cmdWindow")
    #cmds.showWindow()
    cmds.cmdScrollFieldReporter(cmdWindow,e=1,clr=1)
    return cmdWindow

def scale2shelf():
    script = ""
    getScript = cmds.cmdScrollFieldReporter("scale2Shelf_cmdWindow",q=1,t=1)
    shelfName = mel.eval('tabLayout -query -selectTab $gShelfTopLevel')
    for work in getScript.split("\n"):
        if work.find("scale ") != -1:
            script += "scale -r -rab "
            script += work.split(" ")[-4]+" "
            script += work.split(" ")[-3]+" "
            script += work.split(" ")[-2]+" "
            script += ";\n"
    cmds.setParent(shelfName)
    cmds.shelfButton(command=script,sourceType="mel",label="scale",imageOverlayLabel="scale",image1="commandButton.png")
    #cmds.shelfButton(command=getScript,sourceType="mel",label="scale",imageOverlayLabel="scale",image1="commandButton.png")
    cmds.deleteUI("scale2Shelf_window")


#コマンドスクリプトウィンドウを作成
UIName = myCmdWindow()

#スケールマニピュレータを作成&表示
if cmds.manipScaleContext("scale2Shelf_manip",q=1,ex=1):
    cmds.deleteUI("scale2Shelf_manip")
SManip = cmds.manipScaleContext("scale2Shelf_manip",mode=2,psc="scale2shelf()")
cmds.setToolTo(SManip)
