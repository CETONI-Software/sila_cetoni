from os.path import dirname, join

from sila2.framework import Feature

DigitalInChannelProviderFeature = Feature(open(join(dirname(__file__), "DigitalInChannelProvider.sila.xml")).read())
