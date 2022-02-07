from os.path import dirname, join

from sila2.framework import Feature

PumpUnitControllerFeature = Feature(open(join(dirname(__file__), "PumpUnitController.sila.xml")).read())
