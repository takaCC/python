## -*- coding: utf-8 -*-
import maya.cmds as cmds
import random

#選択したキーフレーム間でキーをランダムに打つ関数
def randomKeyFrame(value=0.01,cycle=1):
    cycle = int(cycle)
    if cmds.keyframe(q=1,n=1,sl=1) != None:
        for curveName in cmds.keyframe(q=1,n=1,sl=1):
            #カーブの最小、最大値を取得
            minFrame = int(min(cmds.keyframe(curveName,q=1,sl=1)))
            maxFrame = int(max(cmds.keyframe(curveName,q=1,sl=1)))
            #maxフレームに達するまで、キーをインサート
            for frame in range(minFrame,maxFrame,cycle):
                cmds.setKeyframe(curveName,i=1,t=frame)
            #maxフレームに達するまで、キーの値をランダム化
            for frame in range(minFrame,maxFrame,cycle):
            	if frame != minFrame:
                    targetValue = cmds.keyframe(curveName,q=1,vc=1,t=(frame,frame))[0]
                    rand = targetValue+random.uniform(value*-1,value)
                    cmds.keyframe(curveName,e=1,vc=rand,t=(frame,frame))

#キーフレームをスケールする関数
def scaleKeyFrame(mode,pivotValue,scaleValue):
    
    #カーブを配列で返す関数
    def returnCurves():
        indexArray = []
        curves = cmds.keyframe(q=1,sl=1,n=1)
        for work in curves:
            indexArray.append(cmds.keyframe(work,q=1,sl=1,iv=1))
        cmds.selectKey(cl=1)
        i = 0
        while i < len(indexArray):
            for indexValue in indexArray[i]:
                cmds.selectKey(curves[i],add=1,index=(indexValue,indexValue))
            i += 1
        return [curves,indexArray]
    
    #引数を渡して、キーを選択する関数。第一引数にカーブ名を、第二引数にインデックスの配列を渡す。
    def selectAddAnimCurve(curveName,indexData):
        s = "cmds.selectKey(\""+curveName+"\",add=1,index=[("
        for indexValue in indexData:
            s += str(indexValue)+","+str(indexValue)+"),("
        s += ")])"
        s = s.replace(",()","")
        eval(s)
    
    frame = cmds.currentTime(q=1)
    if cmds.keyframe(q=1,sl=1,n=1) != None:
        curveArray = returnCurves()[0]
        indexArray = returnCurves()[1]
        #モードをframeにした場合
        if mode == 1:
            #cmds.currentTime(pivotValue,u=1)
            i = 0
            while i < len(curveArray):
                cmds.selectKey(cl=1)
                #アニメーションカーブの選択
                selectAddAnimCurve(curveArray[i],indexArray[i])
                pivot = cmds.getAttr(curveArray[i]+".output",t=pivotValue)
                cmds.scaleKey(vs=scaleValue,vp=pivot)
                i += 1
            #cmds.currentTime(frame,u=1)
        #モードを%にした場合
        elif mode == 2:
            i = 0
            while i < len(indexArray):
                cmds.selectKey(cl=1)
                #アニメーションカーブの選択
                selectAddAnimCurve(curveArray[i],indexArray[i])
                #カーブの最小値と最大値から値の幅を取る
                dist = max(cmds.keyframe(q=1,sl=1,vc=1))-min(cmds.keyframe(q=1,sl=1,vc=1))
                #値の幅に割合を掛けたものを、最小値に足す。この数値がscalePivotになる。また、値は0.01倍する(100で100%にするため)
                pivot = min(cmds.keyframe(q=1,sl=1,vc=1))+dist*pivotValue*0.01
                cmds.scaleKey(vs=scaleValue,vp=pivot)
                i += 1
        elif mode == 3:
            i = 0
            while i < len(indexArray):
                cmds.selectKey(cl=1)
                #アニメーションカーブの選択
                selectAddAnimCurve(curveArray[i],indexArray[i])
                #スケールを実行
                cmds.scaleKey(vs=scaleValue,vp=pivotValue)
                i += 1
        i = 0
        while i < len(indexArray):
            selectAddAnimCurve(curveArray[i],indexArray[i])
            i += 1

