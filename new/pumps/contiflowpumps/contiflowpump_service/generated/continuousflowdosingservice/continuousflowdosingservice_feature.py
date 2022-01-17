from os.path import dirname, join

from sila2.framework import Feature

ContinuousFlowDosingServiceFeature = Feature(
    open(join(dirname(__file__), "ContinuousFlowDosingService.sila.xml")).read()
)
