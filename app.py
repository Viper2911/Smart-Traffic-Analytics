import streamlit as st
import tempfile
import os
from core.tracker import process_traffic_stream

st.set_page_config(page_title="Traffic Analytics Hub", layout="wide")
st.title("🚦 Smart City Traffic Density & Speed Analyzer")

uploaded_video = st.file_uploader("Upload Traffic Video (MP4, AVI)", type=['mp4', 'avi'])

if uploaded_video is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_video.read())
    video_path = tfile.name
    model_path = os.path.join('model', 'best.pt') 

    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Live Tracking Feed")
        video_placeholder = st.empty() 
        
    with col2:
        st.subheader("Live Metrics")
        metric_left = st.empty()
        metric_right = st.empty()
        status_left = st.empty()
        status_right = st.empty()
        
    if st.button("Start Traffic Analysis", type="primary"):
        if not os.path.exists(model_path):
            st.error("Model weights not found! Place 'best.pt' inside the 'model/' directory.")
        else:
            with st.spinner('Initializing AI Tracking Engine...'):
                for frame, left_count, right_count in process_traffic_stream(video_path, model_path):
                    video_placeholder.image(frame, channels="RGB", use_container_width=True)
                    metric_left.metric("Vehicles (Left Lane)", left_count)
                    metric_right.metric("Vehicles (Right Lane)", right_count)
                    
                    left_intensity = "🔴 Heavy Congestion" if left_count > 10 else "🟢 Smooth Flow"
                    right_intensity = "🔴 Heavy Congestion" if right_count > 10 else "🟢 Smooth Flow"
                    
                    status_left.info(f"Left Lane Status: **{left_intensity}**")
                    status_right.info(f"Right Lane Status: **{right_intensity}**")
                    
    try:
        os.unlink(video_path)
    except Exception:
        pass