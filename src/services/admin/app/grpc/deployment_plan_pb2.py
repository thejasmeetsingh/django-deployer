# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: deployment_plan.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x64\x65ployment_plan.proto\x12\x0e\x44\x65ploymentPlan\"&\n\x15\x44\x65ploymentPlanRequest\x12\r\n\x05token\x18\x01 \x01(\t\"T\n\x16\x44\x65ploymentPlanResponse\x12\x0c\n\x04plan\x18\x01 \x01(\t\x12\x15\n\rinstance_tier\x18\x02 \x01(\t\x12\x15\n\rinstance_type\x18\x03 \x01(\t2~\n\x15\x44\x65ploymentPlanService\x12\x65\n\x12GetDeploymentPlans\x12%.DeploymentPlan.DeploymentPlanRequest\x1a&.DeploymentPlan.DeploymentPlanResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'deployment_plan_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DEPLOYMENTPLANREQUEST']._serialized_start=41
  _globals['_DEPLOYMENTPLANREQUEST']._serialized_end=79
  _globals['_DEPLOYMENTPLANRESPONSE']._serialized_start=81
  _globals['_DEPLOYMENTPLANRESPONSE']._serialized_end=165
  _globals['_DEPLOYMENTPLANSERVICE']._serialized_start=167
  _globals['_DEPLOYMENTPLANSERVICE']._serialized_end=293
# @@protoc_insertion_point(module_scope)
