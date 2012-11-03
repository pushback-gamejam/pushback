#!/usr/bin/env python

from src.gameoutput import GameOutput
from panda3d.core import Vec3
from direct.showbase.DirectObject import DirectObject


class TaskContainer(DirectObject):
    """"""
    def __init__(self):
        self.i = 0.0
        base.taskMgr.add(self.dummyMove, "sdaf")
        base.taskMgr.add(self.charge)

    def dummyMove(self, arg):
        self.i += 0.05
        go.setPlayerPosition("my", Vec3(0, 0, 0), Vec3(self.i * 10, 0, 0))
        return arg.cont


go = GameOutput("resources/level/testlevel_new.x")

pl = list()
pl.append(["my", Vec3(0,0,0)])
pl.append(["other", Vec3(5,0,0)])
pl.append(["other2", Vec3(-5,0,0)])
go.start("my", pl)

d = TaskContainer()

go.run()
