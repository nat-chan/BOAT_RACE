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
racer_dict = racer.load_fanXXXX("./racer/fan1804.txt")

y = race_array[:,1]
X = np.array([list(racer_dict[int(i)].values()) for i in race_array[:,0]])
X = X/np.max(X) #normalization
target_column = racer_dict[int(race_array[:,0][0])].keys()

def print_red(x):
    print()
    print("\033[31m%s\033[0m"%x)

def print_results(model, X_train, X_test, y_train, y_test):
    print("\033[32mtest\033[0m")
    predicted_test = model.predict(X_test)
    rms = np.mean((predicted_test - y_test)*(predicted_test - y_test))
    mean = np.mean(y_test)
    sd = np.sqrt(np.var(y_test))
    print("rms: %s, mean: %s, sd: %s"%(rms,mean,sd))

    print("\033[32mtrain\033[0m")
    predicted_train = lr.predict(X_train)
    rms = np.mean((predicted_train - y_train)*(predicted_train - y_train))
    mean = np.mean(y_train)
    sd = np.sqrt(np.var(y_train))
    print("rms: %s, mean: %s, sd: %s"%(rms,mean,sd))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

print_red("Linear regression")
lr = LinearRegression()
lr.fit(X_train, y_train)
LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
print_results(lr, X_train, X_test, y_train, y_test)

print_red("Ridge regression")
rr = Ridge(alpha=0.01)
rr.fit(X_train, y_train) 
print_results(rr, X_train, X_test, y_train, y_test)

print_red("Lasso")
model_lasso = Lasso(alpha=0.01)
model_lasso.fit(X_train, y_train) 
print_results(model_lasso, X_train, X_test, y_train, y_test)

print_red("Elastic Net")
model_enet = ElasticNet(alpha = 0.01)
model_enet.fit(X_train, y_train) 
print_results(model_enet, X_train, X_test, y_train, y_test)




