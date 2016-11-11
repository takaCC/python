## -*- coding: utf-8 -*-
import maya.cmds as cmds

#カーブシェイプをコピペする
curveName = cmds.ls(sl=1,l=1)
originalShape = cmds.listRelatives(curveName[0],s=1,f=1)[0]
targetShapeName = cmds.listRelatives(curveName[1],s=1,f=0)[0]
targetShape = cmds.listRelatives(curveName[1],s=1,f=1)[0]
dup = cmds.duplicate(curveName[0],renameChildren=1)[0]
dupShape = cmds.listRelatives(dup,s=1)[0]

cmds.parent(dupShape,curveName[1],r=1,s=1)

cmds.delete(dup,targetShape)
cmds.rename(dupShape,targetShapeName)


#originalカーブのエディットポイント全てを選択
cmds.select(originalShape+".cv[*]")

#オリジナルカーブポイントを、ターゲットカーブポイントに反映させる
script = ""
for i in range(0,len(cmds.ls(sl=1,fl=1,l=1))):
    work = originalShape+".cv["+str(i)+"]"
    pos = cmds.xform(work,q=1,ws=1,t=1,a=1)
    work = work.replace(originalShape,curveName[1])
    print work,originalShape,curveName[1]
    cmd= "cmds.move("+str(pos[0])+","+str(pos[1])+","+str(pos[2])+",\""+work+"\",a=1)"
    eval(cmd)
cmds.select(curveName[1])
