from os.path import dirname, join

from sila2.framework import Feature

DigitalOutChannelControllerFeature = Feature(
    open(join(dirname(__file__), "DigitalOutChannelController.sila.xml")).read()
)
