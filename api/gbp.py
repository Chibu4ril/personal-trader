import requests
import pandas as pd
import os
import shutil

# Define API key and symbols
api_key = 'MBNP6VWFOFNV6Y6J'  # Replace with your Alpha Vantage API key
symbols = ['GBPUSD', 'EURUSD', 'XAUUSD']  # Currency pairs you want to fetch
output_dir = 'dataset/ohlc_data/'  # Directory to save OHLC data
base_dir = 'dataset/'  # Base directory for valid/invalid structure datasets

source_path = 'dataset/annotated_image/'  # Replace with your source path
valid_dir = 'dataset/valid_structure/'  # Directory for valid annotated screenshots
invalid_dir = 'dataset/invalid_structure/'  # Directory for invalid annotated screenshots


def create_directories(base_dir):
    # Create directories if they do not exist
    subdirs = ['valid_structure', 'invalid_structure']
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)


def move_annotated_screenshots(source_path, dest_valid, dest_invalid):
    valid_files = [f for f in os.listdir(source_path) if 'valid' in f]
    invalid_files = [f for f in os.listdir(source_path) if 'invalid' in f]
    
    # Move valid files
    for valid_file in valid_files:
        if os.path.exists(os.path.join(source_path, valid_file)):
            shutil.move(os.path.join(source_path, valid_file), dest_valid)

    # Move invalid files
    for invalid_file in invalid_files:
        if os.path.exists(os.path.join(source_path, invalid_file)):
            shutil.move(os.path.join(source_path, invalid_file), dest_invalid)


# Fetch data for each symbol
def fetch_ohlc_data(api_key, symbols, output_dir):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'apikey': api_key,
        'datatype': 'csv'
    }

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for symbol in symbols:
        params['symbol'] = symbol
        url = f"{base_url}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&datatype=csv"
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(f"{output_dir}/{symbol}_data.csv", 'w') as file:
                file.write(response.text)
            print(f"Data for {symbol} saved.")
        else:
            print(f"Failed to fetch data for {symbol}.")


# Main execution
create_directories(base_dir)
move_annotated_screenshots(source_path, valid_dir, invalid_dir)
fetch_ohlc_data(api_key, symbols, output_dir)
