from os.path import dirname, join

from sila2.framework import Feature

SystemStatusProviderFeature = Feature(open(join(dirname(__file__), "SystemStatusProvider.sila.xml")).read())
