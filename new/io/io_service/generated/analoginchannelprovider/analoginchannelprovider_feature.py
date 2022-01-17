from os.path import dirname, join

from sila2.framework import Feature

AnalogInChannelProviderFeature = Feature(open(join(dirname(__file__), "AnalogInChannelProvider.sila.xml")).read())
