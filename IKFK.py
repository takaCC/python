## ** coding:utf-8 **
import maya.cmds as cmds
import maya.mel as mel

import Script.nodeNameChecker2
reload(Script.nodeNameChecker2)
from Script.nodeNameChecker2 import nodeNameChecker2
from Script.selLoc import *

spanNum = 3
degreeNum = 2
jointDirection = "x"

#アトリビュートをロック&ハイドする関数
def lockAndHideAttr(node,attr=[],lock=True,cb=False):
    for work in attr:
        cmds.setAttr( node+"."+work,lock=lock,keyable=cb,channelBox=cb )

#RIG用のカーブを作成するスクリプト
def createCurveRIG(type,n=""):
    if type == "box":
        box = [(0.5, 0.5, 0.5000000000000002), (0.5, -0.5, 0.5000000000000002), (0.5, -0.5, -0.4999999999999998), (0.5, 0.5, -0.4999999999999998), (0.5, -0.5, -0.4999999999999998), (-0.5, -0.5, -0.4999999999999998), (-0.5, 0.5, -0.4999999999999998), (-0.5, -0.5, -0.4999999999999998), (-0.5, -0.5, 0.5000000000000002), (-0.5, 0.5, 0.5000000000000002), (-0.5, -0.5, 0.5000000000000002), (0.5, -0.5, 0.5000000000000002), (0.5, 0.5, 0.5000000000000002), (0.5, 0.5, -0.4999999999999998), (-0.5, 0.5, -0.4999999999999998), (-0.5, 0.5, 0.5000000000000002), (0.5, 0.5, 0.5000000000000002)]
        c = cmds.curve(p=box,d=1,n=n)
        return c
    elif type == "circle":
        box = [(0.5, 0.5, 0.5000000000000002), (0.5, -0.5, 0.5000000000000002), (0.5, -0.5, -0.4999999999999998), (0.5, 0.5, -0.4999999999999998), (0.5, -0.5, -0.4999999999999998), (-0.5, -0.5, -0.4999999999999998), (-0.5, 0.5, -0.4999999999999998), (-0.5, -0.5, -0.4999999999999998), (-0.5, -0.5, 0.5000000000000002), (-0.5, 0.5, 0.5000000000000002), (-0.5, -0.5, 0.5000000000000002), (0.5, -0.5, 0.5000000000000002), (0.5, 0.5, 0.5000000000000002), (0.5, 0.5, -0.4999999999999998), (-0.5, 0.5, -0.4999999999999998), (-0.5, 0.5, 0.5000000000000002), (0.5, 0.5, 0.5000000000000002)]
        c = cmds.curve(p=box,d=1,n=n)
        return c

#1番目と2番目に選択したジョイント間の階層を返す関数
def returnSelectHierarchy():
    firstSel = cmds.ls(sl=1,l=1)[0]
    secoundSel = cmds.ls(sl=1,l=1)[1]
    tergetJoint = [secoundSel]
    
    checkNode = cmds.listRelatives(secoundSel,parent=1,f=1)
    
    if checkNode != None:
        tergetJoint.append(checkNode[0])
    
    while checkNode != None:
        checkNode = cmds.listRelatives(checkNode,parent=1,f=1)
        if checkNode != None:
            tergetJoint.append(checkNode[0])
        if checkNode[0] == firstSel:
            break
    
    tergetJoint.reverse()
    return tergetJoint

