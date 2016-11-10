## -*- coding:utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
import maya.app.general.pointOnPolyConstraint as ppc

from Script.smartBake import *
from Script.delConst import *

def Build_Hierarchy(rootBake=False,rootRotOrder=0,childRotOrder=0):
    locators = []
    
    selections = cmds.ls(sl=1,l=1,fl=1)
    shortName = cmds.ls(sl=1,fl=1)
    
    if len(selections):
        
        #もしルートがバーテックスの場合
        if shortName[0].find(".vtx[") != -1:
            shortName[0] = shortName[0].replace(".","_").replace("[","_").replace("]","_")
        
        #ロケータ名の設定(リネーム機能付き)
        rootName = shortName[0]+"_loc"
        if cmds.objExists(rootName):
            for work in cmds.ls(rootName):
                cmds.rename(work,work+"_1")
        
        #ロケータ作成＆コンスト等
        root = cmds.spaceLocator(n=rootName)[0]
        cmds.setAttr(root+".rotateOrder",rootRotOrder)
        
        #ルートの選択オブジェクトがどのタイプかによってコンストレインを分岐
        if cmds.objectType(selections[0]) != "mesh":
            cmds.parentConstraint(selections[0],root,mo=0,w=1,st=["none"],sr=["none"])
        if cmds.objectType(selections[0]) == "mesh":
            #pointOnPolyコンストを実行
            cmds.select(selections[0],root)
            popConst = cmds.pointOnPolyConstraint(w=1,mo=0,sk=["none"])[0]
            
            #最後に作ったpointOnPolyConstraintの、UV値を出してくれるっぽい？            
            U_AttrName = ppc.assembleCmd().split("+\".")[1].split("\"")[0]
            U_value = ppc.assembleCmd().split(" ")[3].replace(";","")
            
            V_AttrName = ppc.assembleCmd().split("+\".")[-1].split("\"")[0]
            V_value = ppc.assembleCmd().split(" ")[-1]
            
            cmds.setAttr(popConst+"."+U_AttrName,float(U_value))
            cmds.setAttr(popConst+"."+V_AttrName,float(V_value))
        
        #ルートノードをベイクする場合の処理
        if rootBake:
            cmds.select(rootName)
            smartBake()
            delConst()
            cmds.filterCurve()
        
        for i in range(1,len(selections)):
            #ロケータ名の設定(リネーム機能付き)
            childName = shortName[i]+"_loc"
            if cmds.objExists(childName):
                for work in cmds.ls(childName):
                    cmds.rename(work,work+"_1")
            
            #ロケータ作成＆コンスト等
            child = cmds.spaceLocator(n=childName)[0]
            cmds.setAttr(child+".rotateOrder",childRotOrder)
            cmds.parentConstraint(selections[i],child)
            cmds.parent(child,root)
            locators.append(root+"|"+child)
    
    cmds.select(locators)
    smartBake()
    delConst()
    cmds.filterCurve()
    
    #逆コンスト処理
    for i in range(1,len(selections)):
        try:
            cmds.parentConstraint(locators[i-1],selections[i])
            continue
        except:
            print "not parentConstraint :"+selections[i]
        try:
            cmds.pointConstraint(locators[i-1],selections[i])
        except:
            print "not pointConstraint :"+selections[i]
        try:
            cmds.orientConstraint(locators[i-1],selections[i])
        except:
            print "not orientConstraint :"+selections[i]

width = 170
if cmds.window("Build_Hierarchy",ex=1) == 1:
    cmds.deleteUI("Build_Hierarchy")
cmds.window("Build_Hierarchy",t="Build_Hierarchy",w=width)
cmds.columnLayout(w=width)
cmds.optionMenu("rootRotateOrder",l="Root Rotate Order",w=width)
cmds.menuItem(p="rootRotateOrder",label="xyz")
cmds.menuItem(p="rootRotateOrder",label="yzx")
cmds.menuItem(p="rootRotateOrder",label="zxy")
cmds.menuItem(p="rootRotateOrder",label="xzy")
cmds.menuItem(p="rootRotateOrder",label="yxz")
cmds.menuItem(p="rootRotateOrder",label="zyx")
cmds.optionMenu("childRotateOrder",l="Child Rotate Order",w=width)
cmds.menuItem(p="childRotateOrder",label="xyz")
cmds.menuItem(p="childRotateOrder",label="yzx")
cmds.menuItem(p="childRotateOrder",label="zxy")
cmds.menuItem(p="childRotateOrder",label="xzy")
cmds.menuItem(p="childRotateOrder",label="yxz")
cmds.menuItem(p="childRotateOrder",label="zyx")
cmds.checkBox("Build_Hierarchy_rootBake",l="rootBake?")
cmds.button(l="run",w=width,c="Build_Hierarchy(cmds.checkBox(\"Build_Hierarchy_rootBake\",q=1,v=1),cmds.optionMenu(\"rootRotateOrder\",q=1,sl=1)-1,cmds.optionMenu(\"childRotateOrder\",q=1,sl=1)-1)")
cmds.showWindow("Build_Hierarchy")
