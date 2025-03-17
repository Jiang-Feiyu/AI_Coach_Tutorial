# AI Coach: Real-time Performance Analysis Using Wearable Sensors and LLM

## What is this program?
- An intelligent coaching system using wearable sensor data
- Create personalized real-time feedback
- Optimize training efficiency through AI-powered analysis

## Env setup
- Currently this program is using [SambaNova Cloud API] (`Meta-Llama-3.1-70B-Instruct`), you may need to register the SamabaNova account first and gain your personal API key.
- create & activate env: `conda create -n AIcoach Python=3.9.20`, `conda activate AIcoach`
- `pip install -r requirements.txt`
- Copy `.env.example` to `.env`, and substitute the `SAMBANOVA_API_KEY=""` with your own private key.

## Start the Program
- if you wanna script: `python main.py --mode terminal`
    ![图片描述](./img/image2.png)
- if you wanna UI: `python main.py --mode ui`
    ![图片描述](./img/image.png)

## Prompt
This prompt is designed for real-time exercise monitoring and analysis by a large language model (LLM). It combines current exercise data with trend analysis to provide actionable insights for athletes and coaches.
```
    prompt = f"""
    REAL-TIME EXERCISE DATA:
    Vitals: HR {data['heart_rate']}bpm, BP {data['blood_pressure']['systolic']}/{data['blood_pressure']['diastolic']}, SpO2 {data['blood_oxygen']}%
    Performance: {data['performance']['pace']} min/km, {data['performance']['distance']} km

    10-Record Trends:
    ❤️ HR: {trends['heart_rate_trend']}
    🩺 BP: {trends['blood_pressure_trend']}
    🫁 SpO2: {trends['blood_oxygen_trend']}
    ⚡ Pace: {trends['pace_trend']}

    Provide a 50-100 word analysis covering:
    1. Safety status & risks
    2. Performance trends
    3. Key recommendations

    Focus on critical changes and immediate action items. Be concise and direct.
    """
```
Design Principles：
- **Pre-processed Trends**: Instead of raw historical data, provides calculated trends (increasing, decreasing, stable) from the last 10 records, reducing token usage while maintaining essential information.
- **Clear Instructions**: Requests a specific word count and content structure to ensure consistent, actionable responses.
- **Focus on Relevance**: Directs the LLM to prioritize critical changes and immediate action items, avoiding verbose or generic responses.

System message
```
Design Principles：
- **Pre-processed Trends**: Instead of raw historical data, provides calculated trends (increasing, decreasing, stable) from the last 10 records, reducing token usage while maintaining essential information.
- **Clear Instructions**: Requests a specific word count and content structure to ensure consistent, actionable responses.
- **Focus on Relevance**: Directs the LLM to prioritize critical changes and immediate action items, avoiding verbose or generic responses.

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
```

[SambaNova Cloud API]:https://cloud.sambanova.ai/apis