#!/usr/bin/env python3

import asyncio
import grpc

from dotenv import load_dotenv
from os import getenv, environ as os_environ
from pysis_server import PysisServicer, add_PysisServicer_to_server
from logging import basicConfig as logging_basic_config, DEBUG


async def main():
    load_dotenv()

    logging_basic_config(
        format="[%(asctime)s][%(levelname)s][%(name)s] %(msg)s",
        datefmt="%F %T",
        level=DEBUG
    )

    os_environ["ISISROOT"] = getenv("CONDA_PREFIX")
    server_addr = getenv("SERVER_ADDR")
    server_port = getenv("SERVER_PORT")

    server = grpc.aio.server()
    add_PysisServicer_to_server(PysisServicer(), server)
    server.add_insecure_port("{}:{}".format(server_addr, server_port))

    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
