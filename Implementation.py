import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
#from sklearn.neighbors import KNeighborsRegressor
#from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
#from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


import racer # ogino
import race  # ebata

race_array = np.array(race.get_race_info("./race/2018/K180531.TXT")).reshape(-1,2)
racer.load_fanXXXX("./racer/fan1804.txt")


target_column = ['time']
predictors = list(set(list(df.columns))-set(target_column)) # List of features excluding target variable
df[predictors] = df[predictors]/df[predictors].max() # normalize the predictors since the units are different  to avoid innfluencing of prediction process

X = df[predictors].values # create arrays of indipendent x variable and dependent y variables
y = df[target_column].values

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
#Linear regression

lr = LinearRegression()
lr.fit(X_train, y_train)
#LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
