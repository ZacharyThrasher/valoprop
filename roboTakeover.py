import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
import pandas as pd

# Define your training data
# X represents the player stats and y represents the number of kills
# read data in from sethStats.csv, skipping the first column. The last column is the number of kills


fieldnames = (['Name', 'Agent1', 'Agent2', 'Total Rounds', 'Weighted KPR', 'Weighted KAST', 'Weighted FKPR', 'Weighted FDPR', 'Odds Difference', 'Average Opposing KPR', 'Average Opposing KAST', 'Average Opposing FKPR', 'Average Opposing FDPR', 'Recent Kill Average', 'Actual Kills'])
data = pd.read_csv('testStats.csv', encoding='latin1')


# Split the data into input features (X) and target variable (y)
X = data[fieldnames[1:-1]]


y = data[fieldnames[-1]]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=950)

#implement early stopping to prevent overfitting
early_stopping = EarlyStopping(patience=5, restore_best_weights=True)




from sklearn.metrics import mean_squared_error
from keras.models import load_model
from keras.models import load_model




correct_predictions = 0

#I would like to implement some feature scaling to improve the accuracy of the model. I will use the MinMaxScaler from sklearn.preprocessing to scale the input features to a range of 0 to 1. This will help the model converge faster and improve the accuracy of the predictions.

from sklearn.preprocessing import MinMaxScaler

# Create a MinMaxScaler object
scaler = MinMaxScaler()

# Fit the scaler on the training data and transform the training data
X_train_scaled = scaler.fit_transform(X_train)

# Transform the testing data

X_test_scaled = scaler.transform(X_test)

# Create a new sequential model

'''model = Sequential()
'''
# Add layers to the model

'''model.add(Dense(100, input_dim=13, activation='relu'))
model.add(Dense(1, activation='linear'))'''

# Compile the model

'''model.compile(loss='mean_squared_error', optimizer='adam')
'''
# Fit the model on the scaled training data

'''model.fit(X_train_scaled, y_train, epochs=33, batch_size=1, callbacks=[early_stopping])
'''
# Save the model

'''model.save('valoprop_scaled.keras')
'''
# I would now like to implement some derived features to improve the accuracy of the model. I will add a new feature to the input data that represents the difference between the Weighted KPR and the Weighted FKPR. This feature may help the model learn the relationship between these two statistics and the number of kills.

# Add a new feature to the input data
X_train['KPR_Difference'] = X_train['Weighted KPR'] - X_train['Weighted FKPR']
X_test['KPR_Difference'] = X_test['Weighted KPR'] - X_test['Weighted FKPR']

# Fit the scaler on the training data and transform the training data
X_train_scaled = scaler.fit_transform(X_train)

# Transform the testing data
X_test_scaled = scaler.transform(X_test)

# Create a new sequential model
'''model = Sequential()
'''
# Add layers to the model
'''model.add(Dense(100, input_dim=14, activation='relu'))
model.add(Dense(1, activation='linear'))'''

# Compile the model
'''model.compile(loss='mean_squared_error', optimizer='adam')
'''
# Fit the model on the scaled training data

'''model.fit(X_train_scaled, y_train, epochs=33, batch_size=1, callbacks=[early_stopping])
'''
# Save the model

'''model.save('valoprop_scaled_features.keras')
'''
# I would like to implement more derived features to improve the accuracy of the model. I will add a new feature to the input data that represents the difference between the Weighted KPR and the Odds Difference. This feature may help the model learn the relationship between these two statistics and the number of kills.

# Add a new feature to the input data

X_train['KPR_Odds_Difference'] = X_train['Weighted KPR'] - X_train['Odds Difference']
X_test['KPR_Odds_Difference'] = X_test['Weighted KPR'] - X_test['Odds Difference']

# Fit the scaler on the training data and transform the training data

X_train_scaled = scaler.fit_transform(X_train)

# Transform the testing data

X_test_scaled = scaler.transform(X_test)

# Create a new sequential model

'''model = Sequential()'''

# Add layers to the model

'''model.add(Dense(100, input_dim=15, activation='relu'))
model.add(Dense(1, activation='linear'))'''

# Compile the model

'''model.compile(loss='mean_squared_error', optimizer='adam')
'''
# Fit the model on the scaled training data

'''model.fit(X_train_scaled, y_train, epochs=33, batch_size=1, callbacks=[early_stopping])
'''
# Save the model

'''model.save('valoprop_scaled_features_more.keras')
'''

