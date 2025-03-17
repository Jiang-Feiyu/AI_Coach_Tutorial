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
            # 修改这里，传入历史数据
            prompt = analyze_health_data(health_data, simulator.data_history)
            response = get_llm_response(prompt)
            
            print("\nCurrent Health Data:")
            print(json.dumps(health_data, indent=2))
            print("\nAI Coach Analysis:")
            print(response)
            print("\nWaiting 30 seconds...")
            time.sleep(30)
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