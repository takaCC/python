## -*- coding: utf-8 -*-
import maya.cmds as mc
import sys

#関数の生成

def FileBrowser_Mod():
    #ファイルブラウザ関数

    ## -*- coding: utf-8 -*-
    import maya.cmds as mc

    singleFilter = "All Files (*.*)"
    return cmds.fileDialog2(fileFilter=singleFilter, dialogStyle=2)


def exportAnimationMod(exportPath,NameSpace,ExportType,ExportNode,catchToggle):
    #アニメーションをエキスポートする関数
    #1：書き出し先
    #2:ネームスペースの指定(指定しない場合、書き出しファイルは編集されない)
    #3:エキスポートタイプ(Select、All、Hierarchy)
    #4:書き出すノード
    #5:catchコマンドは発行するか

    ## -*- coding: utf-8 -*-
    import maya.cmds as mc
    import sys

    #変数の初期化
    replaceTxt = []
    
    #アニメーションのエクスポート。シーンに存在する全てのアニメーションカーブを書き出す
    if ExportType == "All":
        #アニメーションのエクスポート
        mc.select(cl=1)
        mc.file(exportPath,f=1,typ="mayaAscii",ean=1)

    #アニメーションのエクスポート。選択したノードからアニメーションカーブを書き出す
    elif ExportType == "Select":
        #アニメーションのエクスポート
        mc.select(ExportNode)
        mc.file(exportPath,f=1,typ="mayaAscii",eas=1)
        mc.select(cl=1)

    #アニメーションのエクスポート。選択したノードを含む、階層化のアニメーションを書き出す
    elif ExportType == "Hierarchy":
        mc.select(ExportNode)
        mc.select(hierarchy=1,add=1)
        mc.file(exportPath,f=1,typ="mayaAscii",eas=1)
        mc.select(cl=1)

    #maファイルの中身を変数に格納
    maFile = open(exportPath,"r")
    txt = maFile.readlines()
    maFile.close

    #NameSpaceが指定されている場合
    if not len(NameSpace) == 0:
        #connectAttrを編集
        for work in txt:
            #行の中にconnectAttrの文字列がある場合、処理を実行
            if not work.find("connectAttr") == -1:
                #connectAttrを置換
                replaceTxt.append(work.split("\"")[0]+"-f \""+work.split("\"")[1]+"\""+work.split("\"")[2]+"(\":\"+$exANM_NameSpace+\""+work.split("\"")[3].split(":")[-1]+"\");\r\n")
            else:
                #connectAttr以外はそのまま変数に代入する
                replaceTxt.append(work)

        if str(catchToggle) == "True":
            replaceTxt.append("\r\n"+"//ConnectAttrを強制実行するコマンドを以下に発行する。シーンに入れ込んでうまくいかなかったら、以下を活用するのもあり。\r\n")
            #catchを使ったconnectAttrも生成する
            for work in txt:
                #行の中にconnectAttrの文字列がある場合、処理を実行
                if not work.find("connectAttr") == -1:
                    #connectAttrを置換
                    replaceTxt.append("catch(`"+work.split("\"")[0]+"-f \""+work.split("\"")[1]+"\""+work.split("\"")[2]+"(\":\"+$exANM_NameSpace+\""+work.split("\"")[3].split(":")[-1]+"\"`);\r\n")

    #NameSpaceが指定されていない場合
    else:
        #connectAttrを編集
        for work in txt:
            #行の中にconnectAttrの文字列がある場合、処理を実行
            if not work.find("connectAttr") == -1:
                #connectAttrを置換
                replaceTxt.append(work.split("\"")[0]+"-f \""+work.split("\"")[1]+"\""+work.split("\"")[2]+"\":"+work.split("\"")[3]+"\";\r\n")
            else:
                #connectAttr以外はそのまま変数に代入する
                replaceTxt.append(work)

        if str(catchToggle) == "True":
            replaceTxt.append("\r\n"+"//ConnectAttrを強制実行するコマンドを以下に発行する。シーンに入れ込んでうまくいかなかったら、以下を活用するのもあり。\r\n")
            #catchを使ったconnectAttrも生成する
            for work in txt:
                #行の中にconnectAttrの文字列がある場合、処理を実行
                if not work.find("connectAttr") == -1:
                    #connectAttrを置換
                    replaceTxt.append("catch(`"+work.split("\"")[0]+"-f \""+work.split("\"")[1]+"\""+work.split("\"")[2]+"\":"+work.split("\"")[3].split(":")[-1]+"\"`);\r\n")

    VarTxt = "global string $exANM_NameSpace = "+"\""+NameSpace+":\";\r\n\r\n"
    
    maFile = open(exportPath,"w")
    maFile.write(VarTxt)
    
    #connectAttrを編集したTXTをファイルに書き込み
    for work in replaceTxt:
        maFile.write(work)
    maFile.close


