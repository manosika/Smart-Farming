import pandas as pd

def load_dataset():
    return pd.read_csv('D://smart_farming_app//data//crop_data.csv')

def predict_yield(temp, humidity, weather, season, crop):
    data = load_dataset()
    # Filter the data based on input and calculate crop yield
    filtered_data = data[(data['Temperature'] == temp) &
                         (data['Humidity'] == humidity) &
                         (data['Weather'] == weather) &
                         (data['Season'] == season) &
                         (data['Crop'] == crop)]
    return filtered_data['Yield'].mean()  # Example: return average yield
