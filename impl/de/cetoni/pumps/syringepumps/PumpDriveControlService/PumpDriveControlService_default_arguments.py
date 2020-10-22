# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import PumpDriveControlService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['InitializePumpDrive_Parameters'] = {
    
}

default_dict['InitializePumpDrive_Responses'] = {
    
}

default_dict['EnablePumpDrive_Parameters'] = {
    
}

default_dict['EnablePumpDrive_Responses'] = {
    
}

default_dict['DisablePumpDrive_Parameters'] = {
    
}

default_dict['DisablePumpDrive_Responses'] = {
    
}

default_dict['Subscribe_PumpDriveState_Responses'] = {
    'PumpDriveState': silaFW_pb2.Boolean(value=False)
}

default_dict['Subscribe_FaultState_Responses'] = {
    'FaultState': silaFW_pb2.Boolean(value=False)
}