#選択したジョイントと同じ形のジョイントを作る
def select2Joint(name="",cnst=False):
    sel = cmds.ls(sl=1,l=1)
    JH = returnSelectHierarchy()
    firstNode = ""
    endNode = ""
    j = ""
    
    cmds.select(cl=1)
    for work in JH:
        #名前の重複チェック
        name = nodeNameChecker2(name)
        
        if cmds.objectType(work) == "joint":
            jointOrient = cmds.getAttr(work+".jointOrient")[0]
            j = cmds.joint(n=name)
            
            #もし最初のノードの場合、作成した骨ノードを変数に格納(TOPノードを取得したい)
            if work == JH[0]:
                firstNode = j

            cmds.setAttr(j+".jointOrientX",jointOrient[0])
            cmds.setAttr(j+".jointOrientY",jointOrient[1])
            cmds.setAttr(j+".jointOrientZ",jointOrient[2])
            
            cmds.delete( cmds.pointConstraint(work,j,mo=0)  )
            cmds.delete( cmds.orientConstraint(work,j,mo=0) )
            cmds.select(j)
            if cnst:
                try:
                    cmds.pointConstraint(j,work,mo=0)
                except:
                    True
                try:
                    cmds.orientConstraint(j,work,mo=0)
                except:
                    True
                ##cmds.scaleConstraint(j,work,mo=0)
        else:
            continue
        #もし最後のノードの場合、骨を変数に格納(末端ノードを取得しておきたい)
        if work == JH[-1]:
            endNode = j
    cmds.select(firstNode,endNode)
    return [firstNode,endNode]

#選択したジョイント階層でカーブを作成する
def createJoint2Curve(degreeValue=2,span=1):
    pointList = []
    for work in returnSelectHierarchy():
        pointList.append( cmds.xform(work,q=1,t=1,ws=1) )
    curveNode = cmds.curve(p=pointList,degree=degreeValue,n=nodeNameChecker2("IK_SplineCurve"))
    cmds.rebuildCurve(curveNode,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=span,d=degreeValue,tol=0.01)
    cmds.smoothCurve(curveNode+'.cv[*]',s=100)
    cmds.select(curveNode)
    return cmds.ls(sl=1,l=1)

#createJoint2Curve(spanNum,degreeNum)

#コンストレインノードについている、Weightのアトリビュートを取得する関数
def returnConstraintWeightAttr(node=""):
    falseAttr = ['nodeState',
    'target.targetWeight',
    'offset',
    'offsetX',
    'offsetY',
    'offsetZ',
    "interpType",
    "target.targetOffsetTranslateX",
    "target.targetOffsetTranslateY",
    "target.targetOffsetTranslateZ",
    "target.targetOffsetRotateX",
    "target.targetOffsetRotateY",
    "target.targetOffsetRotateZ"]
    
    weightAttr = []
    
    if cmds.objExists(node):
        for work in cmds.listAttr(node,k=1):
            if not work in falseAttr:
                weightAttr.append(work)
        return weightAttr

# ------------------- 変数、配列の初期化 -------------------

#system関連
sel = [] #選択した２つのJointを格納しておく配列
selHierarchy = [] #選択した骨の間全てを格納しておく配列

IK_Joint = [] #IK骨の先端、末端を格納しておく配列
IK_Hierarchy = []#IK骨全てを格納しておく配列

FK_Joint = [] #FKジョイントの先端と末端を格納しておく配列
FK_Hierarchy = [] #FKジョイント全てを格納しておく配列

IK_CurveNode = "" #IKスプライン用のカーブを格納しておく変数

IKSpline_MiddlePositionNode = "" #中間地点を取得するロケータノード

IK_Node = "" #IKSplineノード

distNode = "" #distanceノードを格納しておく変数

# RIG関連

IKFK_root = "" #IKFKのルートノード 

IK_SplineCtrl_start = "" #IKSplineの最初のコントロールRIG ★まとめるやつ
IK_SplineCtrl_end = ""   #IKSplineの最後のコントロールRIG ★まとめるやつ

IKSpline_subCtrl_root = [] #subCtrlのルートノードを格納しておく配列 ★まとめるやつ
IKSpline_subCtrl = [] #subCtrlを格納しておく配列

IK_SplineCtrl_middle_root = [] #IKカーブを調整するRIGの親ノード ★まとめるやつ
IK_SplineCtrl_middle = [] #IKカーブを調整するRIG(先端と末端を除くカーブポイント)

startClusterNode = ""  #先端のカーブポイントを動かすクラスター
endClusterNode = "" #末端のカーブポイントを動かすクラスター

