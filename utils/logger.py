import logging

logger = logging.getLogger("CoVid-19")


# Set the verbosity level
def set_verbosity(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
