import pandas as pd
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('odds.csv')

# Calculate the absolute difference between the first column and the second column in the csv file
matrix1 = data[data.columns[0]]
matrix2 = data[data.columns[1]]
data['rounds_per_game'] = data[data.columns[2]]
data['abs_diff'] = abs(matrix1 - matrix2)


# Perform linear regression using the absolute difference and column 3
X = data[['abs_diff']]
y = data['rounds_per_game']
regressor = LinearRegression()
regressor.fit(X, y)

# Plot the regression line
plt.scatter(X, y)
plt.plot(X, regressor.predict(X), color='red')
plt.xlabel('Absolute Difference in odds')
plt.ylabel('Rounds per game')
plt.title('Linear Regression')
plt.show()

#print the correlation coefficient
correlation = regressor.coef_[0]
print(f"Correlation between Odds Difference and Rounds per game: {correlation}")

# Predict the value of column 3 for an absolute difference of 0.5
predicted_value = regressor.predict([[0.9]])
print(f"Rounds per game for an odds difference of 0.9: {predicted_value[0]}")
# print the confidence score 
confidence = regressor.score(X, y)
print(f"Confidence Score: {confidence}")
