from os.path import dirname, join

from sila2.framework import Feature

SyringeConfigurationControllerFeature = Feature(
    open(join(dirname(__file__), "SyringeConfigurationController.sila.xml")).read()
)
