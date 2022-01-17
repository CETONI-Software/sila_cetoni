from os.path import dirname, join

from sila2.framework import Feature

AnalogOutChannelControllerFeature = Feature(open(join(dirname(__file__), "AnalogOutChannelController.sila.xml")).read())
