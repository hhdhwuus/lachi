import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Load your dataset
data = pd.read_csv('./ProcessedData/combined_tage.csv')  # Adjust the path to your dataset

# Preprocess your data similarly to how it was preprocessed before training the models
# For this example, let's assume preprocessing involves just selecting the relevant features
features = ['max.temp', 'min.temp', 'niederschlag', 'bewoelkung', 'sonnenstunden']
target = 'gesamt'

# Assuming your models are saved in a directory called 'ProcessedData/predictionModels'
model_dir = './ProcessedData/predictionModels/'
zaehlstellen = data['zaehlstelle'].unique()

# Initialize a dictionary to store results for plotting
results = {}

for zaehlstelle in zaehlstellen:
    model_path = f'{model_dir}{zaehlstelle}.h5'
    model = load_model(model_path)
    
    # Filter data for the current 'zaehlstelle'
    data_filtered = data[data['zaehlstelle'] == zaehlstelle]
    X = data_filtered[features]
    y = data_filtered[target]
    
    # Make predictions
    y_pred = model.predict(X).reshape(-1)
    
    # Store results for plotting
    results[zaehlstelle] = (y, y_pred)

# Plotting
num_stations = len(zaehlstellen)
cols = 3  # Adjust based on your preference
rows = num_stations // cols + (num_stations % cols > 0)

plt.figure(figsize=(cols * 5, rows * 5))  # Adjust figure size as needed

for i, (zaehlstelle, (y, y_pred)) in enumerate(results.items(), 1):
    plt.subplot(rows, cols, i)
    
    correlation = np.corrcoef(y, y_pred)[0, 1]
    slope, intercept = np.polyfit(y.values.reshape(-1), y_pred, 1)
    
    # Plotting
    plt.plot(y, slope * y + intercept, color='red', label='Regression Line')
    plt.plot(y, y, color='blue', linestyle='dotted', label='Ideal Prediction')
    plt.scatter(y, y_pred, s=5, alpha=0.2)
    
    plt.title(f'{zaehlstelle} (Corr: {correlation:.2f})')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.legend(loc='upper left')
    plt.grid(True)

plt.suptitle('Wie beeinflusst das Wetter die Anzahl der Fahrradfahrten?', fontsize=34)

plt.tight_layout()
plt.show()
