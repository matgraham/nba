# ## Machine Learning Section
import pandas as pd
import numpy as np
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.externals import joblib


def rf_regressor(df):
    '''the rf_regressor function will be passed a dataframe and run through a random forest regression function for each item
    that comprises the fantasy points'''

    df_comparison = pd.DataFrame()
    stats = ['TOV', 'REB', '3PM', 'FGM', 'AST', 'STL', 'BLK']

    for i in stats:
        X = df.drop(columns=stats)
        X_columns = X.columns
        with open('columns.txt', 'w') as f:
            for item in X_columns:
                f.write("%s\n" % item)
        y = df[i]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        
        regr = RandomForestRegressor()

        regr.fit(X_train, y_train)
        
        predictions = regr.predict(X_test)
        
        #For investigating 
        # df_comparison2 = pd.DataFrame({'Actual': y_test, 'Predicted': predictions, 'Actual Index': y_test.index})  
        # df_comparison2['Difference'] = np.sqrt((df_comparison2['Actual'] - df_comparison2['Predicted']) ** 2)
        # print(i)
        # print(df_comparison2.nlargest(5,'Difference'))
        # problem = df_comparison2.nlargest(5,'Difference').iloc[0][2]
        # problem = X_test.loc[problem]
        # problem = problem.where(problem >= 1)
        # problem = problem.dropna()
        # print(problem)

        #Pickle Creation
        joblib.dump(regr,'F:\\Projects\\NBA\\Pickles\\' + i + '.pkl')
        

        print(i + ' ' + 'RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

        df_comparison[i] = predictions
    return df_comparison 