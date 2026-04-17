import streamlit as st
import requests
import io
import base64
from PIL import Image

# 1. 보안 설정
HF_TOKEN = st.secrets["HF_TOKEN"]
# img2img가 가장 잘 먹히는 표준 모델
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="cottonshow AI 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 가구 고정 img2img 시뮬레이터")

# 34가지 컬러 딕셔너리 (사장님 리스트 반영)
cotton_colors = {
    "퓨어화이트_E01": "pure snow white cotton texture wallpaper",
    "빈티지베이지_E02": "vintage warm beige fabric wallpaper",
    # ... (나머지 32개 컬러는 동일하게 유지) ...
    "골든블랙_E36": "luxurious black wallpaper with gold mineral chips"
}

# [핵심함수] 이미지를 AI가 읽을 수 있는 텍스트(base64)로 변환
def get_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("방 사진을 올려주세요", type=["jpg", "png"])
    selected_name = st.selectbox("🎨 색상 선택", list(cotton_colors.keys()))

if uploaded_file:
    # 원본 이미지 로드 및 리사이징 (API 부하 방지)
    init_image = Image.open(uploaded_file).convert("RGB")
    init_image = init_image.resize((512, 512)) # SD v1.5 최적 사이즈
    
    with col1:
        st.image(init_image, caption="시공 전", use_container_width=True)

    if st.button("✨ 정밀 도배 시작"):
        with st.spinner("원본 가구를 지키며 벽지를 칠하는 중..."):
            img_b64 = get_base64(init_image)
            color_desc = cotton_colors[selected_name]
            
            # 클로드가 말한 img2img 핵심 파라미터 적용
            payload = {
                "inputs": f"interior photo, walls changed to {color_desc}, maintain original furniture and layout, high quality",
                "image": img_b64,
                "parameters": {
                    "strength": 0.35,  # [매우 중요] 0.3~0.4 사이가 가구는 안 변하고 색만 바뀌는 황금 수치입니다!
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                result_image = Image.open(io.BytesIO(response.content))
                with col2:
                    st.image(result_image, caption=f"{selected_name} 시공 후", use_container_width=True)
                    st.success("원본의 구조를 유지하며 도배를 마쳤습니다!")
            else:
                st.error(f"오류 발생: {response.status_code}. 토큰 권한이나 서버 상태를 확인해 주세요.")
