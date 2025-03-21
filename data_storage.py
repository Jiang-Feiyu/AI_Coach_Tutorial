import os
import csv
import pandas as pd
from pathlib import Path

def save_data_to_csv(health_data, csv_path="./data/data.csv"):
    """
    将健康数据保存到CSV文件
    
    参数:
        health_data (dict): 包含健康数据的字典
        csv_path (str): CSV文件保存路径
    """
    # 确保目录存在
    directory = os.path.dirname(csv_path)
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    # 将嵌套字典扁平化为一维字典
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
    
    # 检查文件是否存在
    file_exists = os.path.isfile(csv_path)
    
    # 写入CSV
    with open(csv_path, mode='a', newline='') as file:
        fieldnames = flat_data.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writeheader()
        
        # 写入数据行
        writer.writerow(flat_data)
    
    return csv_path