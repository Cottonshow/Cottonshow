import streamlit as st
import requests
import io
from PIL import Image

# 1. 허깅페이스에서 복사한 토큰을 여기에 붙여넣으세요.
HF_TOKEN = st.secrets["HF_TOKEN"
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 사이트 설정 (브라우저 탭에 표시될 이름)
st.set_page_config(page_title="cottonshow - 섬유 벽지 시뮬레이터", layout="wide")

# 메인 타이틀
st.title("🏠 cottonshow: 내 방 시뮬레이터")
st.markdown("#### 바르는 섬유 벽지, 우리 집에는 어떤 색이 어울릴까요?")
st.info("방 사진을 업로드하고 색상을 선택하면 AI가 시공 후 모습을 보여드립니다.")

# 화면 분할 (왼쪽: 설정 및 업로드 / 오른쪽: 결과)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 사진과 색상 선택")
    uploaded_file = st.file_uploader("방 사진을 올려주세요 (JPG, PNG)", type=["jpg", "png"])
    color = st.selectbox("원하는 cottonshow 색상", 
                        ["Natural White", "Cream Beige", "Soft Mint", "Warm Pink", "Cloud Gray", "Sky Blue"])

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

if uploaded_file:
    image = Image.open(uploaded_file)
    with col1:
        st.image(image, caption="시공 전 원본 사진", use_container_width=True)

    if st.button("✨ cottonshow 시뮬레이션 시작"):
        with st.spinner("AI가 cottonshow 섬유 벽지를 시공 중입니다..."):
            # AI에게 주는 상세 명령(Prompt)
            prompt = f"interior photography of a room, walls are beautifully covered with {color} color textured liquid fabric wallpaper, realistic interior design, high quality"
            image_bytes = query({"inputs": prompt})
            
            result_image = Image.open(io.BytesIO(image_bytes))
            with col2:
                st.subheader("2. 시공 후 예상 모습")
                st.image(result_image, caption=f"{color} 시공 후 (AI 예상안)", use_container_width=True)
                st.success(f"선택하신 {color} 색상입니다! 질감이 마음에 드시나요?")
                
                # 스마트스토어 링크로 연결되는 버튼
                st.link_button("🛒 cottonshow 제품 구매하러 가기", "https://smartstore.naver.com/davincistyle/products/5829868302")
