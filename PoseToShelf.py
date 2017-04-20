import maya.cmds as cmds
import maya.mel as mel
def PoseToShelf(SelectList):
    AttrValue = 0
    AttrCmd = "scriptToShelf \"Pose\" \""
    for work in SelectList:
        for Attr in cmds.listAttr(work,k=1,u=1,se=1):
            AttrValue = cmds.getAttr(work+"."+Attr)
            if AttrValue == True:
                AttrValue = 1
            elif AttrValue == False:
                AttrValue = 0
            AttrCmd += "catch(`setAttr \\\""+work+"."+Attr+"\\\" "+str(AttrValue)+"`);\\r"
    AttrCmd += "\" \"1\";"
    mel.eval(AttrCmd)
PoseToShelf(cmds.ls(sl=1))
