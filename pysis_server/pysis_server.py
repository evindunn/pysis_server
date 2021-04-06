from concurrent.futures.thread import ThreadPoolExecutor
from logging import getLogger
from urllib.request import urlretrieve

from pysis import IsisPool
from pysis.exceptions import ProcessError as IsisError

from .pysis_server_pb2_grpc import PysisServicer as _PysisServicer
from .pysis_server_pb2 import PysisCommand, PysisResult
from .isis_file import IsisFile


class PysisServicer(_PysisServicer):
    FILE_CHUNK_SIZE = 8192

    async def Isis(self, request: PysisCommand, context) -> PysisResult:
        logger = getLogger(self.__class__.__name__)

        result = PysisResult(return_code=0, to=list(), stderr="")
        dl_threads = list()

        with ThreadPoolExecutor() as pool:
            for url in request.from_:
                logger.debug("Downloading {}...".format(url))
                dl_thread = pool.submit(PysisServicer._download_file, url)
                dl_threads.append(dl_thread)

        input_files = [dl_thread.result() for dl_thread in dl_threads]
        logger.debug("Downloads complete.")

        try:
            with IsisPool() as isis:
                isis_cmd = getattr(isis, request.command)
                for file in input_files:
                    logger.debug(
                        "Running {} on {}...".format(request.command, file.input_target.name)
                    )
                    isis_cmd(
                        from_=file.input_target,
                        to=file.output_target,
                        **request.args
                    )
                    result.to.append(file.output_target.name)

        except IsisError as e:
            result.to = list()
            result.return_code = e.returncode
            result.stderr = e.stderr
            logger.error("{} failed: {}".format(request.command, e.stderr.strip()))

        logger.debug("{} complete.".format(request.command))
        [isis_file.cleanup() for isis_file in input_files]

        return result

    @staticmethod
    def _download_file(url) -> IsisFile:
        isis_file = IsisFile()
        urlretrieve(url, isis_file.input_target.name)
        return isis_file
