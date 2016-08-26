translate1 = cmds.xform(cmds.ls(sl=1)[0],q=1,ws=1,t=1)
translate2 = cmds.xform(cmds.ls(sl=1)[1],q=1,ws=1,t=1)

tx = translate2[0]+(translate1[0]-translate2[0])/2
ty = translate2[1]+(translate1[1]-translate2[1])/2
tz = translate2[2]+(translate1[2]-translate2[2])/2

cmds.select(cl=1)
cmds.joint(p=[tx,ty,tz],radius=0.4)
