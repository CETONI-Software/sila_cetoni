from os.path import dirname, join

from sila2.framework import Feature

ContinuousFlowInitializationControllerFeature = Feature(
    open(join(dirname(__file__), "ContinuousFlowInitializationController.sila.xml")).read()
)
