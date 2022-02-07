from os.path import dirname, join

from sila2.framework import Feature

BalanceServiceFeature = Feature(open(join(dirname(__file__), "BalanceService.sila.xml")).read())
