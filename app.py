from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load the dataset (replace with your actual file path)
data = pd.read_csv('data/crop_data.csv')

# Ensure correct data types (if needed)
data['Temperature'] = pd.to_numeric(data['Temperature'], errors='coerce')
data['Humidity'] = pd.to_numeric(data['Humidity'], errors='coerce')
data['Yield'] = pd.to_numeric(data['Yield'], errors='coerce')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the form
    temp = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    weather = request.form['weather']
    season = request.form['season']
    crop = request.form['crop_name']
    visualization_type = request.form['visualization']

    # Call the function to predict crop yield and visualize
    plot_url = visualize_crop_yield(temp, humidity, weather, season, crop, visualization_type)
    
    return render_template('result.html', plot_url=plot_url)

def visualize_crop_yield(temp, humidity, weather, season, crop, visualization_type):
    # Filter dataset based on input values
    filtered_data = data[
        (data['Temperature'].between(temp-5, temp+5)) &  # Temperature within +-5°C
        (data['Humidity'].between(humidity-10, humidity+10)) &  # Humidity within +-10%
        (data['Weather'].str.contains(weather, case=False)) & 
        (data['Season'].str.contains(season, case=False)) & 
        (data['Crop'].str.contains(crop, case=False))
    ]
    
    # If no data matches, generate a plot with default data or suggest the user adjust inputs
    if filtered_data.empty:
        filtered_data = data  # Use all data for a general visualization
        message = "No exact matches found. Displaying general crop yield data."
    else:
        message = "Displaying data based on your inputs."

    # Create the plot based on the selected type
    plt.figure()
    
    if visualization_type == 'line':
        plt.plot(filtered_data['Temperature'], filtered_data['Yield'], marker='o', label='Temperature vs Yield')
        plt.title(f'Yield Prediction for {crop} during {season}')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Yield (kg/hectare)')
        
    elif visualization_type == 'bar':
        plt.bar(filtered_data['Temperature'], filtered_data['Yield'], label='Temperature vs Yield')
        plt.title(f'Yield Prediction for {crop} during {season}')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Yield (kg/hectare)')
        
    elif visualization_type == 'scatter':
        plt.scatter(filtered_data['Temperature'], filtered_data['Yield'], label='Temperature vs Yield')
        plt.title(f'Yield Prediction for {crop} during {season}')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Yield (kg/hectare)')

    # Save plot to a string buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f'data:image/png;base64,{image}'

if __name__ == '__main__':
    app.run(debug=True)
