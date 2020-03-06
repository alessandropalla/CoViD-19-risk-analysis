from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.svm import SVR

import pandas as pd
import numpy as np
import datetime

from utils.logger import logger


class Predictor():
    def __init__(self, dataframe):
        cols = dataframe.keys()
        self.timeseries = dataframe.loc[:, cols[4]:cols[-1]]
        self.dates = self.timeseries.keys()

        logger.info(f"Log data from {self.dates.min()} to {self.dates.max()}")

    def generate_model(self):
        kernel = ['linear', 'rbf']
        c = [0.01, 0.1, 1, 10]
        gamma = [0.01, 0.1, 1]
        epsilon = [0.01, 0.1, 1]
        shrinking = [True, False]
        svm_grid = {'kernel': kernel, 'C': c, 'gamma': gamma, 'epsilon': epsilon, 'shrinking': shrinking}

        self.svm = SVR()
        self.model_search = RandomizedSearchCV(self.svm,
                                               svm_grid,
                                               scoring='neg_mean_squared_error',
                                               cv=3,
                                               return_train_score=True,
                                               n_jobs=-1,
                                               n_iter=30,
                                               verbose=False)
        logger.debug(self.model_search)

    def generate_data(self):
        cases = np.array(self.timeseries.sum(axis=0)).reshape(-1, 1)
        dates = np.array(list(range(len(self.dates)))).reshape(-1, 1)
        return train_test_split(dates, cases.ravel(), test_size=0.2, shuffle=False)

    def fit(self, X_train_confirmed, y_train_confirmed):

        logger.info("Fitting the regression model")
        self.model_search.fit(X_train_confirmed, y_train_confirmed)
        self.model = self.model_search.best_estimator_

    def test(self, X_test_confirmed, y_test_confirmed):
        # check against testing data
        logger.info("Testing the regression model")
        svm_test_pred = self.model.predict(X_test_confirmed)

    def predict(self, days_in_future):
        # build the x axis
        future_forcast = np.array([i for i in range(len(self.dates) + days_in_future)]).reshape(-1, 1)
        # Predict x days in the future
        pred = self.model.predict(future_forcast)

        return pred
