# This file contains default values that are used for the implementations to supply them with
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import PumpUnitController_pb2 as pb2

# initialise the default dictionary so we can add keys.
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()
default_dict['DataType_VolumeUnit'] = {
    'VolumeUnit': silaFW_pb2.String(value='default string')
}

default_dict['DataType_TimeUnit'] = {
    'TimeUnit': silaFW_pb2.String(value='default string')
}

default_dict['SetFlowUnit_Parameters'] = {
    'FlowUnit': pb2.SetFlowUnit_Parameters.FlowUnit_Struct(VolumeUnit=pb2.DataType_VolumeUnit(**default_dict['DataType_VolumeUnit']), TimeUnit=pb2.DataType_TimeUnit(**default_dict['DataType_TimeUnit']))
}

default_dict['SetFlowUnit_Responses'] = {

}

default_dict['SetVolumeUnit_Parameters'] = {
    'VolumeUnit': pb2.DataType_VolumeUnit(**default_dict['DataType_VolumeUnit'])
}

default_dict['SetVolumeUnit_Responses'] = {

}

default_dict['Subscribe_FlowUnit_Responses'] = {
    'FlowUnit': pb2.Subscribe_FlowUnit_Responses.FlowUnit_Struct(VolumeUnit=pb2.DataType_VolumeUnit(**default_dict['DataType_VolumeUnit']), TimeUnit=pb2.DataType_TimeUnit(**default_dict['DataType_TimeUnit']))
}

default_dict['Subscribe_VolumeUnit_Responses'] = {
    'VolumeUnit': pb2.DataType_VolumeUnit(**default_dict['DataType_VolumeUnit'])
}
