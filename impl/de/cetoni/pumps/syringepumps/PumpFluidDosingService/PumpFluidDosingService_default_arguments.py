# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import PumpFluidDosingService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['SetFillLevel_Parameters'] = {
    'FillLevel': silaFW_pb2.Real(value=0.0),
    'FlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFillLevel_Responses'] = {
    
}

default_dict['DoseVolume_Parameters'] = {
    'Volume': silaFW_pb2.Real(value=0.0),
    'FlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['DoseVolume_Responses'] = {
    
}

default_dict['GenerateFlow_Parameters'] = {
    'FlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['GenerateFlow_Responses'] = {
    
}

default_dict['StopDosage_Parameters'] = {
    
}

default_dict['StopDosage_Responses'] = {
    
}

default_dict['Subscribe_MaxSyringeFillLevel_Responses'] = {
    'MaxSyringeFillLevel': silaFW_pb2.Real(value=0.0)
}

default_dict['Subscribe_SyringeFillLevel_Responses'] = {
    'SyringeFillLevel': silaFW_pb2.Real(value=0.0)
}

default_dict['Subscribe_MaxFlowRate_Responses'] = {
    'MaxFlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['Subscribe_FlowRate_Responses'] = {
    'FlowRate': silaFW_pb2.Real(value=0.0)
}