#I would like to implement some feature selection to improve the accuracy of the model. I will use the SelectKBest class from sklearn.feature_selection to select the top 5 features that are most relevant to the target variable. This will help the model focus on the most important features and improve the accuracy of the predictions.

from sklearn.feature_selection import SelectKBest, f_regression

# Create a SelectKBest object
selector = SelectKBest(score_func=f_regression, k=5)

# Fit the selector on the training data and transform the training data

X_train_selected = selector.fit_transform(X_train_scaled, y_train)

# Transform the testing data

X_test_selected = selector.transform(X_test_scaled)

# Create a new sequential model

'''model = Sequential()'''

# Add layers to the model

'''model.add(Dense(100, input_dim=5, activation='relu'))
model.add(Dense(1, activation='linear'))'''

# Compile the model

'''model.compile(loss='mean_squared_error', optimizer='adam')'''

# Fit the model on the selected training data

'''model.fit(X_train_selected, y_train, epochs=33, batch_size=1, callbacks=[early_stopping])'''

# I would like to implement some hyperparameter tuning to improve the accuracy of the model. I will use the GridSearchCV class from sklearn.model_selection to search for the best combination of hyperparameters for the model. This will help the model find the optimal hyperparameters and improve the accuracy of the predictions.

from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasRegressor

# Define a function that creates the model

'''def create_model(optimizer='adam', neurons=100):
    model = Sequential()
    model.add(Dense(neurons, input_dim=5, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    return model'''

# Create a KerasRegressor object

'''model = KerasRegressor(build_fn=create_model, epochs=33, batch_size=1, verbose=1)'''

# Define the hyperparameters to search

'''param_grid = {
    'optimizer': ['adam', 'sgd'],
    'neurons': [50, 100, 150]
}'''

# Create a GridSearchCV object

'''grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)'''

# Fit the GridSearchCV object on the selected training data

'''grid_result = grid.fit(X_train_selected, y_train)'''

# Print the best hyperparameters

'''print('Best Hyperparameters:', grid_result.best_params_)'''

# Save the best model

'''best_model = grid_result.best_estimator_.model
best_model.save('valoprop_scaled_features_selected_tuned.keras')'''

# I would like to implement some cross-validation to improve the accuracy of the model. I will use the cross_val_score function from sklearn.model_selection to evaluate the model using cross-validation. This will help the model generalize better to new data and improve the accuracy of the predictions.

from sklearn.model_selection import cross_val_score

# Define a function that creates the model

'''def create_model():
    model = Sequential()
    model.add(Dense(100, input_dim=5, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model'''

# Create a KerasRegressor object

'''model = KerasRegressor(build_fn=create_model, epochs=33, batch_size=1, verbose=1)'''

# Evaluate the model using cross-validation

'''scores = cross_val_score(model, X_train_selected, y_train, cv=3)'''

# Print the cross-validation scores

'''print('Cross-Validation Scores:', scores)'''

# I would like to implement some model evaluation to improve the accuracy of the model. I will use the mean_squared_error function from sklearn.metrics to evaluate the model on the testing data. This will help me understand how well the model is performing and improve the accuracy of the predictions.

from sklearn.metrics import mean_squared_error

# Evaluate the model on the testing data

'''predictions = model.predict(X_test_selected)
mse = mean_squared_error(y_test, predictions)'''

# Print the mean squared error

'''print('Mean Squared Error:', mse)
'''
# I would like to implement some model interpretation to improve the accuracy of the model. I will use the feature_importances_ attribute of the model to extract the importance of each feature in the model. This will help me understand which features are most relevant to the target variable and improve the accuracy of the predictions.

# Extract the feature importances

'''feature_importances = model.feature_importances_
'''
# Print the feature importances

'''print('Feature Importances:', feature_importances)
'''

# Load the best model

model = load_model('valoprop_scaled_features_selected_tuned.keras')

# Evaluate the model on the testing data

predictions = model.predict(X_test_selected)
mse = mean_squared_error(y_test, predictions)

# Print the mean squared error

print('Mean Squared Error:', mse)

for i in range(len(X_test_selected)):
    prediction = model.predict(X_test_selected[i].reshape(1, -1))
    print('Predicted kills:', prediction[0][0], 'Actual kills:', y_test.iloc[i])
    #mark the prediction as correct if it is within 1 kill of the actual value and calculate the accuracy
    if abs(prediction[0][0].round() - y_test.iloc[i]) <= 3:
        correct_predictions += 1

accuracy = correct_predictions / len(y_test)
print('Accuracy:', accuracy) 