#選択したキーに、選択した間隔でキーを打つ関数
def insertKeyframe(intervalValue):
    for work in cmds.keyframe(q=1,n=1):
        if cmds.keyframe(work,q=1,vc=1,sl=1) == None:
            cmds.selectKey(work)
        #animカーブの最初のフレームを取得
        startFrame = cmds.keyframe(work,q=1,tc=1,sl=1)[0]
        endFrame = cmds.keyframe(work,q=1,tc=1,sl=1)[-1]
        minValue = min(cmds.keyframe(work,q=1,vc=1,sl=1))
        maxValue = max(cmds.keyframe(work,q=1,vc=1,sl=1))
        
        #最初にキーを打つフレームを変数に代入
        index = startFrame+intervalValue
        
        #範囲内に指定フレーム間隔でキーを打つ
        while index < endFrame:
            #指定間隔でキーを打つ
            cmds.setKeyframe(work,t=[index,index],insert=1)
            index += intervalValue

#キーフレームをオフセットする関数
def offsetKeyFrame(offset,mode="ShiftValue"):
    if mode == "ShiftValue":
        #選択しているキーがあれば
        if cmds.keyframe(q=1,n=1,sl=1) != None:
            index = 0
            for work in cmds.keyframe(q=1,n=1):
                if index != 0:
                    cmds.keyframe(e=1,r=1,tc=offset)
                    cmds.selectKey(work,rm=1)
                else:
                	cmds.selectKey(work,rm=1)
                index += 1
                #offset += offset
    
    elif mode == "frontMove":
        cmds.keyframe(e=1,r=1,tc=offset)
    elif mode == "backMove":
        cmds.keyframe(e=1,r=1,tc=offset*-1)
    elif mode == "atFrame":
        offset = offset-min(cmds.keyframe(q=1))
        cmds.keyframe(e=1,r=1,tc=offset)

#キーフレーム削除関数
def removeKeyframe(start=0,end=0,auto=False,insertKey=False):
    #timeSliderの削除モードの場合
    if auto:
        minFrame = cmds.playbackOptions(q=1,min=1)
        maxFrame = cmds.playbackOptions(q=1,max=1)
        
        cmds.selectKey()
        if insertKey:
            cmds.setKeyframe(i=1,t=minFrame)
            cmds.setKeyframe(i=1,t=maxFrame)
        
        for work in cmds.keyframe(q=1,n=1):
            cmds.selectKey(work,rm=1,k=1,time=(cmds.playbackOptions(q=1,min=1),cmds.playbackOptions(q=1,max=1)))
        if cmds.keyframe(q=1,sl=1) != None:
            cmds.cutKey()
    #何か選択されていれば
    if cmds.ls(sl=1) != []:
        #スタートとエンドの差が0.0じゃなければ
        if end-start != 0:
            cmds.cutKey(time=(start,end))
    else:
        cmds.error("please select node")
        
#UI作成
UIPath = "X:/p141/prj141dnt/user/auth_motion/SCRIPTS/keyAdjust/UI/keyAdjustUI.ui"
if cmds.window("keyAdjustUI",q=1,ex=1):
    cmds.deleteUI("keyAdjustUI")

UI = cmds.loadUI(f=UIPath)
cmds.window("keyAdjustUI",e=1,te=150)
cmds.showWindow(UI)

#キーずらし機能を付加
cmds.button("keyAdjustUI_keyShifter_run",e=1,c='offsetKeyFrame(float(cmds.textField("keyAdjustUI_keyShifter_value",q=1,tx=1)),mode="ShiftValue")')

#キースケール機能を付加
def Return_KeyScaleMode():
    mode = 1
    if cmds.radioButton("keyAdjustUI_keyScale_pivotFrame",q=1,sl=1):
        mode = 1
    elif cmds.radioButton("keyAdjustUI_keyScale_pivotRatio",q=1,sl=1):
        mode = 2
    elif cmds.radioButton("keyAdjustUI_keyScale_pivotAmount",q=1,sl=1):
        mode = 3
    return mode

cmds.button("keyAdjustUI_keyScale_run",e=1,c='scaleKeyFrame(Return_KeyScaleMode(),float(cmds.textField("keyAdjustUI_keyScale_pivotValue",q=1,tx=1)),float(cmds.textField("keyAdjustUI_keyScale_scaleValue",q=1,tx=1)))')

