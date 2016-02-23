import re
import os
import time

TargetDirectory = ""

#チェックしたディレクトリ一覧を入れておくリスト
globalSaveDir = []

#再帰を行うための関数
def returnDir_Loop(target):
    globalSaveDir.append(target)
    returnDir(target)

#指定したディレクトリ下にあるディレクトリ一覧を返す関数
def returnDir(targetDir):
    #チェック用のリストを作成
    checkList = []
    
    #指定ディレクトリが存在しない or ディレクトリじゃない場合 処理を終了
    if not os.path.exists(targetDir) or os.path.isdir(targetDir) == False:
        return 0
    
    #末尾が/じゃない場合は足す
    if targetDir[-1] != "/":
        targetDir += "/"
    
    #ターゲットディレクトリ内のディレクトリ一覧をチェックリストに入れる
    [returnDir_Loop(targetDir+work) for work in os.listdir(targetDir)]
    
    """
    #チェックリストが空でなければ
    if len(checkList):
        #ディレクトリ一覧を保存
        globalSaveDir.append(checkList)
        #[globalSaveDir.append(work) for work in checkList]
        #チェックしたディレクトリ一覧をループして、また自身の関数を呼び出す
        [returnDir(targetDir=work) for work in checkList]
    """
