from os.path import dirname, join

from sila2.framework import Feature

ForceMonitoringServiceFeature = Feature(open(join(dirname(__file__), "ForceMonitoringService.sila.xml")).read())
