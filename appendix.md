#### Core System Components

| Component | Key Functions | Description |
|-----------|--------------|-------------|
| **Data Management** | `initialize_session_state()` | Sets up application state variables for metrics, history, and UI settings |
| | `update_history()` | Updates time-series data for visualization with 100-point rolling window |
| | `save_data_to_csv()` | Persists health metrics to CSV files with metadata and timestamps |
| **Visualization** | `create_metrics_chart()` | Generates multi-panel Plotly charts for vital signs, performance metrics, and environmental conditions |
| **AI Feedback** | `analyze_health_data()` | Prepares contextual prompts for LLM based on current and historical data |
| | `get_llm_response()` | Retrieves AI-generated coaching feedback about exercise performance |
| **Voice Features** | `text_to_speech()` | Converts AI feedback to spoken audio using Web Speech API |
| **Health Simulation** | `HealthDataSimulator` | Simulates realistic physiological responses with personalized baselines |
| **Data Storage** | CSV Management | Stores exercise data in structured format with timestamps and metrics |

#### Implementation Details

| Component | Features | Description |
|-----------|----------|-------------|
| **Health Data Simulator** | Baseline Metrics | Establishes personalized resting heart rate, blood pressure baselines |
| | Exercise Progression | Incrementally increases duration and intensity |
| | Physiological Response | Adjusts responses with randomization for realism |
| | Data Generation | Regular interval comprehensive data point creation |
| | Status Monitoring | Maintains normal/warning/critical status flags |
| **Visualization Dashboard** | Vital Signs Panel | Real-time heart rate and blood oxygen monitoring |
| | Blood Pressure Panel | Dynamic systolic and diastolic readings |
| | Performance Panel | Live pace, distance, and calorie tracking |
| | Environmental Panel | Temperature and humidity visualization |
| **Data Management** | Session State | Initializes and maintains application variables |
| | History Tracking | Maintains 100-entry rolling window |
| | Data Persistence | Automatic CSV storage with timestamps |
| | Data Structure | Hierarchical JSON organization |
| **AI Feedback** | Prompt Generation | Creates context-aware prompts from current/historical data |
| | LLM Processing | Integration with Meta-Llama-3.1-70B-Instruct |
| | Response Formatting | Human-readable coaching advice |
| | Priority System | Status-based feedback urgency |
| **Voice Features** | Speech Conversion | Web Speech API integration |
| | Control Options | Manual and automatic feedback modes |
| | Alert System | Audible notifications for critical conditions |

#### Base Physiological Parameters

| Parameter | Value | Unit | Description |
|-----------|-------|------|-------------|
| `base_heart_rate` | 75 | bpm | Resting heart rate |
| `base_blood_pressure_systolic` | 120 | mmHg | Resting systolic blood pressure |
| `base_blood_pressure_diastolic` | 80 | mmHg | Resting diastolic blood pressure |
| `base_blood_oxygen` | 98 | % | Resting blood oxygen saturation |

#### Performance Parameters

| Parameter | Value | Unit | Description |
|-----------|-------|------|-------------|
| `base_pace` | 6.0 | min/km | Base running/walking pace |
| `base_stride` | 0.8 | m | Base stride length |
| `base_cadence` | 160 | steps/min | Base step frequency |

#### Environmental Parameters

| Parameter | Value | Unit | Description |
|-----------|-------|------|-------------|
| `base_altitude` | 50 | m | Base altitude |
| `base_temperature` | 25 | °C | Base environmental temperature |
| `base_pressure` | 1013 | hPa | Base atmospheric pressure |
| `base_humidity` | 60 | % | Base humidity level |

#### Exercise Parameters

| Parameter | Initial Value | Unit | Description |
|-----------|---------------|------|-------------|
| `exercise_duration` | 0 | min | Duration of exercise (increments during simulation) |
| `total_distance` | 0 | km | Total distance covered (accumulates during simulation) |
| `calories_burned` | 0 | kcal | Total calories burned (accumulates during simulation) |

#### Status Thresholds

| Status | Condition |
|--------|-----------|
| `normal` | Default status |
| `warning` | Heart rate > 160 bpm OR Blood oxygen < 95% |
| `critical` | Heart rate > 180 bpm OR Blood oxygen < 90% |

#### Physiological Adjustments During Exercise
| Parameter | Adjustment Formula | Max Change | 
|-----------|-------------------|------------| 
| Heart Rate | `base + (40 * exercise_factor) + random(-10, 10)` | +40 bpm | 
| Systolic BP | `base + (20 * exercise_factor) + random(-10, 10)` | +20 mmHg | 
| Diastolic BP | `base + (10 * exercise_factor) + random(-5, 5)` | +10 mmHg | 
| Blood Oxygen | `base - exercise_factor + random(-1, 1)` | -1%

#### Data Structure

```json
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "heart_rate": 75,
  "blood_pressure": {
    "systolic": 120,
    "diastolic": 80
  },
  "blood_oxygen": 98.0,
  "performance": {
    "pace": 6.0,
    "stride": 0.8,
    "cadence": 160,
    "duration": 0.0,
    "distance": 0.0,
    "calories": 0.0
  },
  "environment": {
    "altitude": 50,
    "temperature": 25.0,
    "pressure": 1013,
    "humidity": 60
  },
  "status": "normal"
}
```

#### Prompt Template
Exercise analysis template
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