middleClusterNode = [] #中間のカーブポイントを動かすクラスター

distLoc = [] #distance用のロケータを配列に格納

distNode = "" #distanceノードを格納しておく変数
distShape = "" #distanceShapeノードを格納しておく変数

# ------------------- 実処理 -------------------

#選択したジョイントを取得
sel = cmds.ls(sl=1,l=1)
selHierarchy = returnSelectHierarchy()

#IKのJoint階層を作成 
cmds.select(sel)
IK_Joint = select2Joint(name="IK_Joint1",cnst=False)
cmds.setAttr( IK_Joint[0]+".visibility",0 )
IK_Hierarchy = returnSelectHierarchy()

#subコントローラーを作成
for work in IK_Hierarchy:
    #subCtrlのルートロケータを作成
    subCtrlRoot = cmds.createNode( "transform", n = nodeNameChecker2("IKSpline_subCtrl_root1") )
    cmds.delete( cmds.parentConstraint(work,subCtrlRoot) )
    #cmds.setAttr(subCtrlRoot+".visibility",0)
    
    #subCtrlを作成
    subCtrl = createCurveRIG("box",n = nodeNameChecker2("IKSpline_subCtrl1") )
    
    cmds.select( subCtrl )
    cmds.parent( subCtrl , subCtrlRoot )
    
    cmds.setAttr(subCtrl+".translateX",0)
    cmds.setAttr(subCtrl+".translateY",0)
    cmds.setAttr(subCtrl+".translateZ",0)
    cmds.setAttr(subCtrl+".rotateX",0)
    cmds.setAttr(subCtrl+".rotateY",0)
    cmds.setAttr(subCtrl+".rotateZ",0)
    
    IKSpline_subCtrl_root.append( subCtrlRoot )
    IKSpline_subCtrl.append( cmds.ls(sl=1)[0] )

print IKSpline_subCtrl

#IK関係のコンストレインを実行
for i in range( len(selHierarchy) ):
    print i
    #サブコントローラーから元の骨にペアレントコンストレイン
    try:
        cmds.pointConstraint(IKSpline_subCtrl[i],selHierarchy[i],mo=0)
    except:
        True
    try:
        cmds.orientConstraint(IKSpline_subCtrl[i],selHierarchy[i],mo=0)
    except:
        True
    #IK スプライン骨→サブコントローラー骨にペアレントコンストレイン
    cmds.parentConstraint(IK_Hierarchy[i],IKSpline_subCtrl_root[i],mo=0)

#FK用の骨を作成
cmds.select(sel)
FK_Joint = select2Joint(name="FK_Joint1",cnst=True)
cmds.setAttr( FK_Joint[0]+".visibility",0 )
FK_Hierarchy = returnSelectHierarchy()

#カーブを作成
IK_CurveNode = createJoint2Curve(degreeValue=degreeNum,span=spanNum)
cmds.setAttr( IK_CurveNode[0]+".template",1 )

#IK用のカーブにコントローラを追加
cmds.select(IK_CurveNode[0]+".cv[*]")
cv = cmds.ls(sl=1,l=1,fl=1)

