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
- if you wanna UI: `python main.py --mode ui`
    ![图片描述](./img/image.png)

[SambaNova Cloud API]:https://cloud.sambanova.ai/apis