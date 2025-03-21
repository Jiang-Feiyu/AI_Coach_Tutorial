import streamlit as st
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import csv
from pathlib import Path
from terminal import simulate_real_time_data, HealthDataSimulator
from fetch_llm import get_llm_response, analyze_health_data

# 添加保存数据到CSV的函数
def save_data_to_csv(health_data, csv_path="./data/data.csv"):
    """
    将健康数据保存到CSV文件
    
    参数:
        health_data (dict): 包含健康数据的字典
        csv_path (str): CSV文件保存路径
    """
    # 确保目录存在
    directory = os.path.dirname(csv_path)
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    # 将嵌套字典扁平化为一维字典
    flat_data = {
        "timestamp": health_data["timestamp"],
        "heart_rate": health_data["heart_rate"],
        "blood_pressure_systolic": health_data["blood_pressure"]["systolic"],
        "blood_pressure_diastolic": health_data["blood_pressure"]["diastolic"],
        "blood_oxygen": health_data["blood_oxygen"],
        "pace": health_data["performance"]["pace"],
        "stride": health_data["performance"]["stride"],
        "cadence": health_data["performance"]["cadence"],
        "duration": health_data["performance"]["duration"],
        "distance": health_data["performance"]["distance"],
        "calories": health_data["performance"]["calories"],
        "altitude": health_data["environment"]["altitude"],
        "temperature": health_data["environment"]["temperature"],
        "pressure": health_data["environment"]["pressure"],
        "humidity": health_data["environment"]["humidity"],
        "status": health_data["status"]
    }
    
    # 检查文件是否存在
    file_exists = os.path.isfile(csv_path)
    
    # 写入CSV
    with open(csv_path, mode='a', newline='') as file:
        fieldnames = flat_data.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writeheader()
        
        # 写入数据行
        writer.writerow(flat_data)
    
    return csv_path

def initialize_session_state():
    """初始化Session State"""
    if 'history' not in st.session_state:
        st.session_state.history = {
            'timestamp': [],
            'heart_rate': [],
            'blood_oxygen': [],
            'systolic': [],
            'diastolic': [],
            'pace': [],
            'distance': [],
            'calories': [],
            'temperature': [],
            'humidity': []
        }
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = "Waiting for data..."
    if 'simulator' not in st.session_state:
        st.session_state.simulator = HealthDataSimulator()
    if 'csv_path' not in st.session_state:
        st.session_state.csv_path = "./data/data.csv"
    if 'save_data' not in st.session_state:
        st.session_state.save_data = True
    # 添加语音反馈相关的状态
    if 'auto_read_feedback' not in st.session_state:
        st.session_state.auto_read_feedback = False
    if 'last_read_feedback' not in st.session_state:
        st.session_state.last_read_feedback = ""
    # 添加一个计数器用于生成唯一的键
    if 'button_counter' not in st.session_state:
        st.session_state.button_counter = 0

def update_history(data):
    """更新历史数据"""
    history = st.session_state.history
    history['timestamp'].append(data['timestamp'])
    history['heart_rate'].append(data['heart_rate'])
    history['blood_oxygen'].append(data['blood_oxygen'])
    history['systolic'].append(data['blood_pressure']['systolic'])
    history['diastolic'].append(data['blood_pressure']['diastolic'])
    history['pace'].append(data['performance']['pace'])
    history['distance'].append(data['performance']['distance'])
    history['calories'].append(data['performance']['calories'])
    history['temperature'].append(data['environment']['temperature'])
    history['humidity'].append(data['environment']['humidity'])
    
    # 保持历史记录在最近100个数据点
    if len(history['timestamp']) > 100:
        for key in history:
            history[key] = history[key][-100:]
    
    # 保存数据到CSV
    if st.session_state.save_data:
        save_data_to_csv(data, st.session_state.csv_path)

