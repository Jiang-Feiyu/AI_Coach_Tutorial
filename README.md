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

- if you want to use UI mode: `python main.py --mode ui`
  - can configure data storage and audio output strategy in the settings panel .
    ![图片描述](./img/image.png)

    ![alt text](./img/image.1.png)

## Core Functions

### Data Management
- Sets up application state variables for metrics, history, and UI settings
- Updates time-series data for visualization while maintaining a rolling window of 100 data points
- Persists health metrics to CSV files with comprehensive metadata and timestamps

## Visualization
Generates multi-panel Plotly charts displaying vital signs, performance metrics, and environmental conditions in real-time

## AI Feedback
-  Prepares contextual prompts for the LLM based on current metrics and historical trends
- Retrieves AI-generated coaching feedback about exercise performance and health status

## Voice Features
- Converts AI feedback to spoken audio using Web Speech API
- Supports both manual triggering via button and automatic reading of new feedback

## Health Data Simulation
-  Establishes personalized baseline metrics and simulates realistic physiological responses
-  Incrementally adjusts exercise intensity and duration with appropriate metabolic responses
-  Generates comprehensive data points with natural variations for authentic training scenarios

## Data Storage
-   Exercise data is automatically saved to `./data/data.csv` by default
-   Custom storage location configurable through the UI settings panel
-   Structured CSV format includes timestamps, vital signs, performance metrics, and environmental data
-   Supports data export, visualization, and longitudinal analysis

### Appendix
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


[SambaNova Cloud API]:https://cloud.sambanova.ai/apis