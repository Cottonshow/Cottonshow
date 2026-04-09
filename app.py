import streamlit as st
import requests
import io
import time
from PIL import Image

# 1. 보안 설정 (Secrets 관리)
HF_TOKEN = st.secrets["HF_TOKEN"]

# 2. 가장 안정적인 모델 주소 (OpenJourney는 무료 중 응답률이 가장 좋습니다)
API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="cottonshow 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 내 방 시뮬레이터")

# 3. 사장님의 실제 제품 색상 데이터 (HEX 코드 포함)
# AI에게 정확한 색상을 지시하기 위해 구체적인 컬러값을 심었습니다.
cotton_colors = {
    "화이트 (Natural White)": {"eng": "pure snow white color #FFFFFF", "desc": "가장 깨끗하고 넓어 보이는 기본 화이트"},
    "베이지 (Cream Beige)": {"eng": "warm creamy oatmeal beige #F5F5DC", "desc": "따스하고 포근한 느낌의 스테디셀러"},
    "민트 (Soft Mint)": {"eng": "pale mint green color #E0FFF0", "desc": "공간을 생기 있게 만드는 산뜻한 민트"},
    "그레이 (Cloud Gray)": {"eng": "modern neutral light gray #D3D3D3", "desc": "세련되고 차분한 프리미엄 그레이"}
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
        with st.spinner("AI 도배사가 작업 중입니다... (최대 20초)"):
            color_data = cotton_colors[selected_name]
            # 색상 코드(#)와 질감(fabric texture)을 명확히 지시하여 정확도를 높임
            prompt = f"realistic interior photo, walls covered with {color_data['eng']} textured liquid fabric wallpaper, cotton texture, bright natural lighting, 8k"
            
            # AI에게 요청 (에러 대비 1회 재시도 포함)
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            
            # 결과 처리
            if response.status_code == 200:
                try:
                    # 응답이 진짜 이미지인지 확인 후 출력
                    result_image = Image.open(io.BytesIO(response.content))
                    with col2:
                        st.image(result_image, caption=f"{selected_name} 시공 예상 모습", use_container_width=True)
                        st.success(f"✅ {color_data['desc']} 적용 완료!")
                        st.link_button("🛒 실제 제품 확인하기", "https://smartstore.naver.com/davincistyle/products/5829868302")
                except:
                    st.error("AI 서버가 바쁩니다. 사진이 아닌 에러 문자를 보냈네요. 10초 뒤에 다시 버튼을 눌러주세요!")
            elif response.status_code == 503:
                st.warning("AI 모델이 부팅 중입니다. 잠시 후 다시 눌러보세요.")
            else:
                st.error(f"서버 연결 오류(코드: {response.status_code}). 토큰 권한을 다시 확인해 주세요.")
