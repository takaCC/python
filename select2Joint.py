sel = cmds.ls(sl=1,l=1,fl=1)
cmds.select(cl=1)

for work in sel:
    if not cmds.objectType(work) == "mesh":
        cmds.select(work)
        name = cmds.ls(sl=1)[0].split("|")[-1]
        print name
        cmds.select(cl=1)
        cmds.delete(cmds.parentConstraint(work,cmds.joint(n=name+"_joint",radius=0.4)))
        cmds.select(cl=1)
    
    else:
        name = work.split(".vtx")[0].split("|")[-1]
        cmds.select(work)
        clstr = cmds.cluster()
        cmds.select(cl=1)
        j = cmds.joint(n=name+"_joint",radius=0.4)
        cmds.select(cl=1)
        
        cmds.delete(cmds.parentConstraint(clstr,j))
        cmds.delete(clstr)