#CV全てに対して処理
for work in cv:
    if work == cv[0]:
        #ロケータを作成
        RIG = createCurveRIG("box",n=nodeNameChecker2("IK_SplineCtrl_start") )
        IK_SplineCtrl_start = RIG
        
        #cluster作成
        cmds.select(work)
        startClusterNode = cmds.cluster(relative=0)[1]
        clstr = startClusterNode
        cmds.setAttr(clstr+".visibility",0)
        
        #locatorの位置をCVの位置へ
        cmds.delete( cmds.pointConstraint(clstr,RIG) )
        cmds.parent(clstr,RIG)
    
    elif work == cv[-1]:
        #ロケータを作成
        RIG = createCurveRIG("box",n=nodeNameChecker2("IK_SplineCtrl_end") )
        IK_SplineCtrl_end = RIG
        IK_SplineCtrl_end = RIG
        
        #cluster作成
        cmds.select(work)
        endClusterNode = cmds.cluster(relative=0)[1]
        clstr = endClusterNode
        cmds.setAttr(clstr+".visibility",0)
        
        #locatorの位置をCVの位置へ
        cmds.delete( cmds.pointConstraint(clstr,RIG) )
        cmds.parent(clstr,RIG)
    
    else:
        #ロケータを作成
        RIG = createCurveRIG("box",n=nodeNameChecker2("IK_SplineCtrl_middle1") )
        cmds.addAttr(RIG,ln="parent",at="enum",en="global:local",dv=1,min=0,max=1)
        cmds.setAttr(RIG+".parent",e=1,keyable=1)
        IK_SplineCtrl_middle.append(RIG)
        
        #cluster作成
        cmds.select(work)
        clstr = cmds.cluster(relative=0)[1]
        cmds.setAttr(clstr+".visibility",0)
        middleClusterNode.append(clstr)
        
        #locatorの位置をCVの位置へ
        cmds.delete( cmds.pointConstraint(clstr,RIG) )
        cmds.parent(clstr,RIG)

#中間地点取得用のノードを作成
IKSpline_MiddlePositionNode = cmds.createNode( "transform",n=nodeNameChecker2("middle_Position") )
cmds.setAttr( IKSpline_MiddlePositionNode+".visibility",0 )
cmds.pointConstraint(IK_SplineCtrl_start,IKSpline_MiddlePositionNode,mo=0)
cmds.aimConstraint(IK_SplineCtrl_start,IKSpline_MiddlePositionNode,mo=0,offset=[0,0,0],upVector=[0,1,0],worldUpType="vector",worldUpVector=[0,1,0])
cmds.pointConstraint(IK_SplineCtrl_end,IKSpline_MiddlePositionNode,mo=0)

#IK Curve編集用ノードの一つ上に、Parent切り替え用のノードを作成
IK_SplineCtrl_middle_root = []
for work in IK_SplineCtrl_middle:
    node = cmds.createNode( "transform" , n=nodeNameChecker2("IK_SplineCtrl_middle_root1") )
    cmds.delete( cmds.parentConstraint(work,node) )
    IK_SplineCtrl_middle_root.append(node)

for i in range(len(IK_SplineCtrl_middle)):
    #cmds.setAttr(IK_SplineCtrl_middle_root[i]+".visibility",0)
    #subCtrlノード(骨を個々に動かせるコントローラー)を、Parent用ロケータの子供にする
    cmds.parent(IK_SplineCtrl_middle[i],IK_SplineCtrl_middle_root[i])

i = 0
#中間地点ノードと、IKコントローラをコンスト
for work in IK_SplineCtrl_middle_root:
    cnst = cmds.parentConstraint(IKSpline_MiddlePositionNode,work,mo=1)[0]
    #weightを取得
    cnstWeightAttr = returnConstraintWeightAttr(cnst)
    cmds.connectAttr(IK_SplineCtrl_middle[i]+".parent" , cnst+"."+cnstWeightAttr[0])
    i += 1

#IK Splineを作成
cmds.select(IK_Joint,IK_CurveNode)
IK_Node = cmds.ikHandle(sol="ikSplineSolver",ccv=0,fj=0,c=IK_CurveNode[0])[0]
cmds.setAttr( IK_Node+".visibility",0 )
#cmds.setAttr( IK_Node+".dTwistControlEnable",1 )

#IKFKのルートノードを作成&各種アトリビュート追加
IKFK_root = cmds.createNode("transform", n=nodeNameChecker2("IKFK_root") )

cmds.addAttr(IKFK_root,ln="IK_Twist",at="double",dv=0)
cmds.setAttr(IKFK_root+".IK_Twist",e=1,keyable=1)

cmds.addAttr(IKFK_root,ln="IK_FK_Blend",at="double",dv=0,min=0,max=1)
cmds.setAttr(IKFK_root+".IK_FK_Blend",e=1,keyable=1)

