import random
import time
import json
from datetime import datetime

class HealthDataSimulator:
    def __init__(self):
        # 初始基准值
        self.base_heart_rate = 75
        self.base_blood_pressure_systolic = 120
        self.base_blood_pressure_diastolic = 80
        self.base_blood_oxygen = 98

    def generate_heart_rate(self):
        """生成模拟心率数据 (60-100 bpm)"""
        return round(self.base_heart_rate + random.uniform(-15, 15))

    def generate_blood_pressure(self):
        """生成模拟血压数据 (收缩压/舒张压)"""
        systolic = round(self.base_blood_pressure_systolic + random.uniform(-10, 10))
        diastolic = round(self.base_blood_pressure_diastolic + random.uniform(-10, 10))
        return {"systolic": systolic, "diastolic": diastolic}

    def generate_blood_oxygen(self):
        """生成模拟血氧数据 (95-100%)"""
        return round(self.base_blood_oxygen + random.uniform(-3, 2), 1)

    def generate_health_data(self):
        """生成完整的健康数据集"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "timestamp": timestamp,
            "heart_rate": self.generate_heart_rate(),
            "blood_pressure": self.generate_blood_pressure(),
            "blood_oxygen": self.generate_blood_oxygen(),
            "status": "normal"
        }
        
        # 添加简单的状态判断
        if data["heart_rate"] > 100 or data["heart_rate"] < 60:
            data["status"] = "abnormal_heart_rate"
        if data["blood_oxygen"] < 95:
            data["status"] = "abnormal_blood_oxygen"
        
        return data

def simulate_real_time_data(duration_seconds=None, interval=1):
    """实时模拟数据生成器"""
    simulator = HealthDataSimulator()
    start_time = time.time()
    
    try:
        while True:
            # 生成数据
            health_data = simulator.generate_health_data()
            
            # 转换为JSON并打印
            print(json.dumps(health_data, indent=2))
            
            # 检查是否达到指定持续时间
            if duration_seconds and (time.time() - start_time) >= duration_seconds:
                break
                
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n模拟器已停止")

if __name__ == "__main__":
    print("开始模拟健康数据生成 (按 Ctrl+C 停止)...")
    # 模拟运行60秒，每秒生成一次数据
    simulate_real_time_data(duration_seconds=60, interval=1)