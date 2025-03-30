import random
import time
import json
from datetime import datetime

class HealthDataSimulator:
    def __init__(self):
        # Basic physiological data
        self.base_heart_rate = 75
        self.base_blood_pressure_systolic = 120
        self.base_blood_pressure_diastolic = 80
        self.base_blood_oxygen = 98
        
        # Exercise performance data
        self.base_pace = 6.0  # pace (minutes/kilometer)
        self.base_stride = 0.8  # stride length (meters)
        self.base_cadence = 160  # steps per minute
        
        # Environmental data
        self.base_altitude = 50 
        self.base_temperature = 25
        self.base_pressure = 1013
        self.base_humidity = 60
        
        # Exercise intensity and cumulative data
        self.exercise_duration = 0
        self.total_distance = 0
        self.calories_burned = 0
        
        self.abnormal_probability = 0.1

        self.data_history = []
        self.max_history = 10  # store last 10 records

    def generate_performance_data(self):
        """Generate exercise performance data"""
        pace = round(self.base_pace + random.uniform(-1, 1), 2)
        stride = round(self.base_stride + random.uniform(-0.1, 0.1), 2)
        cadence = round(self.base_cadence + random.uniform(-10, 10))
        
        # Update cumulative data
        self.exercise_duration += 1/60  # add 1 second each update
        distance_delta = (1000/pace)/60  # distance moved per second
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
        
        # Adjust physiological data based on exercise duration
        exercise_factor = min(self.exercise_duration / 30, 1)  # max intensity at 30 minutes
        hr_adjustment = 40 * exercise_factor  # max increase of 40bpm
        
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
        
        # Status assessment
        if (heart_rate > 160 or blood_oxygen < 95):
            data["status"] = "warning"
        if (heart_rate > 180 or blood_oxygen < 90):
            data["status"] = "critical"

        # Add validation before storing or returning data
        is_valid, message = self.validate_health_data(data)
        if not is_valid:
            print(f"Warning: {message}")
            # Could add logic to regenerate data or adjust values

        # Add data to history
        self.data_history.append(data)
        if len(self.data_history) > self.max_history:
            self.data_history.pop(0)
            
        return data
    
    def validate_health_data(self, data):
        """
        Validate health data is within acceptable ranges
        Returns: (is_valid, message)
        """
        if not (40 <= data["heart_rate"] <= 200):
            return False, "Heart rate out of range"
        if not (85 <= data["blood_pressure"]["systolic"] <= 200):
            return False, "Systolic pressure out of range"
        # ============================================================
        # Add your code here 
        # Task1 : more validation rules
        # ============================================================
        return True, "Data valid"

def simulate_real_time_data(duration_seconds=None, interval=1):
    """Real-time data generator simulator"""
    simulator = HealthDataSimulator()
    start_time = time.time()
    
    try:
        while True:
            # Generate data
            health_data = simulator.generate_health_data()
            
            # Convert to JSON and print
            print(json.dumps(health_data, indent=2))
            
            # Check if specified duration has been reached
            if duration_seconds and (time.time() - start_time) >= duration_seconds:
                break
                
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nSimulator Stopped")


def simulate_workout_session(self, workout_plan):
    """
    workout_plan example:
    [
        ("warmup", 5),      # 5 minutes warmup
        ("running", 20),    # 20 minutes running
        ("cooldown", 5)     # 5 minutes cooldown
    ]
    """
    # ============================================================
    # Add your code here 
    # Task1: Create a method that simulates a complete workout session with different phases
    # ============================================================
    pass

if __name__ == "__main__":
    print("Simulation started (Press Ctrl+C to Stop)...")
    # Generate new data every 60 seconds
    simulate_real_time_data(duration_seconds=10, interval=1)