cmds.addAttr(IKFK_root,ln="squash",at="bool",dv=1,min=0,max=1)
cmds.setAttr(IKFK_root+".squash",e=1,keyable=1)

cmds.addAttr(IKFK_root,ln="slide",at="double",dv=0)
cmds.setAttr(IKFK_root+".slide",e=1,keyable=1)

cmds.addAttr(IKFK_root,ln="subCtrl",at="bool",dv=0)
cmds.setAttr(IKFK_root+".subCtrl",e=1,keyable=1)

#Twistアトリビュートのコネクションを繋ぐ
cmds.connectAttr( ( IKFK_root+".IK_Twist" ) , IK_Node+".twist" )

#Blendアトリビュートのコネクションを繋ぐ
revNode = cmds.createNode("reverse")
cmds.connectAttr(IKFK_root+".IK_FK_Blend",revNode+".inputX")

#distance Nodeを作成
for work in [IK_SplineCtrl_start,IK_SplineCtrl_end]:
    data = cmds.spaceLocator( n=nodeNameChecker2("IKSpline_distanceLoc1") )[0]
    cmds.delete( cmds.parentConstraint(work,data) )
    distLoc.append( data )

cmds.select(distLoc)
cmds.setAttr(distLoc[0]+".visibility",0)
cmds.setAttr(distLoc[1]+".visibility",0)

cmds.parent(distLoc[0],IK_SplineCtrl_start)
cmds.parent(distLoc[1],IK_SplineCtrl_end)
cmds.select(distLoc)

distShape = cmds.distanceDimension()
distNode = cmds.listRelatives(distShape,p=1)[0]
distValue = cmds.getAttr(distShape+".distance")
divideNode = cmds.createNode("multiplyDivide")

cmds.setAttr( distNode+".visibility",0 )
cmds.setAttr( divideNode+".operation",2 )
cmds.connectAttr( distShape+".distance",divideNode+".input1X" )
cmds.setAttr( divideNode+".input2X",distValue )

#squashの切り替えの仕組みを作成
for work in IK_Hierarchy[0:-1]:
    squashNode = cmds.createNode("condition")
    cmds.connectAttr(IKFK_root+".squash",squashNode+".firstTerm")
    cmds.setAttr(squashNode+".secondTerm",1)
    cmds.connectAttr(divideNode+".outputX",squashNode+".colorIfTrueR")
    if jointDirection == "x":
        cmds.connectAttr(squashNode+".outColorR",work+".scaleX")
    if jointDirection == "y":
        cmds.connectAttr(squashNode+".outColorR",work+".scaleY")
    if jointDirection == "z":
        cmds.connectAttr(squashNode+".outColorR",work+".scaleZ")

cmds.connectAttr(divideNode+".outputX",IKSpline_MiddlePositionNode+".scaleX")
cmds.connectAttr(divideNode+".outputX",IKSpline_MiddlePositionNode+".scaleY")
cmds.connectAttr(divideNode+".outputX",IKSpline_MiddlePositionNode+".scaleZ")

#SubCtrlアトリビュート→subCtrl Visibilityへ接続
for work in IKSpline_subCtrl:
    cmds.connectAttr(IKFK_root+".subCtrl",work+".visibility")

#コンストノードと、ブレンド用ノードを接続
for work in selHierarchy:
    if cmds.objectType(work) == "joint":
        for cnstNode in cmds.listRelatives(work,c=1,type="constraint"):
            weightAttr = returnConstraintWeightAttr(node=cnstNode)
            
            #IK側に接続
            cmds.connectAttr(revNode+".outputX",cnstNode+"."+weightAttr[0])
            
            #FK側に接続
            cmds.connectAttr(IKFK_root+".IK_FK_Blend",cnstNode+"."+weightAttr[1])

