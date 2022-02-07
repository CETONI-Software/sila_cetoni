from os.path import dirname, join

from sila2.framework import Feature

BatteryProviderFeature = Feature(open(join(dirname(__file__), "BatteryProvider.sila.xml")).read())
