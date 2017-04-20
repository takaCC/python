## -*- coding:utf-8 -*-
import maya.cmds as cmds
if cmds.window("CaptureEditor",ex=1):
    cmds.deleteUI("CaptureEditor")
w = cmds.window("CaptureEditor")
cmds.columnLayout(adj=1)
cmds.button(l="アニメーションレイヤのモードを切り替える")
cmds.button(l="現在フレームを、ベースレイヤーのポーズに変換")
cmds.button(l="タイムスライダ上のキーフレームを、ベースレイヤーのポーズに変換")
cmds.showWindow(w)
