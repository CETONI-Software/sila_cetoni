# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AnalogInChannelProvider.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import sila2lib.framework.SiLAFramework_pb2 as SiLAFramework__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='AnalogInChannelProvider.proto',
  package='sila2.de.cetoni.io.analoginchannelprovider.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1d\x41nalogInChannelProvider.proto\x12-sila2.de.cetoni.io.analoginchannelprovider.v1\x1a\x13SiLAFramework.proto\"!\n\x1fGet_NumberOfChannels_Parameters\"[\n\x1eGet_NumberOfChannels_Responses\x12\x39\n\x10NumberOfChannels\x18\x01 \x01(\x0b\x32\x1f.sila2.org.silastandard.Integer\"\x1c\n\x1aSubscribe_Value_Parameters\"H\n\x19Subscribe_Value_Responses\x12+\n\x05Value\x18\x01 \x01(\x0b\x32\x1c.sila2.org.silastandard.Real\"3\n1Get_FCPAffectedByMetadata_ChannelIndex_Parameters\"i\n0Get_FCPAffectedByMetadata_ChannelIndex_Responses\x12\x35\n\rAffectedCalls\x18\x01 \x03(\x0b\x32\x1e.sila2.org.silastandard.String\"N\n\x15Metadata_ChannelIndex\x12\x35\n\x0c\x43hannelIndex\x18\x01 \x01(\x0b\x32\x1f.sila2.org.silastandard.Integer2\xf0\x04\n\x17\x41nalogInChannelProvider\x12\xb7\x01\n\x14Get_NumberOfChannels\x12N.sila2.de.cetoni.io.analoginchannelprovider.v1.Get_NumberOfChannels_Parameters\x1aM.sila2.de.cetoni.io.analoginchannelprovider.v1.Get_NumberOfChannels_Responses\"\x00\x12\xaa\x01\n\x0fSubscribe_Value\x12I.sila2.de.cetoni.io.analoginchannelprovider.v1.Subscribe_Value_Parameters\x1aH.sila2.de.cetoni.io.analoginchannelprovider.v1.Subscribe_Value_Responses\"\x00\x30\x01\x12\xed\x01\n&Get_FCPAffectedByMetadata_ChannelIndex\x12`.sila2.de.cetoni.io.analoginchannelprovider.v1.Get_FCPAffectedByMetadata_ChannelIndex_Parameters\x1a_.sila2.de.cetoni.io.analoginchannelprovider.v1.Get_FCPAffectedByMetadata_ChannelIndex_Responses\"\x00\x62\x06proto3'
  ,
  dependencies=[SiLAFramework__pb2.DESCRIPTOR,])




_GET_NUMBEROFCHANNELS_PARAMETERS = _descriptor.Descriptor(
  name='Get_NumberOfChannels_Parameters',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Get_NumberOfChannels_Parameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=134,
)


_GET_NUMBEROFCHANNELS_RESPONSES = _descriptor.Descriptor(
  name='Get_NumberOfChannels_Responses',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Get_NumberOfChannels_Responses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='NumberOfChannels', full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Get_NumberOfChannels_Responses.NumberOfChannels', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=136,
  serialized_end=227,
)


_SUBSCRIBE_VALUE_PARAMETERS = _descriptor.Descriptor(
  name='Subscribe_Value_Parameters',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Subscribe_Value_Parameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=229,
  serialized_end=257,
)


_SUBSCRIBE_VALUE_RESPONSES = _descriptor.Descriptor(
  name='Subscribe_Value_Responses',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Subscribe_Value_Responses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Value', full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Subscribe_Value_Responses.Value', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=259,
  serialized_end=331,
)


_GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_PARAMETERS = _descriptor.Descriptor(
  name='Get_FCPAffectedByMetadata_ChannelIndex_Parameters',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Get_FCPAffectedByMetadata_ChannelIndex_Parameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=333,
  serialized_end=384,
)


_GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_RESPONSES = _descriptor.Descriptor(
  name='Get_FCPAffectedByMetadata_ChannelIndex_Responses',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Get_FCPAffectedByMetadata_ChannelIndex_Responses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='AffectedCalls', full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Get_FCPAffectedByMetadata_ChannelIndex_Responses.AffectedCalls', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=386,
  serialized_end=491,
)


_METADATA_CHANNELINDEX = _descriptor.Descriptor(
  name='Metadata_ChannelIndex',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Metadata_ChannelIndex',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ChannelIndex', full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.Metadata_ChannelIndex.ChannelIndex', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=493,
  serialized_end=571,
)

