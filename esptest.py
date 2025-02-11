import streamlit as st
import cv2
import numpy as np

# ESP32-CAMのストリームURL (例: http://192.168.1.100:81/stream)
ESP32_CAM_URL = "http://192.168.10.113:81/stream"

st.title("ESP32-CAM Live Stream")

# ボタンでストリーミングの開始・停止を制御
if "stream" not in st.session_state:
    st.session_state["stream"] = False

if st.button("Start Stream"):
    st.session_state["stream"] = True

if st.button("Stop Stream"):
    st.session_state["stream"] = False

# 映像の取得と表示
if st.session_state["stream"]:
    # OpenCVでストリームを取得
    stream = cv2.VideoCapture(ESP32_CAM_URL)

    if not stream.isOpened():
        st.error("Failed to open the stream. Check the URL or network connection.")
    else:
        # 空の表示領域を作成
        frame_placeholder = st.empty()

        # ストリーミングを実行
        while st.session_state["stream"]:
            ret, frame = stream.read()
            if not ret:
                st.warning("Failed to retrieve frame. Retrying...")
                break

            # 映像の色変換 (BGRからRGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # フレームを表示領域に更新
            frame_placeholder.image(frame, channels="RGB")

        stream.release()
else:
    st.text("Stream stopped.")
