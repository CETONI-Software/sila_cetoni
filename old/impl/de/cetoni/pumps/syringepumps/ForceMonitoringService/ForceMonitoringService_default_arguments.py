# This file contains default values that are used for the implementations to supply them with
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import ForceMonitoringService_pb2 as pb2

# initialise the default dictionary so we can add keys.
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()
default_dict['DataType_Force'] = {
    'Force': silaFW_pb2.Real(value=1.0)
}

default_dict['ClearForceSafetyStop_Parameters'] = {

}

default_dict['ClearForceSafetyStop_Responses'] = {

}

default_dict['EnableForceMonitoring_Parameters'] = {

}

default_dict['EnableForceMonitoring_Responses'] = {

}

default_dict['DisableForceMonitoring_Parameters'] = {

}

default_dict['DisableForceMonitoring_Responses'] = {

}

default_dict['SetForceLimit_Parameters'] = {
    'ForceLimit': pb2.DataType_Force(**default_dict['DataType_Force'])
}

default_dict['SetForceLimit_Responses'] = {

}

default_dict['Subscribe_ForceSensorValue_Responses'] = {
    'ForceSensorValue': pb2.DataType_Force(**default_dict['DataType_Force'])
}

default_dict['Subscribe_ForceLimit_Responses'] = {
    'ForceLimit': pb2.DataType_Force(**default_dict['DataType_Force'])
}

default_dict['Subscribe_MaxDeviceForce_Responses'] = {
    'MaxDeviceForce': pb2.DataType_Force(**default_dict['DataType_Force'])
}

default_dict['Subscribe_ForceMonitoringEnabled_Responses'] = {
    'ForceMonitoringEnabled': silaFW_pb2.Boolean(value=False)
}

default_dict['Subscribe_ForceSafetyStopActive_Responses'] = {
    'ForceSafetyStopActive': silaFW_pb2.Boolean(value=False)
}