def ExportButton_UICmd():
    #Export Animation Toolの,Exportボタンで実行するための関数。
    #各種パラメータを読み取り、exportAnimationMod関数へ引き渡す

    #書き出し先の取得
    if len(mc.textField("ExportAnimTool_filePath",q=1,tx=1)) > 0:
        exportPath = mc.textField("ExportAnimTool_filePath",q=1,tx=1)
    else:
        mc.error("Please Output Path Setting.")

    #namespaceの取得
    if mc.radioButton("ExportAnimTool_ExportTypeSelect",q=1,sl=1) == 1 or mc.radioButton("ExportAnimTool_ExportTypeHierarchy",q=1,sl=1) == 1:
        NameSpace = str(mc.textField("ExportAnimTool_NameSpaceString",q=1,tx=1))
    elif mc.radioButton("ExportAnimTool_ExportTypeAll",q=1,sl=1) == 1:
        NameSpace = ""

    #書き出すタイプの取得
    if mc.radioButton("ExportAnimTool_ExportTypeAll",q=1,sl=1) == 1:
        ExportType = "All"
    elif mc.radioButton("ExportAnimTool_ExportTypeSelect",q=1,sl=1) == 1:
        if len(mc.ls(sl=1)) == 0:
            mc.error("Please Select Node.")
        else:
            ExportType = "Select"
    elif mc.radioButton("ExportAnimTool_ExportTypeHierarchy",q=1,sl=1) == 1:
        if len(mc.ls(sl=1)) == 0:
            mc.error("Please Select Node.")
        else:
            ExportType = "Hierarchy"

    #書き出すアニメーションカーブが付いているノードを取得
    ExportNode = mc.ls(sl=1,l=1)

    #catchコマンドを含めるかの取得
    if mc.radioButton("ExportAnimTool_CatchToggelTrue",q=1,sl=1) == 1:
        catchToggle = "True"
    else:
        catchToggle = ""
    
    #Hierarchyモードでノードを２つ以上選択しており、なおかつNameSpaceが設定されている場合
    if ExportType == "Hierarchy" and len(NameSpace) > 0:
        check = mc.confirmDialog(title="警告メッセージ",message="Hierarchyモードでなおかつ、ノードが２つ以上選択されています。\r\nこのままでは書きだされたアニメーションノードのNameSpace全てが指定したNameSpaceになります。\r\n(書きだされたアニメーションがうまく読み込めない可能性があります)\r\nよろしいですか？",button=["Yes","No"],defaultButton="Yes",cancelButton="No",dismissString="No")
        if check == "Yes":
            exportAnimationMod(exportPath,NameSpace,ExportType,ExportNode,catchToggle)
            if mc.checkBox("ExportAnimTool_notice",q=1,v=1) == 1:
                mc.confirmDialog(title="Notice",message="書き出しが終了しました!",button="Yes")
        else:
            mc.confirmDialog(message="処理を中断しました!",button="Yes")
    else:
        exportAnimationMod(exportPath,NameSpace,ExportType,ExportNode,catchToggle)
        if mc.checkBox("ExportAnimTool_notice",q=1,v=1) == 1:
            mc.confirmDialog(title="Notice",message="書き出しが終了しました!",button="Yes")


#UIの作成＆編集
#UIの作成
if mc.window("ExportAnimationTool_Window",ex=1) == 1:
    mc.deleteUI("ExportAnimationTool_Window")
mc.showWindow(mc.loadUI(f="path/ExportAnimUI.ui"))

#UIの編集
#outputボタンにコマンドを割り当てる
mc.button("ExportAnimTool_filePathButton",e=1,c="mc.textField(\"ExportAnimTool_filePath\",e=1,tx=FileBrowser_Mod()[0])")

#Exportボタンにコマンドを割り当てる
mc.button("ExportAnimTool_Run",e=1,c="ExportButton_UICmd()")