#キー削除機能を付加
cmds.button("keyAdjustUI_keyDelete_run",e=1,c='removeKeyframe(start=float(cmds.textField("keyAdjustUI_keyDelete_frameStart",q=1,tx=1)),end=float(cmds.textField("keyAdjustUI_keyDelete_frameEnd",q=1,tx=1)),auto=cmds.radioButton("keyAdjustUI_keyDelete_modeTimeSlider",q=1,sl=1),insertKey=cmds.checkBox("keyAdjustUI_keyDelete_setInsertKey",q=1,v=1))')

#キー移動機能を付加
def return_KeyMoveMode():
    mode = 1
    if cmds.radioButton("keyAdjustUI_keyMove_modeAgo",q=1,sl=1):
        mode = "frontMove"
    elif cmds.radioButton("keyAdjustUI_keyMove_modeBehind",q=1,sl=1):
        mode = "backMove"
    elif cmds.radioButton("keyAdjustUI_keyMove_modeAtFrame",q=1,sl=1):
        mode = "atFrame"
    return mode

cmds.button("keyAdjustUI_keyMove_run",e=1,c='offsetKeyFrame(float(cmds.textField("keyAdjustUI_keyMove_frameValue",q=1,tx=1)),mode=return_KeyMoveMode())')

#ランダムにキーを打つ機能を付加
cmds.button("keyAdjustUI_randomKey_run",e=1,c='randomKeyFrame(value=float(cmds.textField("keyAdjustUI_randomKey_Value",q=1,tx=1)),cycle=float(cmds.textField("keyAdjustUI_randomKey_cycle",q=1,tx=1)))')

#menuItemを編集
cmds.menuItem("keyAdjust_gotoWiki",ec=1,e=1,c="os.system('X:/p141/prj141dnt/user/auth_motion/SCRIPTS/keyAdjust/ref/keyAdjust_wiki.url')")
cmds.menuItem("keyAdjust_watchMovie",ec=1,e=1,c="os.system('X:/p141/prj141dnt/user/auth_motion/SCRIPTS/keyAdjust/ref/keyAdjust_tutorial.wmv')")





