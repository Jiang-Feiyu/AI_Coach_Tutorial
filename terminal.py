import random
import time
import json
from datetime import datetime

class HealthDataSimulator:
    def __init__(self):
        # 基础生理数据
        self.base_heart_rate = 75
        self.base_blood_pressure_systolic = 120
        self.base_blood_pressure_diastolic = 80
        self.base_blood_oxygen = 98
        
        # 运动表现数据
        self.base_pace = 6.0  # 配速(分钟/公里)
        self.base_stride = 0.8  # 步幅(米)
        self.base_cadence = 160  # 步频(步/分钟)
        
        # 环境数据
        self.base_altitude = 50  # 海拔(米)
        self.base_temperature = 25  # 温度(摄氏度)
        self.base_pressure = 1013  # 气压(百帕)
        self.base_humidity = 60  # 湿度(%)
        
        # 运动强度和累计数据
        self.exercise_duration = 0  # 运动时长(分钟)
        self.total_distance = 0  # 总距离(公里)
        self.calories_burned = 0  # 消耗卡路里
        
        self.abnormal_probability = 0.1

        self.data_history = []
        self.max_history = 10  # 保存最近10条记录

    def generate_performance_data(self):
        """生成运动表现数据"""
        pace = round(self.base_pace + random.uniform(-1, 1), 2)
        stride = round(self.base_stride + random.uniform(-0.1, 0.1), 2)
        cadence = round(self.base_cadence + random.uniform(-10, 10))
        
        # 更新累计数据
        self.exercise_duration += 1/60  # 每次更新增加1秒
        distance_delta = (1000/pace)/60  # 每秒移动的距离
        self.total_distance = round(self.total_distance + distance_delta/1000, 3)
        self.calories_burned = round(self.calories_burned + random.uniform(0.1, 0.2), 1)
        
        return {
            "pace": pace,
            "stride": stride,
            "cadence": cadence,
            "duration": round(self.exercise_duration, 2),
            "distance": self.total_distance,
            "calories": self.calories_burned
        }

    def generate_environmental_data(self):
        """生成环境数据"""
        return {
            "altitude": round(self.base_altitude + random.uniform(-5, 5)),
            "temperature": round(self.base_temperature + random.uniform(-1, 1), 1),
            "pressure": round(self.base_pressure + random.uniform(-5, 5)),
            "humidity": round(self.base_humidity + random.uniform(-5, 5))
        }

    def generate_health_data(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 根据运动时长调整生理数据基准
        exercise_factor = min(self.exercise_duration / 30, 1)  # 30分钟达到最大强度
        hr_adjustment = 40 * exercise_factor  # 最多增加40bpm
        
        heart_rate = round(self.base_heart_rate + hr_adjustment + random.uniform(-10, 10))
        blood_pressure = {
            "systolic": round(self.base_blood_pressure_systolic + 20 * exercise_factor + random.uniform(-10, 10)),
            "diastolic": round(self.base_blood_pressure_diastolic + 10 * exercise_factor + random.uniform(-5, 5))
        }
        blood_oxygen = round(self.base_blood_oxygen - exercise_factor + random.uniform(-1, 1), 1)

        data = {
            "timestamp": timestamp,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "blood_oxygen": blood_oxygen,
            "performance": self.generate_performance_data(),
            "environment": self.generate_environmental_data(),
            "status": "normal"
        }
        
        # 状态判断
        if (heart_rate > 160 or blood_oxygen < 95):
            data["status"] = "warning"
        if (heart_rate > 180 or blood_oxygen < 90):
            data["status"] = "critical"

        # 添加数据到历史记录
        self.data_history.append(data)
        if len(self.data_history) > self.max_history:
            self.data_history.pop(0)
            
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
    simulate_real_time_data(duration_seconds=10, interval=1)