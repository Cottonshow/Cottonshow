import streamlit as st
import requests
import io
import base64
from PIL import Image

# 1. 보안 설정
HF_TOKEN = st.secrets["HF_TOKEN"]
# 가장 안정적인 ControlNet 모델
API_URL = "https://api-inference.huggingface.co/models/lllyasviel/sd-controlnet-canny"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="cottonshow AI 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 가구 그대로! 정밀 시뮬레이션")

# 사장님 제품 컬러 데이터
cotton_colors = {
    "화이트 (Natural White)": "pure clean snow white color wallpaper, high quality fabric texture",
    "베이지 (Cream Beige)": "warm creamy oatmeal beige color wallpaper, soft cotton texture",
    "민트 (Soft Mint)": "pale soft mint green color wallpaper, fresh fabric texture",
    "그레이 (Cloud Gray)": "modern neutral light gray color wallpaper, premium fabric feel"
}

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("방 사진을 올려주세요", type=["jpg", "png"])
    selected_name = st.selectbox("원하는 cottonshow 색상", list(cotton_colors.keys()))

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    with col1:
        st.image(image, caption="시공 전 (원본 가구)", use_container_width=True)

    if st.button("✨ 정밀 시뮬레이션 시작"):
        with st.spinner("가구 배치를 분석하며 정밀하게 도배 중입니다..."):
            # 에러 방지를 위해 사진을 base64 텍스트로 안전하게 변환
            img_str = image_to_base64(image)
            color_prompt = cotton_colors[selected_name]
            
            # JSON 데이터 형식 최적화
            payload = {
                "inputs": f"interior photo, walls in {color_prompt}, highly detailed, 8k",
                "image": img_str,
                "parameters": {
                    "negative_prompt": "change furniture, move sofa, blurry, low quality, distorted",
                    "num_inference_steps": 25
                }
            }
            
            # API 호출
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                try:
                    result_image = Image.open(io.BytesIO(response.content))
                    with col2:
                        st.image(result_image, caption=f"{selected_name} 시공 후 (가구 유지)", use_container_width=True)
                        st.success("완료! 가구는 그대로, 벽지만 예쁘게 바뀌었습니다.")
                except:
                    st.error("이미지 생성 중입니다. 10초만 기다렸다가 다시 버튼을 눌러보세요!")
            elif response.status_code == 503:
                st.warning("도배사가 준비 중입니다(모델 부팅). 잠시 후 다시 눌러보세요.")
            else:
                st.error(f"오류 발생 (코드: {response.status_code}). 잠시 후 재시도 부탁드립니다.")
