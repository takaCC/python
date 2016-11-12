## -*- coding:utf-8 -*-
import maya.cmds as cmds

#showBufferをOnにする。デフォルトのグラフエディタのみ対応
#focusPanel = cmds.getPanel(wf=1)
if cmds.animCurveEditor("graphEditor1GraphEd",ex=1):
    cmds.animCurveEditor("graphEditor1GraphEd",edit=1,showBufferCurves=1)

#標準のSimplify Curveを関数化。
#事前にBufferCurveかけるようにした。
def mySimplifyCurve(tt=10.0,vt=0.0):
    cmds.bufferCurve( animation='keys', overwrite=True )
    cmds.simplify(animation='keysOrObjects',timeTolerance=tt,valueTolerance=vt)