_GET_NUMBEROFCHANNELS_RESPONSES.fields_by_name['NumberOfChannels'].message_type = SiLAFramework__pb2._INTEGER
_SUBSCRIBE_VALUE_RESPONSES.fields_by_name['Value'].message_type = SiLAFramework__pb2._REAL
_GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_RESPONSES.fields_by_name['AffectedCalls'].message_type = SiLAFramework__pb2._STRING
_METADATA_CHANNELINDEX.fields_by_name['ChannelIndex'].message_type = SiLAFramework__pb2._INTEGER
DESCRIPTOR.message_types_by_name['Get_NumberOfChannels_Parameters'] = _GET_NUMBEROFCHANNELS_PARAMETERS
DESCRIPTOR.message_types_by_name['Get_NumberOfChannels_Responses'] = _GET_NUMBEROFCHANNELS_RESPONSES
DESCRIPTOR.message_types_by_name['Subscribe_Value_Parameters'] = _SUBSCRIBE_VALUE_PARAMETERS
DESCRIPTOR.message_types_by_name['Subscribe_Value_Responses'] = _SUBSCRIBE_VALUE_RESPONSES
DESCRIPTOR.message_types_by_name['Get_FCPAffectedByMetadata_ChannelIndex_Parameters'] = _GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_PARAMETERS
DESCRIPTOR.message_types_by_name['Get_FCPAffectedByMetadata_ChannelIndex_Responses'] = _GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_RESPONSES
DESCRIPTOR.message_types_by_name['Metadata_ChannelIndex'] = _METADATA_CHANNELINDEX
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Get_NumberOfChannels_Parameters = _reflection.GeneratedProtocolMessageType('Get_NumberOfChannels_Parameters', (_message.Message,), {
  'DESCRIPTOR' : _GET_NUMBEROFCHANNELS_PARAMETERS,
  '__module__' : 'AnalogInChannelProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.io.analoginchannelprovider.v1.Get_NumberOfChannels_Parameters)
  })
_sym_db.RegisterMessage(Get_NumberOfChannels_Parameters)

Get_NumberOfChannels_Responses = _reflection.GeneratedProtocolMessageType('Get_NumberOfChannels_Responses', (_message.Message,), {
  'DESCRIPTOR' : _GET_NUMBEROFCHANNELS_RESPONSES,
  '__module__' : 'AnalogInChannelProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.io.analoginchannelprovider.v1.Get_NumberOfChannels_Responses)
  })
_sym_db.RegisterMessage(Get_NumberOfChannels_Responses)

Subscribe_Value_Parameters = _reflection.GeneratedProtocolMessageType('Subscribe_Value_Parameters', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBE_VALUE_PARAMETERS,
  '__module__' : 'AnalogInChannelProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.io.analoginchannelprovider.v1.Subscribe_Value_Parameters)
  })
_sym_db.RegisterMessage(Subscribe_Value_Parameters)

Subscribe_Value_Responses = _reflection.GeneratedProtocolMessageType('Subscribe_Value_Responses', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBE_VALUE_RESPONSES,
  '__module__' : 'AnalogInChannelProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.io.analoginchannelprovider.v1.Subscribe_Value_Responses)
  })
_sym_db.RegisterMessage(Subscribe_Value_Responses)

Get_FCPAffectedByMetadata_ChannelIndex_Parameters = _reflection.GeneratedProtocolMessageType('Get_FCPAffectedByMetadata_ChannelIndex_Parameters', (_message.Message,), {
  'DESCRIPTOR' : _GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_PARAMETERS,
  '__module__' : 'AnalogInChannelProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.io.analoginchannelprovider.v1.Get_FCPAffectedByMetadata_ChannelIndex_Parameters)
  })
_sym_db.RegisterMessage(Get_FCPAffectedByMetadata_ChannelIndex_Parameters)

Get_FCPAffectedByMetadata_ChannelIndex_Responses = _reflection.GeneratedProtocolMessageType('Get_FCPAffectedByMetadata_ChannelIndex_Responses', (_message.Message,), {
  'DESCRIPTOR' : _GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_RESPONSES,
  '__module__' : 'AnalogInChannelProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.io.analoginchannelprovider.v1.Get_FCPAffectedByMetadata_ChannelIndex_Responses)
  })
_sym_db.RegisterMessage(Get_FCPAffectedByMetadata_ChannelIndex_Responses)

Metadata_ChannelIndex = _reflection.GeneratedProtocolMessageType('Metadata_ChannelIndex', (_message.Message,), {
  'DESCRIPTOR' : _METADATA_CHANNELINDEX,
  '__module__' : 'AnalogInChannelProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.io.analoginchannelprovider.v1.Metadata_ChannelIndex)
  })
_sym_db.RegisterMessage(Metadata_ChannelIndex)



_ANALOGINCHANNELPROVIDER = _descriptor.ServiceDescriptor(
  name='AnalogInChannelProvider',
  full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=574,
  serialized_end=1198,
  methods=[
  _descriptor.MethodDescriptor(
    name='Get_NumberOfChannels',
    full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider.Get_NumberOfChannels',
    index=0,
    containing_service=None,
    input_type=_GET_NUMBEROFCHANNELS_PARAMETERS,
    output_type=_GET_NUMBEROFCHANNELS_RESPONSES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Subscribe_Value',
    full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider.Subscribe_Value',
    index=1,
    containing_service=None,
    input_type=_SUBSCRIBE_VALUE_PARAMETERS,
    output_type=_SUBSCRIBE_VALUE_RESPONSES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Get_FCPAffectedByMetadata_ChannelIndex',
    full_name='sila2.de.cetoni.io.analoginchannelprovider.v1.AnalogInChannelProvider.Get_FCPAffectedByMetadata_ChannelIndex',
    index=2,
    containing_service=None,
    input_type=_GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_PARAMETERS,
    output_type=_GET_FCPAFFECTEDBYMETADATA_CHANNELINDEX_RESPONSES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ANALOGINCHANNELPROVIDER)

DESCRIPTOR.services_by_name['AnalogInChannelProvider'] = _ANALOGINCHANNELPROVIDER

# @@protoc_insertion_point(module_scope)