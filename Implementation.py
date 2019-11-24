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

import matplotlib.pyplot as plt

import racer # ogino
import race  # ebata

race_array = np.array(race.get_race_info("./race/2018/K180531.TXT")).reshape(-1,2)
racer_dict = racer.load_fanXXXX("./racer/fan1804.txt")

y = race_array[:,1]
X = np.array([list(racer_dict[int(i)].values()) for i in race_array[:,0]])
#X = X/np.max(X) #normalization
X = (X - np.mean(X,axis=0))/(np.var(X,axis=0) + 1e-10) #normalization
target_column = np.array(list(racer_dict[int(race_array[:,0][0])].keys()))


df = pd.DataFrame(
{target_column[i]: X[:,i]
for i in range(target_column.shape[0])
}
)

import IPython;IPython.embed()

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

def choice_worst_feature(X_,y):
    rms_list = []
    for i in range(X_.shape[1]):
        X = np.hstack((X_[:,:i],X_[:,(i+1):]))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
        model_lasso = Lasso(alpha=0.01)
        model_lasso.fit(X_train, y_train)
        predicted_test = model_lasso.predict(X_test)
        rms = np.mean((predicted_test - y_test)*(predicted_test - y_test))
        rms_list.append(rms)
    worst_feature = np.argmin(rms_list)
    worst_rms = rms_list[worst_feature]
#    best_feature = np.argmin(rms_list)
#    print("best %s, worst %s"%(rms_list[best_feature], rms_list[worst_feature]))
    return worst_feature, worst_rms


rms_list = []

name_list = []
for i in range(X.shape[1] - 1):
    worst_feature, worst_rms = choice_worst_feature(X,y)
    rms_list.append(worst_rms)
    name_list.append(target_column[worst_feature])
    print(target_column[worst_feature], worst_rms)
    X = np.hstack((X[:,:worst_feature],X[:,(worst_feature+1):]))
    target_column = np.hstack((target_column[:worst_feature],target_column[(worst_feature+1):]))


plt.plot(rms_list)
plt.savefig("results.png")
plt.show()
#import IPython;IPython.embed()

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
#
#print_red("Linear regression")
#lr = LinearRegression()
#lr.fit(X_train, y_train)
#LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
#print_results(lr, X_train, X_test, y_train, y_test)
#
#print_red("Ridge regression")
#rr = Ridge(alpha=0.01)
#rr.fit(X_train, y_train) 
#print_results(rr, X_train, X_test, y_train, y_test)
#
#print_red("Lasso")
#model_lasso = Lasso(alpha=0.01)
#model_lasso.fit(X_train, y_train) 
#print_results(model_lasso, X_train, X_test, y_train, y_test)
#
#print_red("Elastic Net")
#model_enet = ElasticNet(alpha = 0.01)
#model_enet.fit(X_train, y_train) 
#print_results(model_enet, X_train, X_test, y_train, y_test)
#
#
#
#
