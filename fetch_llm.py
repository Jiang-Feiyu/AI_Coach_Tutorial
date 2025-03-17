import os
import openai
from dotenv import load_dotenv

SYSTEM_MESSAGE = """You are a professional healthcare assistant with expertise in monitoring and analyzing vital signs. 
You should:
1. Analyze the vital signs data and provide a brief assessment
2. Point out any abnormal readings and potential health risks
3. Give personalized health suggestions
4. Use bullet points for better readability
5. Keep responses clear and concise
6. Present information in a calm and professional manner

Reference ranges:
- Heart rate: 60-100 bpm (normal resting)
- Blood pressure: 90-120/60-80 mmHg (ideal)
- Blood oxygen: 95-100% (normal)
"""

def get_llm_response(prompt, system_message=SYSTEM_MESSAGE):
    """
    获取LLM模型响应的函数
    
    Args:
        prompt (str): user input
        system_message (str): system prompt, default is "You are a helpful assistant"
    
    Returns:
        str: output of LLM
    """
    load_dotenv()
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.sambanova.ai/v1",
    )
    
    response = client.chat.completions.create(
        model="Meta-Llama-3.1-70B-Instruct",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        top_p=0.1
    )
    
    return response.choices[0].message.content

def analyze_health_data(data):
    """根据健康数据生成分析提示"""
    prompt = f"""
    Please analyze the following real-time exercise vital signs data:

    Time: {data['timestamp']}
    Heart Rate: {data['heart_rate']} bpm
    Blood Pressure: {data['blood_pressure']['systolic']}/{data['blood_pressure']['diastolic']} mmHg
    Blood Oxygen: {data['blood_oxygen']}%
    
    Context: This is real-time monitoring data during exercise/physical activity.
    
    Please provide:
    1. Quick assessment of vital signs during exercise
    2. Analysis of each measurement considering exercise intensity:
       - Heart rate zones (aerobic/anaerobic)
       - Blood pressure response to exercise
       - Blood oxygen levels during activity
    3. Any concerning patterns or readings for exercise conditions
    4. Exercise-specific recommendations:
       - Whether to maintain/adjust exercise intensity
       - Recovery suggestions
       - Hydration and rest recommendations
    5. Whether to stop exercise and seek medical attention
    
    Training Safety Guidelines:
    - Target heart rate zone: 50-85% of max heart rate
    - Expected BP increase during exercise: systolic +20-40 mmHg
    - Blood oxygen should remain stable even during exercise
    
    Note: Focus on exercise safety and performance optimization.
    """
    return prompt

def main():
    # 示例调用
    prompt = "Hello"
    response = get_llm_response(prompt)
    print(response)

if __name__ == "__main__":
    main()