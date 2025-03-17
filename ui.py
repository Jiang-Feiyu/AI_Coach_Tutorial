import streamlit as st
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import streamlit as st
import time
from terminal import simulate_real_time_data, HealthDataSimulator
from fetch_llm import get_llm_response, analyze_health_data
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def main():
    st.set_page_config(page_title="Exercise Monitor", layout="wide")
    
    initialize_session_state()
    
    st.title("🏃‍♂️ Real-time Exercise Monitor")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        chart_placeholder = st.empty()
    
    with col2:
        # 为当前指标创建空占位符
        metrics_placeholder = st.empty()
        # 为分析结果创建空占位符
        analysis_placeholder = st.empty()
    
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
        
        # 更新分析
        prompt = analyze_health_data(data)
        analysis = get_llm_response(prompt)
        
        # 使用空占位符更新分析结果
        with analysis_placeholder.container():
            st.subheader("💡 AI Coach Feedback")
            st.markdown(f"**Latest Update ({data['timestamp']}):**")
            st.markdown(analysis)
        
        time.sleep(10)

if __name__ == "__main__":
    main()