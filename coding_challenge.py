import os
import pandas as pd
import numpy as np

# Function to simulate API 1: Return 10 consecutive data points starting from a random timestamp
def api_1(file_path):
   try:
       # Load the CSV file into a DataFrame
       data = pd.read_csv(file_path)
       
       # Check if required columns exist
       if 'Timestamp' not in data.columns or 'Stock-ID' not in data.columns or 'stock price' not in data.columns:
           raise ValueError("Input file is missing one or more required columns: 'Timestamp', 'Stock-ID', 'stock price'")
       
       if len(data) < 10:
           raise ValueError("File has less than 10 data points")
       
       # Randomly select a starting point ensuring there are 10 points available
       start_index = np.random.randint(0, len(data) - 10)
       return data.iloc[start_index:start_index + 10]
   except Exception as e:
       raise RuntimeError(f"Error processing file {file_path}: {e}")

# Function to simulate API 2: Predict the next 3 values based on provided logic
def api_2(data):
   try:
       # Get the second-highest value from the last 10 data points
       second_highest = sorted(data['stock price'].values)[-2]
       
       # Predict the next three values based on the given formula
       n = second_highest
       predictions = [
           n,                         # n+1: Same as second-highest
           n + (n - data.iloc[-1]['stock price']) / 2,  # n+2: Half the difference
           n + (n - data.iloc[-1]['stock price']) / 4   # n+3: One-fourth the difference
       ]
       return predictions
   except Exception as e:
       raise RuntimeError(f"Error predicting values: {e}")

# Main function to process all files and generate output
def process_files(input_dir, output_dir, num_files):
   if not os.path.exists(output_dir):
       os.makedirs(output_dir)
   
   files_processed = 0
   for file_name in os.listdir(input_dir):
       if files_processed >= num_files:
           break
       
       file_path = os.path.join(input_dir, file_name)
       if not file_path.endswith(".csv"):
           continue
       
       try:
           # Step 1: Get 10 consecutive data points using API 1
           data = api_1(file_path)
           
           # Step 2: Predict the next 3 values using API 2
           predictions = api_2(data)
           
           # Step 3: Create the output DataFrame
           output_data = data.copy()
           last_timestamp = pd.to_datetime(data.iloc[-1]['Timestamp'])
           timestamps = pd.date_range(start=last_timestamp, periods=4, freq='D')[1:]
           stock_id = data.iloc[-1]['Stock-ID']
           
           for i, pred in enumerate(predictions):
               output_data = output_data.append({
                   'Stock-ID': stock_id,
                   'Timestamp': timestamps[i].strftime('%d-%m-%Y'),
                   'stock price': pred
               }, ignore_index=True)
           
           # Save the output to a new CSV file
           output_file = os.path.join(output_dir, f"output_{file_name}")
           output_data.to_csv(output_file, index=False)
           files_processed += 1
           print(f"Processed file: {file_name} -> {output_file}")
       except Exception as e:
           print(f"Error processing file {file_name}: {e}")