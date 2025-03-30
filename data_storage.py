import os
import csv
import pandas as pd
from pathlib import Path

def save_data_to_csv(health_data, csv_path="./data/data.csv"):
    """
    save data into the CSV file
    
    parameters:
        health_data (dict): directory with data
        csv_path (str): CSV file saving path
    """

    directory = os.path.dirname(csv_path)
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    flat_data = {
        "timestamp": health_data["timestamp"],
        "heart_rate": health_data["heart_rate"],
        "blood_pressure_systolic": health_data["blood_pressure"]["systolic"],
        "blood_pressure_diastolic": health_data["blood_pressure"]["diastolic"],
        "blood_oxygen": health_data["blood_oxygen"],
        "pace": health_data["performance"]["pace"],
        "stride": health_data["performance"]["stride"],
        "cadence": health_data["performance"]["cadence"],
        "duration": health_data["performance"]["duration"],
        "distance": health_data["performance"]["distance"],
        "calories": health_data["performance"]["calories"],
        "altitude": health_data["environment"]["altitude"],
        "temperature": health_data["environment"]["temperature"],
        "pressure": health_data["environment"]["pressure"],
        "humidity": health_data["environment"]["humidity"],
        "status": health_data["status"]
    }

    
    def manage_file_rotation(csv_path, max_size_mb=10):
        # ==========================================================
        # Add your code here 
        # Task2 : File Management
        # Modify your code here to:
        # - Implement file rotation based on size or date
        # - Add backup functionality
        # - Check and manage file size
        # ==========================================================
        pass

    # check if the file exists
    file_exists = os.path.isfile(csv_path)
    
    # writr into CSV
    with open(csv_path, mode='a', newline='') as file:
        fieldnames = flat_data.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(flat_data)
    
    return csv_path