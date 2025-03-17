import os
import openai
from dotenv import load_dotenv

SYSTEM_MESSAGE = """You are a professional healthcare and sports medicine expert who specializes in real-time exercise monitoring.

Core Guidelines:
1. Monitor vital signs and performance metrics
2. Provide instant safety assessments
3. Give personalized exercise guidance
4. Use clear, actionable language
5. Focus on athlete safety and performance

Exercise Reference Ranges:
• Heart Rate Zones:
- Zone 1 (50-60%): Warm-up
- Zone 2 (60-70%): Fat burn
- Zone 3 (70-80%): Aerobic
- Zone 4 (80-90%): Anaerobic
- Zone 5 (90-100%): Maximum

• Blood Pressure Response:
- Normal exercise increase: +20-40/+10-20 mmHg
- Warning levels: >180/120 mmHg

• Other Metrics:
- SpO2: Should stay >95%
- RPE: 6-20 scale (Borg)
"""

def get_llm_response(prompt, system_message=SYSTEM_MESSAGE):
    """
    Get LLM model response
    
    Args:
        prompt (str): user input
        system_message (str): system prompt
    
    Returns:
        str: LLM output
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
    """Generate exercise analysis prompt"""
    
    # Calculate training zone percentage
    max_hr = 220 - 30  # Assuming 30 years old
    hr_percentage = round((data['heart_rate'] / max_hr) * 100)
    
    prompt = f"""
    REAL-TIME EXERCISE MONITORING DATA:

    Timestamp: {data['timestamp']}

    VITAL SIGNS:
    ❤️ Heart Rate: {data['heart_rate']} bpm ({hr_percentage}% of max)
    🩺 Blood Pressure: {data['blood_pressure']['systolic']}/{data['blood_pressure']['diastolic']} mmHg
    🫁 SpO2: {data['blood_oxygen']}%

    PERFORMANCE METRICS:
    ⚡ Pace: {data['performance']['pace']} min/km
    📏 Distance: {data['performance']['distance']} km
    🔥 Calories: {data['performance']['calories']} kcal

    ENVIRONMENTAL:
    🌡️ Temperature: {data['environment']['temperature']}°C
    💧 Humidity: {data['environment']['humidity']}%

    Please provide a QUICK STATUS REPORT:

    1. SAFETY STATUS:
    - Current training zone
    - Key vitals assessment
    - Any immediate concerns

    2. PERFORMANCE UPDATE:
    - Exercise intensity evaluation
    - Effort vs. capacity
    - Progress indicators

    3. ACTION ITEMS:
    - Immediate adjustments needed
    - Next steps recommendation
    - Safety precautions if any

    Format: Keep response under 100 words, prioritize safety alerts, use clear directives.
    """
    return prompt

def main():
    # 示例调用
    prompt = "Hello"
    response = get_llm_response(prompt)
    print(response)

if __name__ == "__main__":
    main()