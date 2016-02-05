## -*- coding: utf-8 -*-
import maya.cmds as cmds

#指定したアニメーションレイヤーを書き出す関数.pathは書き出すファイル名のフルパスを記入する
def exportAnimLayer(path,exportLayer):
    """
    baseLayerName = cmds.animLayer(q=1,root=1)
    exportLayers = []
    if len(cmds.ls(type="animLayer")):
        for work in cmds.ls(type="animLayer"):
            if work != baseLayerName:
                exportLayers.append(work)
    
    #アニメーションレイヤーがある場合、アニメーションレイヤーを書き出す
    if len(exportLayers):
        for work in exportLayers:
            cmds.select(cl=1)
            for Alayer in exportLayers:
                cmds.animLayer(Alayer,e=1,writeBlendnodeDestinations=1)
                layerCurves = cmds.animLayer(Alayer,q=1,animCurves=1)
                layerBlendNodes = cmds.animLayer(Alayer,q=1,blendNodes=1)
                cmds.select(Alayer,add=1,noExpand=1)
                for Acurve in layerCurves:
                    cmds.select(Acurve,add=1)
                for blendNode in layerBlendNodes:
                    cmds.select(blendNode,add=1)
            cmds.file(path,force=1,exportSelected=1,channels=0,constructionHistory=0,expressions=0,constraints=0,type="mayaBinary")
    """
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

#指定したアニメーションレイヤーを書き出す関数(全レイヤー)。pathは書き出すファイル名のフルパスを記入する
def exportAnimLayerALL(path):
    baseLayerName = cmds.animLayer(q=1,root=1)
    exportLayers = []
    if len(cmds.ls(type="animLayer")):
        for work in cmds.ls(type="animLayer"):
            if work != baseLayerName:
                exportLayers.append(work)
    
    #アニメーションレイヤーがある場合、アニメーションレイヤーを書き出す
    if len(exportLayers):
        layerCurves = []
        layerBlendNodes = []
        exportCheck = 1
        for work in exportLayers:
            cmds.select(cl=1)
            for Alayer in exportLayers:
                cmds.animLayer(Alayer,e=1,writeBlendnodeDestinations=1)
                #アニメーションレイヤーにアニムカーブやblendNodesが含まれている場合は配列に代入
                if cmds.animLayer(Alayer,q=1,animCurves=1) != None and cmds.animLayer(Alayer,q=1,blendNodes=1) != None:
                    for node in cmds.animLayer(Alayer,q=1,animCurves=1):
                        layerCurves.append(node)
                    for node in cmds.animLayer(Alayer,q=1,blendNodes=1):
                        layerBlendNodes.append(node)
        #アニメーションカーブ等が無い場合、書き出し処理を行わない
        if len(layerCurves) > 0  and len(layerBlendNodes) > 0:
            cmds.select(exportLayers,add=1,noExpand=1)
            cmds.select(layerBlendNodes,layerCurves,add=1)
            cmds.file(path,force=1,exportSelected=1,channels=0,constructionHistory=0,expressions=0,constraints=0,type="mayaBinary")
            cmds.select(cl=1)
