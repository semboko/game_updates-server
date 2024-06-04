import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
