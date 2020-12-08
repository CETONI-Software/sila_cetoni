# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import DigitalOutChannelController_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()
default_dict['DataType_State'] = {
    'State': silaFW_pb2.String(value='default string')
}

default_dict['SetOutput_Parameters'] = {
    'State': pb2.DataType_State(**default_dict['DataType_State'])
}

default_dict['SetOutput_Responses'] = {
    
}

default_dict['Subscribe_State_Responses'] = {
    'State': pb2.DataType_State(**default_dict['DataType_State'])
}
