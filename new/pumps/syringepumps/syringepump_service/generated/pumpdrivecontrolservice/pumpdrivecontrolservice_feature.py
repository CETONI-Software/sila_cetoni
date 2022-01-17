from os.path import dirname, join

from sila2.framework import Feature

PumpDriveControlServiceFeature = Feature(open(join(dirname(__file__), "PumpDriveControlService.sila.xml")).read())
