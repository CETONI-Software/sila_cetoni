from os.path import dirname, join

from sila2.framework import Feature

ValvePositionControllerFeature = Feature(open(join(dirname(__file__), "ValvePositionController.sila.xml")).read())
