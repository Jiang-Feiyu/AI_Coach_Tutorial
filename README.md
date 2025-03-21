# AI Coach: Real-time Performance Analysis Using Wearable Sensors and LLM

Tutorial writhing Assignment

Author
- Jiang Feiyu <3035770800>
- Wu Jiaux <>

## Introduction

The integration of wearable sensors with artificial intelligence is revolutionizing fitness training and health monitoring. However, the gap between collecting sensor data and generating actionable insights remains a challenge for many developers and fitness enthusiasts. Traditional approaches often simply display raw metrics without contextual interpretation, limiting their practical value during exercise.

This tutorial addresses this challenge by demonstrating how to build an AI Coach system that processes physiological data from wearable sensors, analyzes patterns across multiple parameters, and delivers personalized, real-time feedback using Large Language Models (LLMs). By combining sensor data processing, visualization techniques, and natural language generation, we create a comprehensive coaching experience similar to having a knowledgeable personal trainer accompanying your workouts.

Our approach enables:
- Real-time monitoring of vital signs and performance metrics
- AI-powered interpretation of physiological data
- Personalized coaching feedback through both visual and voice interfaces
- Historical data analysis for long-term performance tracking

## Setup
1. **SambaNova Cloud API Configuration**:
   - Register for a SambaNova account at [cloud.sambanova.ai](https://cloud.sambanova.ai/apis)
   - Navigate to the API section and generate your personal API key
   - Store this key securely as it will be needed for LLM integration

2. **Python Environment Setup**:
  ```
  # Create and activate a new conda environment
  conda create -n AIcoach python=3.9.20
  conda activate AIcoach
   
  # Install required packages
  pip install -r requirements.txt
  ```

3. **Environment Variables Configuration**
  ```
  # Copy the example configuration file
  cp .env.example .env

  # Edit the .env file and add your SambaNova API key
  # SAMBANOVA_API_KEY="your-key-here"
  ```

## Demonstration
Our AI Coach system can be run in two modes:
- For headless or debugging purposes, the system can operate in terminal mode:
  ```
  python main.py --mode terminal
  ```
  In this mode, exercise data and AI feedback are displayed in the console, allowing for lightweight monitoring.
  ![图片描述](./img/image2.png)

- For a complete interactive experience, the UI mode provides comprehensive visualization and control: 
  ```
  python main.py --mode ui
  ```
  The UI mode features:
  - Real-time multi-panel charts
  - AI feedback display
  - Voice output controls
  - Settings configuration panel
  
  ![图片描述](./img/image.png)

  ![alt text](./img/image.1.png)

## Implementation
### Health Data Simulator Implementation
The simulator component allows us to test the system without actual wearable hardware by generating realistic physiological data based on exercise duration and intensity. Our implementation creates a comprehensive data structure including vital signs, performance metrics, and environmental conditions.

The simulator:
- Establishes personalized baseline metrics (resting heart rate, blood pressure, etc.)
- Incrementally increases exercise duration and intensity
- Adjusts physiological responses based on exercise factor with randomization for realism
- Generates comprehensive data points at regular intervals
- Maintains a status flag (normal, warning, critical) based on vital sign thresholds

### Visualization Dashboard Creation
The visualization engine creates real-time multi-panel charts using Plotly:
- **Vital Signs Panel**: Displays heart rate and blood oxygen saturation
- **Blood Pressure Panel**: Shows systolic and diastolic readings
- **Performance Metrics Panel**: Visualizes pace, distance, and calories burned
-** Environmental Panel**: Presents temperature and humidity conditions

All charts update dynamically as new data arrives, providing comprehensive exercise monitoring.

### Data Management Implementation
The data management component handles storage, retrieval, and maintenance of exercise metrics:
- **Session State Management**: Initializes and maintains application variables
- **History Tracking**: Updates a rolling window of recent data points (limited to 100 entries)
- **Data Persistence**: Automatically saves health metrics to CSV files with timestamps
- **Data Structure**: Organizes metrics in a hierarchical JSON structure for easy access

### AI Feedback Integration
The AI feedback component leverages SambaNova's LLM API to generate personalized coaching:
- **Contextual Prompt Generation**: Creates detailed prompts based on current and historical data
- **LLM Query Processing**: Sends data to the Meta-Llama-3.1-70B-Instruct model via API
- **Response Formatting**: Presents AI-generated advice in a readable format
- **Status-Based Prioritization**: Adjusts feedback urgency based on physiological status

### Voice Feedback Implementation
To enhance the coaching experience, we implement voice feedback:
- **Text-to-Speech Conversion**: Uses Web Speech API to vocalize AI insights
- **Feedback Control Options**: Includes both manual (button-triggered) and automatic reading
- **Status Notification**: Provides audible alerts for critical physiological conditions

## Core System Components
### Data Management
- `initialize_session_state()`: Sets up application state variables for metrics, history, and UI settings
- `update_history()`: Updates time-series data for visualization while maintaining a rolling window of 100 data points
- `save_data_to_csv()`: Persists health metrics to CSV files with comprehensive metadata and timestamps

### Visualization
- `create_metrics_chart()`: Generates multi-panel Plotly charts displaying vital signs, performance metrics, and environmental conditions in real-time

### AI Feedback
- `analyze_health_data()`: Prepares contextual prompts for the LLM based on current metrics and historical trends
- `get_llm_response()`: Retrieves AI-generated coaching feedback about exercise performance and health status

### Voice Features
- `text_to_speech()`:Converts AI feedback to spoken audio using Web Speech API
- Supports both manual triggering via button and automatic reading of new feedback

### Health Data Simulation
-  `HealthDataSimulator`: Establishes personalized baseline metrics and simulates realistic physiological responses
-  Incrementally adjusts exercise intensity and duration with appropriate metabolic responses
-  Generates comprehensive data points with natural variations for authentic training scenarios

### Data Storage
-   Exercise data is automatically saved to `./data/data.csv` by default
-   Custom storage location configurable through the UI settings panel
-   Structured CSV format includes timestamps, vital signs, performance metrics, and environmental data
-   Supports data export, visualization, and longitudinal analysis

## Practical Applications
The AI Coach system has several practical applications:

- Personal Fitness Training: Provides coaching when a human trainer isn't available
- Remote Health Monitoring: Allows healthcare providers to track patient exercise remotely
- Athletic Performance Optimization: Helps athletes fine-tune their training regimens
- Rehabilitation Support: Monitors progress during physical therapy and recovery
- Research Tool: Enables collection and analysis of exercise data for fitness studies

## Conclusion
This tutorial demonstrates how to bridge the gap between raw wearable sensor data and actionable insights through AI integration. By combining real-time data visualization with LLM-powered analysis, we've created a comprehensive coaching system that provides personalized guidance during exercise.

The modular architecture allows for easy extension to incorporate:
- Integration with commercial fitness wearables
- Additional physiological sensors
- Alternative LLM providers
- Custom training programs
- Advanced performance analytics

As wearable technology and AI continue to evolve, systems like AI Coach will play an increasingly important role in personal health management, athletic training, and clinical applications.

## FAQs
**Q: Can this system work with real wearable devices instead of simulated data?**

A: Yes. The Health Data Simulator can be replaced with API connections to commercial wearables or custom sensor implementations. The data structure would remain the same, allowing all other components to function without modification.

**Q: How can I customize the AI feedback for specific training programs?**

A: Modify the prompt templates in `.env` to include specific training parameters, goals, or restrictions. The LLM will then generate feedback tailored to these specialized requirements.

**Q: What are the hardware requirements for running this system?**

A: The system is designed to run on standard consumer hardware. For the UI mode, any modern computer with Python support is sufficient. The LLM processing occurs in the cloud via SambaNova's API, minimizing local computational requirements.

**Q: Can the system work offline?**

A: Partially. The data collection, visualization, and storage components can function offline. However, the AI feedback requires an internet connection to access the SambaNova Cloud API. A future enhancement could include a lightweight local model for basic offline analysis.

## Appendix
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


[SambaNova Cloud API]:https://cloud.sambanova.ai/apis