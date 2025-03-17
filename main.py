from fetch_llm import get_llm_response, analyze_health_data
from terminal import simulate_real_time_data, HealthDataSimulator
import json
import time
from datetime import datetime
import argparse
import subprocess
import sys

def run_terminal_mode(simulator):
    """在终端模式下运行"""
    try:
        while True:
            health_data = simulator.generate_health_data()
            
            # 显示当前数据
            print("\nCurrent Health Data:")
            print(json.dumps(health_data, indent=2))
            
            # 显示历史数据列表
            if len(simulator.data_history) > 1:
                print("\n=== Historical Data (Last 5 records) ===")
                
                # 取最近的10条记录(如果有的话)
                recent_history = simulator.data_history[-10:] if len(simulator.data_history) >= 10 else simulator.data_history
                
                # 打印每条历史记录的关键信息
                for i, record in enumerate(recent_history):
                    print(f"\nRecord {i+1} - {record['timestamp']}:")
                    print(f"  HR: {record['heart_rate']} bpm | BP: {record['blood_pressure']['systolic']}/{record['blood_pressure']['diastolic']} | SpO2: {record['blood_oxygen']}%")
                    print(f"  Pace: {record['performance']['pace']:.2f} min/km | Distance: {record['performance']['distance']:.3f} km")
                
                # 显示历史数据趋势
                print("\n=== Trend Analysis ===")
                from fetch_llm import analyze_trends
                trends = analyze_trends(simulator.data_history)
                
                print(f"❤️ Heart Rate Trend: {trends['heart_rate_trend']}")
                print(f"🩺 Blood Pressure Trend: {trends['blood_pressure_trend']}")
                print(f"🫁 Blood Oxygen Trend: {trends['blood_oxygen_trend']}")
                print(f"⚡ Pace Trend: {trends['pace_trend']}")
                print(f"📈 Overall Performance Trend: {trends['performance_trend']}")
            
            # 传入历史数据获取AI分析
            prompt = analyze_health_data(health_data, simulator.data_history)
            response = get_llm_response(prompt)
            
            print("\nAI Coach Analysis:")
            print(response)
            print("\nWaiting 10 seconds...")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nProgram stopped")

def run_ui_mode():
    """启动UI模式"""
    try:
        subprocess.run(["streamlit", "run", "ui.py"])
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install it using 'pip install streamlit'")
        sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Exercise Monitoring System')
    parser.add_argument('--mode', type=str, choices=['terminal', 'ui'], 
                       default='ui', help='Run mode: terminal or ui')
    args = parser.parse_args()
    
    if args.mode == 'terminal':
        simulator = HealthDataSimulator()
        run_terminal_mode(simulator)
    else:
        run_ui_mode()

if __name__ == "__main__":
    main()