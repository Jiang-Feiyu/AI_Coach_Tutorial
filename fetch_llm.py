import os
import openai
from dotenv import load_dotenv
# Setting the environment variable
os.environ["SYSTEM_MESSAGE"] = """You are a professional healthcare and sports medicine expert who specializes in real-time exercise monitoring.

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

os.environ["EXERCISE_ANALYSIS_TEMPLATE"] = """
REAL-TIME EXERCISE DATA:
Vitals: HR {heart_rate}bpm, BP {systolic}/{diastolic}, SpO2 {blood_oxygen}%
Performance: {pace} min/km, {distance} km

10-Record Trends:
❤️ HR: {heart_rate_trend}
🩺 BP: {blood_pressure_trend}
🫁 SpO2: {blood_oxygen_trend}
⚡ Pace: {pace_trend}

Provide a 50-100 word analysis covering:
1. Safety status & risks
2. Performance trends
3. Key recommendations

Focus on critical changes and immediate action items. Be concise and direct.
"""

# Reading the environment variable
system_message = os.environ.get("SYSTEM_MESSAGE")

def get_llm_response(prompt, system_message=system_message):
    """Get LLM model response"""
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

def analyze_trends(data_history):
    if not data_history:
        return {}
        
    trends = {
        "heart_rate": [],
        "blood_pressure_systolic": [],
        "blood_pressure_diastolic": [],
        "blood_oxygen": [],
        "pace": [],
        "distance": [],
        "calories": []
    }
    
    for data in data_history:
        trends["heart_rate"].append(data["heart_rate"])
        trends["blood_pressure_systolic"].append(data["blood_pressure"]["systolic"])
        trends["blood_pressure_diastolic"].append(data["blood_pressure"]["diastolic"])
        trends["blood_oxygen"].append(data["blood_oxygen"])
        trends["pace"].append(data["performance"]["pace"])
        trends["distance"].append(data["performance"]["distance"])
        trends["calories"].append(data["performance"]["calories"])
    
    def calculate_trend(values):
        if len(values) < 2:
            return "stable"
        diff = values[-1] - values[0]
        if abs(diff) < 0.05 * values[0]: 
            return "stable"
        return "increasing" if diff > 0 else "decreasing"
    
    return {
        "heart_rate_trend": calculate_trend(trends["heart_rate"]),
        "blood_pressure_trend": calculate_trend(trends["blood_pressure_systolic"]),
        "blood_oxygen_trend": calculate_trend(trends["blood_oxygen"]),
        "pace_trend": calculate_trend(trends["pace"]),
        "performance_trend": calculate_trend(trends["distance"])
    }

def analyze_health_data(data, data_history):
    """Generate exercise analysis prompt with trend analysis"""
    trends = analyze_trends(data_history)
    
    prompt_template = os.environ.get("EXERCISE_ANALYSIS_TEMPLATE")
    
    formatted_prompt = prompt_template.format(
        heart_rate=data["heart_rate"],
        systolic=data["blood_pressure"]["systolic"],
        diastolic=data["blood_pressure"]["diastolic"],
        blood_oxygen=data["blood_oxygen"],
        pace=data["performance"]["pace"],
        distance=data["performance"]["distance"],
        heart_rate_trend=trends["heart_rate_trend"],
        blood_pressure_trend=trends["blood_pressure_trend"],
        blood_oxygen_trend=trends["blood_oxygen_trend"],
        pace_trend=trends["pace_trend"]
    )
    
    return formatted_prompt

def main():
    prompt = "Hello"
    response = get_llm_response(prompt)
    print(response)

if __name__ == "__main__":
    main()