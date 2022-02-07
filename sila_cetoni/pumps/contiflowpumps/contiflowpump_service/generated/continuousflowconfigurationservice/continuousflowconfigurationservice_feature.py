from os.path import dirname, join

from sila2.framework import Feature

ContinuousFlowConfigurationServiceFeature = Feature(
    open(join(dirname(__file__), "ContinuousFlowConfigurationService.sila.xml")).read()
)
