from utils.logger import logger, set_verbosity
from analysis.regression import Predictor
from db.utils import Database
import argparse


# Parse input arguments
def define_and_parse_args():

    parser = argparse.ArgumentParser(description='CoVid-19 analyzer tool')
    parser.add_argument("-d",
                        "--days",
                        help="Predict the number of confirmed infection in the next d days",
                        type=int,
                        required=True)
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    return parser.parse_args()


def main(args):
    # Set the verbosity
    set_verbosity(args.verbose)

    # Get the arguments
    confirmed = Database("confirmed")

    italy_confirmed = confirmed.get_patients_by_country("Italy")
    all_confirmed = confirmed.get_patients_by_country()

    logger.info("Italian Confirmed patients")
    logger.info(italy_confirmed.loc[:, italy_confirmed.keys()[4]:italy_confirmed.keys()[-1]])

    logger.info("Countries with confirmed patients")
    logger.info(confirmed.get_countries())

    predictor = Predictor(all_confirmed)

    predictor.generate_model()
    train_dates, test_dates, train_cases, test_cases = predictor.generate_data()

    predictor.fit(train_dates, train_cases)
    # predictor.test(test_dates, test_cases)
    prediction = predictor.predict(args.days)

    logger.info(f"Number of predicted infections in the next {args.days} days: {[int(idx) for idx in prediction[-3:]]}")


if __name__ == "__main__":
    args = define_and_parse_args()
    main(args)