#Scaleをブレンドする仕組みを構築
size = len(selHierarchy)
for i in range(size):
    #FKとIKの切り替え用
    blendNode = cmds.createNode("blendColors")
    
    """
    #SquashのOn、Off判断用ノード
    ifNode = cmds.createNode("condition")
    
    #Squash判断アトリビュートと接続
    cmds.connectAttr(IKFK_root+".squash",ifNode+".firstTerm")
    cmds.setAttr(ifNode+".secondTerm",1)
    
    #IK用骨と、FK用骨のスケールをそれぞれ接続
    cmds.connectAttr(IK_Hierarchy[i]+".scaleX",ifNode+".colorIfTrueR")
    cmds.connectAttr(FK_Hierarchy[i]+".scaleX",ifNode+".colorIfFalseR")
    cmds.connectAttr(ifNode+".outColorR",blendNode+".color1R")
    cmds.connectAttr(FK_Hierarchy[i]+".scaleX",blendNode+".color2R")
    """
    #indexが0じゃなければ、つまりIK_Hierarchyがトップノードじゃない場合、Slide用処理を走らせる
    if i != 0:
        #Slide用のノードを追加
        plusNode = cmds.createNode("plusMinusAverage")
        cmds.connectAttr(IKFK_root+".slide",plusNode+".input1D[0]")
        
        #blendColorXアトリビュートを、実際にスキニングされている骨のScaleXに接続
        if jointDirection == "x":
            cmds.setAttr( plusNode+".input1D[1]" , cmds.getAttr(IK_Hierarchy[i]+".tx") )
            cmds.connectAttr(plusNode+".output1D",IK_Hierarchy[i]+".tx")
        if jointDirection == "y":
            cmds.setAttr( plusNode+".input1D[1]" , cmds.getAttr(IK_Hierarchy[i]+".ty") )
            cmds.connectAttr(plusNode+".output1D",IK_Hierarchy[i]+".ty")
        if jointDirection == "z":
            cmds.setAttr( plusNode+".input1D[1]" , cmds.getAttr(IK_Hierarchy[i]+".tz") )
            cmds.connectAttr(plusNode+".output1D",IK_Hierarchy[i]+".tz")

#階層構造をまとめる&アトリビュートの整理
IK_Group = cmds.createNode("transform",n=nodeNameChecker2( "IK_Group" ))
cmds.parent( [IK_SplineCtrl_start,IK_SplineCtrl_end],  IK_Group)
cmds.parent( IK_SplineCtrl_middle_root,  IK_Group)
cmds.parent( IKSpline_subCtrl_root ,  IK_Group)
cmds.parent( IK_Group , IKFK_root)

systemGroup = cmds.createNode( "transform",n=nodeNameChecker2( "system" ) )
cmds.parent( [IK_Joint[0],FK_Joint[0],IK_CurveNode[0],IK_Node,IKSpline_MiddlePositionNode,distNode],systemGroup )

IKFK_RIG = cmds.createNode( "transform",n=nodeNameChecker2( "IKFK_RIG" ) )
cmds.parent( [systemGroup,IKFK_root], IKFK_RIG)

#コントローラのアトリビュートを0.0にする
cmds.select(IK_SplineCtrl_start,IK_SplineCtrl_end)
mel.eval("makeIdentity -apply true -t 1 -r 1 -s 0 -n 0 -pn 1;")

#IK MidCtrlのアトリビュートを整理
for work in IK_SplineCtrl_middle:
    try:
        lockAndHideAttr( work,["rx","ry","rz","sx","sy","sz","v"],cb=False )
    except:
        continue

#subCtrlのアトリビュートを整理
for work in IKSpline_subCtrl:
    lockAndHideAttr( work,["sx","sy","sz","v"],cb=False )


#階層下のカーブ以外全てのTRSFVのアトリビュートを全部ロック＆ハイド
cmds.select(IKFK_RIG,hi=1)
cmds.select( cmds.listRelatives( cmds.ls( type=["nurbsCurve"] ),p=1 ),d=1 )
for work in cmds.ls(sl=1):
    if cmds.objectType(work).find("Constraint") != -1 or cmds.objectType(work) == "joint" or work == IKFK_root:
        continue
    try:
        lockAndHideAttr( work,["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"],cb=False )
    except:
        continue
