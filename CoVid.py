from db.utils import Database
from utils.logger import logger, set_verbosity
import argparse


# Parse input arguments
def define_and_parse_args():

    parser = argparse.ArgumentParser(description='CoVid-19 analyzer tool')
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    return parser.parse_args()


def main(args):
    # Set the verbosity
    set_verbosity(args.verbose)

    # Get the arguments
    confirmed = Database("confirmed")

    italy_confirmed = confirmed.get_patients_by_country("Italy")

    logger.info("Italian Confirmed patients")
    logger.info(italy_confirmed)

    logger.info("Countries with confirmed patients")
    logger.info(confirmed.get_countries())


if __name__ == "__main__":
    args = define_and_parse_args()
    main(args)
