#!/usr/bin/env python3

from grpc_tools import protoc

protoc.main((
    '',
    '--python_out=.',
    '--grpc_python_out=.',
    'pysis_server/pysis_server.proto',
))