def create_metrics_chart():
    """创建实时指标图表"""
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Vital Signs', 'Blood Pressure', 
                       'Performance', 'Progress',
                       'Environment', 'Status')
    )

    history = st.session_state.history
    
    # 心率和血氧
    fig.add_trace(
        go.Scatter(y=history['heart_rate'], name="Heart Rate",
                  line=dict(color='red')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(y=history['blood_oxygen'], name="SpO2",
                  line=dict(color='blue')),
        row=1, col=1
    )

    # 血压
    fig.add_trace(
        go.Scatter(y=history['systolic'], name="Systolic",
                  line=dict(color='orange')),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(y=history['diastolic'], name="Diastolic",
                  line=dict(color='green')),
        row=1, col=2
    )

    # 配速和距离
    fig.add_trace(
        go.Scatter(y=history['pace'], name="Pace",
                  line=dict(color='purple')),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(y=history['distance'], name="Distance",
                  line=dict(color='brown')),
        row=2, col=2
    )

    # 温度和湿度
    fig.add_trace(
        go.Scatter(y=history['temperature'], name="Temperature",
                  line=dict(color='red')),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(y=history['humidity'], name="Humidity",
                  line=dict(color='blue')),
        row=3, col=2
    )
    
    fig.update_layout(height=800, showlegend=True)
    return fig

# 添加语音播报功能
def text_to_speech(text):
    """
    将文本转换为语音并在网页中播放
    
    参数:
        text (str): 需要播放的文本
    """
    # 使用HTML的audio元素和Web Speech API
    speech_js = f"""
    <script>
        function speak() {{
            const utterance = new SpeechSynthesisUtterance(`{text}`);
            speechSynthesis.speak(utterance);
        }}
        speak();
    </script>
    """
    # 使用Streamlit组件来注入JavaScript
    st.components.v1.html(speech_js, height=0)

def main():
    st.set_page_config(page_title="Exercise Monitor", layout="wide")
    
    initialize_session_state()
    
    st.title("🏃‍♂️ Real-time Exercise Monitor")
    
    # 添加侧边栏设置
    with st.sidebar:
        st.header("Settings")
        st.session_state.save_data = st.checkbox("Save data to CSV", value=True)
        
        # 添加语音反馈设置
        st.subheader("Voice Feedback Settings")
        st.session_state.auto_read_feedback = st.checkbox("Auto-read AI Coach Feedback", 
                                                         value=st.session_state.auto_read_feedback,
                                                         key="auto_read_checkbox")
        
        if st.session_state.save_data:
            # 允许用户自定义CSV文件路径
            custom_path = st.text_input("CSV file path", value=st.session_state.csv_path)
            if custom_path != st.session_state.csv_path:
                st.session_state.csv_path = custom_path
            
            # 显示当前CSV文件路径和状态
            csv_file = Path(st.session_state.csv_path)
            if csv_file.exists():
                st.success(f"Saving data to: {st.session_state.csv_path}")
                
                # 添加查看数据选项
                if st.button("View Saved Data", key="view_data_button"):
                    try:
                        import pandas as pd
                        df = pd.read_csv(st.session_state.csv_path)
                        st.dataframe(df.tail(10))
                        st.download_button(
                            label="Download CSV",
                            data=open(st.session_state.csv_path, 'rb').read(),
                            file_name="exercise_data.csv",
                            mime="text/csv",
                            key="download_button"
                        )
                    except Exception as e:
                        st.error(f"Error reading CSV: {e}")
            else:
                st.info(f"Will create: {st.session_state.csv_path} when data is generated")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        chart_placeholder = st.empty()
    
    with col2:
        # 为当前指标创建空占位符
        metrics_placeholder = st.empty()
        # 为分析结果创建空占位符
        analysis_placeholder = st.empty()
        # 为语音播报按钮创建空占位符
        speech_button_placeholder = st.empty()
    
    # 主循环
    while True:
        # 生成新数据
        data = st.session_state.simulator.generate_health_data()
        update_history(data)
        
        # 更新图表
        with chart_placeholder:
            st.plotly_chart(create_metrics_chart(), use_container_width=True)
        
        # 更新指标 - 使用占位符
        with metrics_placeholder.container():
            st.subheader("📊 Current Metrics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Heart Rate", f"{data['heart_rate']} bpm")
                st.metric("Blood Oxygen", f"{data['blood_oxygen']}%")
                st.metric("Distance", f"{data['performance']['distance']:.2f} km")
            with col2:
                st.metric("Pace", f"{data['performance']['pace']:.1f} min/km")
                st.metric("Temperature", f"{data['environment']['temperature']}°C")
                st.metric("Humidity", f"{data['environment']['humidity']}%")
            
            # 添加数据保存状态提示
            if st.session_state.save_data:
                st.caption(f"✅ Data saved to {st.session_state.csv_path}")
        
        # 更新分析
        prompt = analyze_health_data(data, st.session_state.simulator.data_history)
        analysis = get_llm_response(prompt)
        
        # 使用空占位符更新分析结果
        with analysis_placeholder.container():
            st.subheader("💡 AI Coach Feedback")
            st.markdown(f"**Latest Update ({data['timestamp']}):**")
            st.markdown(analysis)
        
        # 递增按钮计数器以生成唯一key
        st.session_state.button_counter += 1
        button_key = f"read_feedback_{st.session_state.button_counter}"
        
        # 添加语音播报按钮 - 使用动态生成的唯一key
        with speech_button_placeholder.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔊 Read Feedback", key=button_key):
                    text_to_speech(analysis)
                    st.session_state.last_read_feedback = analysis
            with col2:
                if st.session_state.auto_read_feedback:
                    st.success("Auto-read enabled")
                    # 只有当分析内容发生变化时才自动播报
                    if analysis != st.session_state.last_read_feedback:
                        text_to_speech(analysis)
                        st.session_state.last_read_feedback = analysis
                else:
                    st.info("Auto-read disabled")
        
        time.sleep(10)

if __name__ == "__main__":
    main()