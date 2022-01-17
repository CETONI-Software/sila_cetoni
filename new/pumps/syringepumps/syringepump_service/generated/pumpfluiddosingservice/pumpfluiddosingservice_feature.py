from os.path import dirname, join

from sila2.framework import Feature

PumpFluidDosingServiceFeature = Feature(open(join(dirname(__file__), "PumpFluidDosingService.sila.xml")).read())