<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>keyAdjustUI</class>
 <widget class="QMainWindow" name="keyAdjustUI">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>382</width>
    <height>404</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>keyAdjustUI</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout">
    <item row="0" column="1">
     <widget class="QToolBox" name="toolBox">
      <property name="enabled">
       <bool>true</bool>
      </property>
      <property name="currentIndex">
       <number>0</number>
      </property>
      <widget class="QWidget" name="page_2">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>364</width>
         <height>221</height>
        </rect>
       </property>
       <attribute name="label">
        <string>ランダムにキーを打つ</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_2">
        <item row="0" column="0">
         <widget class="QLabel" name="label_15">
          <property name="text">
           <string>Cycle</string>
          </property>
         </widget>
        </item>
        <item row="0" column="1">
         <widget class="QLineEdit" name="keyAdjustUI_randomKey_cycle">
          <property name="text">
           <string>3</string>
          </property>
          <property name="alignment">
           <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
          </property>
         </widget>
        </item>
        <item row="0" column="2">
         <widget class="QLabel" name="label_16">
          <property name="text">
           <string>Value</string>
          </property>
         </widget>
        </item>
        <item row="0" column="3">
         <widget class="QLineEdit" name="keyAdjustUI_randomKey_Value">
          <property name="text">
           <string>0.1</string>
          </property>
          <property name="alignment">
           <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
          </property>
         </widget>
        </item>
        <item row="1" column="0" colspan="4">
         <widget class="QPushButton" name="keyAdjustUI_randomKey_run">
          <property name="text">
           <string>Run</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="page_3">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>258</width>
         <height>90</height>
        </rect>
       </property>
       <attribute name="label">
        <string>キーフレームの移動</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_4">
        <item row="0" column="0">
         <widget class="QLabel" name="label_7">
          <property name="text">
           <string>Mode</string>
          </property>
         </widget>
        </item>
        <item row="0" column="1">
         <widget class="QRadioButton" name="keyAdjustUI_keyMove_modeAgo">
          <property name="text">
           <string>前に</string>
          </property>
          <property name="checked">
           <bool>true</bool>
          </property>
         </widget>
        </item>
        <item row="0" column="2">
         <widget class="QRadioButton" name="keyAdjustUI_keyMove_modeBehind">
          <property name="text">
           <string>後ろに</string>
          </property>
         </widget>
        </item>
        <item row="0" column="3">
         <widget class="QRadioButton" name="keyAdjustUI_keyMove_modeAtFrame">
          <property name="text">
           <string>指定フレームに</string>
          </property>
         </widget>
        </item>
        <item row="1" column="0">
         <widget class="QLabel" name="label_9">
          <property name="text">
           <string>Frame</string>
          </property>
         </widget>
        </item>
        <item row="1" column="1" colspan="3">
         <widget class="QLineEdit" name="keyAdjustUI_keyMove_frameValue">
          <property name="text">
           <string>0.0</string>
          </property>
          <property name="alignment">
           <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
          </property>
         </widget>
        </item>
        <item row="2" column="0" colspan="4">
         <widget class="QPushButton" name="keyAdjustUI_keyMove_run">
          <property name="text">
           <string>Run</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="page_4">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>96</width>
         <height>67</height>
        </rect>
       </property>
       <attribute name="label">
        <string>キーフレームのずらし</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_8">
        <item row="0" column="0">
         <widget class="QLabel" name="label_8">
          <property name="text">
           <string>Value</string>
          </property>
         </widget>
        </item>
        <item row="0" column="1">
         <widget class="QLineEdit" name="keyAdjustUI_keyShifter_value">
          <property name="text">
           <string>0.0</string>
          </property>
          <property name="alignment">
           <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
          </property>
         </widget>
        </item>
        <item row="1" column="0" colspan="2">
         <widget class="QPushButton" name="keyAdjustUI_keyShifter_run">
          <property name="text">
           <string>Run</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="page_5">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>345</width>
         <height>118</height>
        </rect>
       </property>
       <attribute name="label">
        <string>キーフレームの値をスケール</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_10">
        <item row="1" column="1">
         <widget class="QLineEdit" name="keyAdjustUI_keyScale_pivotValue">
          <property name="text">
           <string>0.0</string>
          </property>
          <property name="alignment">
           <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
          </property>
         </widget>
        </item>
        <item row="2" column="0">
         <widget class="QLabel" name="label_11">
          <property name="text">
           <string>スケール倍率</string>
          </property>
         </widget>
        </item>
        <item row="2" column="1">
         <widget class="QLineEdit" name="keyAdjustUI_keyScale_scaleValue">
          <property name="text">
           <string>1.0</string>
          </property>
          <property name="alignment">
           <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
          </property>
         </widget>
        </item>
        <item row="0" column="0">
         <widget class="QLabel" name="label_10">
          <property name="text">
           <string>スケールピボット</string>
          </property>
         </widget>
        </item>
        <item row="1" column="0">
         <widget class="QLabel" name="label_5">
          <property name="text">
           <string>ピボット値</string>
          </property>
         </widget>
        </item>
        <item row="0" column="1">
         <layout class="QHBoxLayout" name="horizontalLayout">
          <item>
           <widget class="QRadioButton" name="keyAdjustUI_keyScale_pivotFrame">
            <property name="text">
             <string>指定Frame</string>
            </property>
            <property name="checked">
             <bool>true</bool>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QRadioButton" name="keyAdjustUI_keyScale_pivotRatio">
            <property name="text">
             <string>割合値(%指定)</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QRadioButton" name="keyAdjustUI_keyScale_pivotAmount">
            <property name="text">
             <string>指定値</string>
            </property>
           </widget>
          </item>
         </layout>
        </item>
        <item row="3" column="0" colspan="2">
         <widget class="QPushButton" name="keyAdjustUI_keyScale_run">
          <property name="text">
           <string>Run</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="page_6">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>343</width>
         <height>124</height>
        </rect>
       </property>
       <attribute name="label">
        <string>キーフレームの削除</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_5">
        <item row="0" column="0">
         <layout class="QGridLayout" name="gridLayout_13">
          <item row="3" column="1">
           <widget class="QLabel" name="label">
            <property name="text">
             <string>start</string>
            </property>
           </widget>
          </item>
          <item row="3" column="2">
           <widget class="QLineEdit" name="keyAdjustUI_keyDelete_frameStart">
            <property name="enabled">
             <bool>false</bool>
            </property>
            <property name="text">
             <string>0.0</string>
            </property>
            <property name="alignment">
             <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
            </property>
           </widget>
          </item>
          <item row="3" column="0">
           <widget class="QLabel" name="label_4">
            <property name="text">
             <string>Frame</string>
            </property>
           </widget>
          </item>
          <item row="0" column="0">
           <widget class="QLabel" name="label_3">
            <property name="text">
             <string>Mode</string>
            </property>
           </widget>
          </item>
          <item row="3" column="3">
           <widget class="QLabel" name="label_2">
            <property name="text">
             <string>end</string>
            </property>
           </widget>
          </item>
          <item row="2" column="0" colspan="5">
           <widget class="Line" name="line">
            <property name="orientation">
             <enum>Qt::Horizontal</enum>
            </property>
           </widget>
          </item>
          <item row="3" column="4">
           <widget class="QLineEdit" name="keyAdjustUI_keyDelete_frameEnd">
            <property name="enabled">
             <bool>false</bool>
            </property>
            <property name="text">
             <string>0.0</string>
            </property>
            <property name="alignment">
             <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
            </property>
           </widget>
          </item>
          <item row="0" column="4">
           <widget class="QRadioButton" name="keyAdjustUI_keyDelete_modeFrame">
            <property name="text">
             <string>指定フレーム削除</string>
            </property>
           </widget>
          </item>
          <item row="0" column="2">
           <widget class="QRadioButton" name="keyAdjustUI_keyDelete_modeTimeSlider">
            <property name="text">
             <string>タイムスライダー残す</string>
            </property>
            <property name="checked">
             <bool>true</bool>
            </property>
           </widget>
          </item>
          <item row="1" column="2">
           <widget class="QCheckBox" name="keyAdjustUI_keyDelete_setInsertKey">
            <property name="text">
             <string>抑えのキーを打つ</string>
            </property>
           </widget>
          </item>
         </layout>
        </item>
        <item row="1" column="0">
         <widget class="QPushButton" name="keyAdjustUI_keyDelete_run">
          <property name="text">
           <string>Run</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>382</width>
     <height>17</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuHelp">
    <property name="title">
     <string>help</string>
    </property>
    <addaction name="keyAdjust_gotoWiki"/>
    <addaction name="keyAdjust_watchMovie"/>
   </widget>
   <addaction name="menuHelp"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <action name="keyAdjust_gotoWiki">
   <property name="text">
    <string>goto wiki</string>
   </property>
  </action>
  <action name="keyAdjust_watchMovie">
   <property name="text">
    <string>watch movie</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>keyAdjustUI_keyDelete_modeTimeSlider</sender>
   <signal>clicked(bool)</signal>
   <receiver>keyAdjustUI_keyDelete_setInsertKey</receiver>
   <slot>setEnabled(bool)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>157</x>
     <y>208</y>
    </hint>
    <hint type="destinationlabel">
     <x>152</x>
     <y>255</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>keyAdjustUI_keyDelete_modeTimeSlider</sender>
   <signal>clicked(bool)</signal>
   <receiver>keyAdjustUI_keyDelete_frameStart</receiver>
   <slot>setDisabled(bool)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>184</x>
     <y>208</y>
    </hint>
    <hint type="destinationlabel">
     <x>136</x>
     <y>313</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>keyAdjustUI_keyDelete_modeTimeSlider</sender>
   <signal>clicked(bool)</signal>
   <receiver>keyAdjustUI_keyDelete_frameEnd</receiver>
   <slot>setDisabled(bool)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>187</x>
     <y>215</y>
    </hint>
    <hint type="destinationlabel">
     <x>250</x>
     <y>306</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>keyAdjustUI_keyDelete_modeFrame</sender>
   <signal>clicked(bool)</signal>
   <receiver>keyAdjustUI_keyDelete_setInsertKey</receiver>
   <slot>setDisabled(bool)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>271</x>
     <y>209</y>
    </hint>
    <hint type="destinationlabel">
     <x>202</x>
     <y>248</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>keyAdjustUI_keyDelete_modeFrame</sender>
   <signal>clicked(bool)</signal>
   <receiver>keyAdjustUI_keyDelete_frameEnd</receiver>
   <slot>setEnabled(bool)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>307</x>
     <y>214</y>
    </hint>
    <hint type="destinationlabel">
     <x>298</x>
     <y>311</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>keyAdjustUI_keyDelete_modeFrame</sender>
   <signal>clicked(bool)</signal>
   <receiver>keyAdjustUI_keyDelete_frameStart</receiver>
   <slot>setEnabled(bool)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>334</x>
     <y>213</y>
    </hint>
    <hint type="destinationlabel">
     <x>201</x>
     <y>305</y>
    </hint>
   </hints>
  </connection>
 </connections>
</ui>
