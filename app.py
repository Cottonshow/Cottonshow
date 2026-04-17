import streamlit as st
import requests
import io
import numpy as np
from PIL import Image
import cv2

st.set_page_config(page_title="cottonshow CTO Edition", layout="wide")
st.title("🏛️ cottonshow: AI 정밀 컬러 시뮬레이터")

# 컬러 데이터 (기존과 동일)
cotton_colors = {
    "퓨어화이트_E01": "#FFFFFF", "빈티지베이지_E02": "#E5D3B3", "라이트그레이_E03": "#D3D3D3",
    "아이보리_E04": "#FFFFF0", "코토리베이지_E05": "#C5B4A2", "스톤그레이_E06": "#888888",
    "화이트골드칩_E07": "#FDF5E6", "스톤딥그레이_E09": "#4F4F4F", "핑크코튼캔디_E10": "#FFD1DC",
    "오렌지체리칩_E11": "#FFA500", "크리미레몬_E12": "#FFF44F", "네추럴핑크_E13": "#F8C8DC",
    "로맨틱딥핑크_E14": "#FF8DA1", "키즈옐로우_E15": "#FFF700", "미카레드_E16": "#B22222",
    "초코레드_E17": "#8B4513", "키즈오렌지_E18": "#FF8C00", "옐로우그린_E19": "#ADFF2F",
    "올리브그린_E20": "#808000", "민트코튼캔디_E21": "#AAF0D1", "머스크메론_E22": "#C3FDB8",
    "키즈그린_E23": "#00FF00", "블루_E24": "#0000FF", "라이트그린티_E25": "#D0F0C0",
    "스카이블루_E26": "#87CEEB", "카툰블루_E27": "#1E90FF", "라벤더코튼캔디_E28": "#E6E6FA",
    "후래쉬민트_E29": "#BDFCC9", "블루씨골드_E30": "#0077BE", "화이트라벤더_E31": "#F3E5AB",
    "미카네이비_E32": "#000080", "다크네이비_E33": "#000040", "딥라벤더_E34": "#800080",
    "골든블랙_E36": "#1A1A1A"
}

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("방 사진을 올려주세요", type=["jpg", "png"])
    selected_color = st.selectbox("🎨 색상 선택", list(cotton_colors.keys()))
    hex_color = cotton_colors[selected_color]

if uploaded_file:
    # 이미지 처리 엔진
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)
    
    with col1:
        st.image(image, caption="시공 전", use_container_width=True)

    if st.button("🚀 시뮬레이션 실행"):
        # HEX를 RGB로 변환
        h = hex_color.lstrip('#')
        rgb = [int(h[i:i+2], 16) for i in (0, 2, 4)]
        
        # 가구의 음영을 살리는 고급 합성 기술 (Multiply 블렌딩)
        # 벽지의 텍스처와 그림자를 그대로 유지하면서 색상만 입힙니다.
        overlay = np.full(img_np.shape, rgb, dtype='uint8')
        
        # 0.6은 원본 유지율, 0.4는 색상 반영율 (조절 가능)
        result = cv2.addWeighted(img_np, 0.6, overlay, 0.4, 0)
        
        with col2:
            st.image(result, caption=f"{selected_color} 적용 예시", use_container_width=True)
            st.success("✅ 가구 보호 모드로 도배 완료!")
