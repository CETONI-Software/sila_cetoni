from os.path import dirname, join

from sila2.framework import Feature

ValveGatewayServiceFeature = Feature(open(join(dirname(__file__), "ValveGatewayService.sila.xml")).read())
