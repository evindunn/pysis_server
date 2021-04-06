#!/usr/bin/env python3
import grpc

from pysis_server import PysisStub, PysisCommand


def main():
    SERVER_ADDR = "127.0.0.1"
    SERVER_PORT = 8080
    URLS = [
        "https://pdsimage.wr.usgs.gov/Missions/Mars_Reconnaissance_Orbiter/CTX/mrox_2578/data/J03_045994_1986_XN_18N282W.IMG",
        "https://pdsimage.wr.usgs.gov/Missions/Mars_Reconnaissance_Orbiter/CTX/mrox_2968/data/J21_052811_1983_XN_18N282W.IMG"
    ]

    grpc_channel = grpc.insecure_channel("{}:{}".format(SERVER_ADDR, SERVER_PORT))
    pysis_client = PysisStub(grpc_channel)

    pysis_command = PysisCommand(command="mroctx2isis", from_=URLS, args={})
    pysis_result = pysis_client.Isis(pysis_command)

    print([result for result in pysis_result.to])


if __name__ == '__main__':
    main()
