# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: BatteryProvider.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import sila2lib.framework.SiLAFramework_pb2 as SiLAFramework__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='BatteryProvider.proto',
  package='sila2.de.cetoni.core.batteryprovider.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15\x42\x61tteryProvider.proto\x12\'sila2.de.cetoni.core.batteryprovider.v1\x1a\x13SiLAFramework.proto\"%\n#Subscribe_BatteryVoltage_Parameters\"Z\n\"Subscribe_BatteryVoltage_Responses\x12\x34\n\x0e\x42\x61tteryVoltage\x18\x01 \x01(\x0b\x32\x1c.sila2.org.silastandard.Real2\xcd\x01\n\x0f\x42\x61tteryProvider\x12\xb9\x01\n\x18Subscribe_BatteryVoltage\x12L.sila2.de.cetoni.core.batteryprovider.v1.Subscribe_BatteryVoltage_Parameters\x1aK.sila2.de.cetoni.core.batteryprovider.v1.Subscribe_BatteryVoltage_Responses\"\x00\x30\x01\x62\x06proto3'
  ,
  dependencies=[SiLAFramework__pb2.DESCRIPTOR,])




_SUBSCRIBE_BATTERYVOLTAGE_PARAMETERS = _descriptor.Descriptor(
  name='Subscribe_BatteryVoltage_Parameters',
  full_name='sila2.de.cetoni.core.batteryprovider.v1.Subscribe_BatteryVoltage_Parameters',
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
  serialized_start=87,
  serialized_end=124,
)


_SUBSCRIBE_BATTERYVOLTAGE_RESPONSES = _descriptor.Descriptor(
  name='Subscribe_BatteryVoltage_Responses',
  full_name='sila2.de.cetoni.core.batteryprovider.v1.Subscribe_BatteryVoltage_Responses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='BatteryVoltage', full_name='sila2.de.cetoni.core.batteryprovider.v1.Subscribe_BatteryVoltage_Responses.BatteryVoltage', index=0,
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
  serialized_start=126,
  serialized_end=216,
)

_SUBSCRIBE_BATTERYVOLTAGE_RESPONSES.fields_by_name['BatteryVoltage'].message_type = SiLAFramework__pb2._REAL
DESCRIPTOR.message_types_by_name['Subscribe_BatteryVoltage_Parameters'] = _SUBSCRIBE_BATTERYVOLTAGE_PARAMETERS
DESCRIPTOR.message_types_by_name['Subscribe_BatteryVoltage_Responses'] = _SUBSCRIBE_BATTERYVOLTAGE_RESPONSES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Subscribe_BatteryVoltage_Parameters = _reflection.GeneratedProtocolMessageType('Subscribe_BatteryVoltage_Parameters', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBE_BATTERYVOLTAGE_PARAMETERS,
  '__module__' : 'BatteryProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.core.batteryprovider.v1.Subscribe_BatteryVoltage_Parameters)
  })
_sym_db.RegisterMessage(Subscribe_BatteryVoltage_Parameters)

Subscribe_BatteryVoltage_Responses = _reflection.GeneratedProtocolMessageType('Subscribe_BatteryVoltage_Responses', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBE_BATTERYVOLTAGE_RESPONSES,
  '__module__' : 'BatteryProvider_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.core.batteryprovider.v1.Subscribe_BatteryVoltage_Responses)
  })
_sym_db.RegisterMessage(Subscribe_BatteryVoltage_Responses)



_BATTERYPROVIDER = _descriptor.ServiceDescriptor(
  name='BatteryProvider',
  full_name='sila2.de.cetoni.core.batteryprovider.v1.BatteryProvider',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=219,
  serialized_end=424,
  methods=[
  _descriptor.MethodDescriptor(
    name='Subscribe_BatteryVoltage',
    full_name='sila2.de.cetoni.core.batteryprovider.v1.BatteryProvider.Subscribe_BatteryVoltage',
    index=0,
    containing_service=None,
    input_type=_SUBSCRIBE_BATTERYVOLTAGE_PARAMETERS,
    output_type=_SUBSCRIBE_BATTERYVOLTAGE_RESPONSES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BATTERYPROVIDER)

DESCRIPTOR.services_by_name['BatteryProvider'] = _BATTERYPROVIDER

# @@protoc_insertion_point(module_scope)