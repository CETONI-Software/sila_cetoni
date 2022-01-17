from os.path import dirname, join

from sila2.framework import Feature

ControlLoopServiceFeature = Feature(open(join(dirname(__file__), "ControlLoopService.sila.xml")).read())
