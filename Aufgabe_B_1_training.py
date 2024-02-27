import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import models, layers

# Assuming 'data' is your DataFrame containing the features, target, and 'zaehlstelle'
data = pd.read_csv('./FahrradMuenchen/combined_tage.csv')  # Adjust the path to your dataset

# Preprocessing: Fill or remove NaN values as appropriate for your dataset
# For simplicity, this example drops rows with any NaN values
# remove 0 values in the "gesamt" column
#remove 95% quantile
# data = data[data['gesamt'] < data['gesamt'].quantile(0.95)]


# Iterate through each unique 'zaehlstelle'
for zaehlstelle in data['zaehlstelle'].unique():
    print(f"Training model for: {zaehlstelle}")
    
    # Filter data for the current 'zaehlstelle'
    data_filtered = data[data['zaehlstelle'] == zaehlstelle]
    
    # Define features and target variable
    X = data_filtered[['max.temp', 'min.temp', 'niederschlag', 'bewoelkung', 'sonnenstunden']]  # Adjust as needed
    y = data_filtered['gesamt']  # Target variable
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    
    # Initialize and train the linear regression model
    model = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
        layers.Dropout(0.5),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='msle', metrics=['mae', 'mse'])
    model.fit(X, y, validation_split=0.2, epochs=500, batch_size=32, verbose=0, shuffle=True)
    
    # save the model
    model.save(f'./ProcessedData/predictionModels/{zaehlstelle}.h5')
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    y_pred = y_pred.reshape(-1)
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    correlation = np.corrcoef(y_test, y_pred)[0, 1]

    # perform linear regression between actual and predicted values
    slope, intercept = np.polyfit(y_test.values.reshape(-1), y_pred.reshape(-1), 1)


    #plot prediction against actual values with regression line
    # Plot the regression line
    plt.plot(y_test, slope * y_test + intercept, color='red', label='Regression Line')
    plt.plot(y_test, y_test, color='blue', linestyle='dotted', label='Ideal Prediction')
    plt.scatter(y_test, y_pred)
    plt.title(f'Actual vs. Predicted Values for {zaehlstelle} (correlation = {correlation:.2f})')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.legend(title=zaehlstelle, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    
    print(f"Correlation coefficient for {zaehlstelle}: {correlation:.2f}")
    print(f"R-squared (R2) for {zaehlstelle}: {r2:.2f}\n")

# Note: This example prints out the MSE and R-squared for each model. 
# You might want to store these metrics for further analysis or comparison.
