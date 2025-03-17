from fetch_llm import get_llm_response, analyze_health_data
from terminal import simulate_real_time_data, HealthDataSimulator
import json
import time
from datetime import datetime

def main():
    simulator = HealthDataSimulator()
    
    try:
        while True:
            # 生成健康数据
            health_data = simulator.generate_health_data()
            print("\n当前健康数据：")
            print(json.dumps(health_data, indent=2))

            # 生成分析提示并获取LLM响应
            prompt = analyze_health_data(health_data)
            print("\nLLM分析结果：")
            response = get_llm_response(prompt)
            print(response)

            # 等待5秒后继续
            print("\n5秒后生成新数据...")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main()