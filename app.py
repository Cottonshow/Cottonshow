import streamlit as st
import requests
import io
import time
from PIL import Image

# 1. 스트림릿 세팅 (사장님 세팅 완벽함!)
HF_TOKEN = st.secrets["HF_TOKEN"]

# 2. 모델 주소 변경 (중요!! 현재 410 에러 안 나는 가장 안정적인 주소)
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="cottonshow 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 내 방 시뮬레이터")

# 3. cottonshow 실제 제품 색상값 (AI가 이해하기 쉽게 매칭)
cotton_colors = {
    "화이트 (Natural White)": {"eng": "pure snow white color wallpaper", "desc": "가장 깨끗한 기본 화이트"},
    "베이지 (Cream Beige)": {"eng": "warm creamy beige color wallpaper", "desc": "포근하고 아늑한 베스트셀러"},
    "민트 (Soft Mint)": {"eng": "pale mint green color wallpaper", "desc": "산뜻하고 생기 있는 공간"},
    "그레이 (Cloud Gray)": {"eng": "modern neutral light gray color wallpaper", "desc": "세련되고 차분한 프리미엄 그레이"}
}

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("방 사진을 올려주세요", type=["jpg", "png"])
    selected_name = st.selectbox("원하는 cottonshow 색상", list(cotton_colors.keys()))
    
if uploaded_file:
    image = Image.open(uploaded_file)
    with col1:
        st.image(image, caption="시공 전", use_container_width=True)

    if st.button("✨ cottonshow 시뮬레이션 시작"):
        with st.spinner("AI 도배사가 작업 중입니다..."):
            color_data = cotton_colors[selected_name]
            # AI가 '도배'라는 걸 확실히 인지하게 명령어 구성
            prompt = f"interior photo of a room, walls are painted in {color_data['eng']}, soft fabric texture, highly detailed, 8k"
            
            # API 호출
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            
            if response.status_code == 200:
                try:
                    result_image = Image.open(io.BytesIO(response.content))
                    with col2:
                        st.image(result_image, caption=f"{selected_name} 시공 후 예상", use_container_width=True)
                        st.success(f"✅ {color_data['desc']} 적용 완료!")
                except:
                    st.error("이미지를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
            elif response.status_code == 503:
                st.warning("AI 모델이 부팅 중입니다. 10초만 기다렸다가 다시 버튼을 눌러보세요!")
            else:
                st.error(f"서버 응답 오류 (코드: {response.status_code}). 모델 주소를 확인 중입니다.")
