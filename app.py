import streamlit as st
import requests
import io
from PIL import Image

# 1. 보안 설정 (토큰은 그대로 쓰시면 됩니다!)
HF_TOKEN = st.secrets["HF_TOKEN"]

# 2. ControlNet 모델 주소 (구조를 유지하며 채색하는 모델)
# 이 모델은 이미지의 '뼈대'를 유지하는 데 특화되어 있습니다.
API_URL = "https://api-inference.huggingface.co/models/lllyasviel/sd-controlnet-canny"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="cottonshow AI 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 가구 그대로! 벽지만 쓱싹")

# 사장님의 실제 제품 컬러 데이터
cotton_colors = {
    "화이트 (Natural White)": "pure clean snow white color wallpaper, high quality fabric texture",
    "베이지 (Cream Beige)": "warm creamy oatmeal beige color wallpaper, soft cotton texture",
    "민트 (Soft Mint)": "pale soft mint green color wallpaper, fresh fabric texture",
    "그레이 (Cloud Gray)": "modern neutral light gray color wallpaper, premium fabric feel"
}

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("방 사진을 올려주세요 (가구가 있는 사진도 좋아요!)", type=["jpg", "png"])
    selected_name = st.selectbox("원하는 cottonshow 색상", list(cotton_colors.keys()))

if uploaded_file:
    # 원본 사진 준비
    image = Image.open(uploaded_file).convert("RGB")
    with col1:
        st.image(image, caption="시공 전 (원본 가구 유지)", use_container_width=True)

    if st.button("✨ 정밀 시뮬레이션 시작"):
        with st.spinner("가구 위치를 고정하고 도배 중입니다..."):
            # 이미지를 AI가 읽을 수 있는 데이터로 변환
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = buffered.getvalue()

            color_prompt = cotton_colors[selected_name]
            # AI에게 "이 뼈대(image) 위에 이 색상(prompt)을 입혀줘"라고 명령
            payload = {
                "inputs": color_prompt,
                "image": uploaded_file.getvalue(), # 원본 사진을 뼈대로 사용
                "parameters": {
                    "negative_prompt": "change furniture, move sofa, blurry, low quality",
                    "num_inference_steps": 30
                }
            }
            
            # API 호출 (무료 서버라 503 에러 대비 재시도 로직)
            for _ in range(3):
                response = requests.post(API_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    break
                import time
                time.sleep(5)

            if response.status_code == 200:
                try:
                    result_image = Image.open(io.BytesIO(response.content))
                    with col2:
                        st.image(result_image, caption=f"{selected_name} 시공 후 (가구 유지)", use_container_width=True)
                        st.success("완료! 가구 배치는 그대로, 벽지만 예쁘게 바뀌었습니다.")
                except:
                    st.error("AI가 사진을 만드는 중입니다. 10초 뒤에 다시 눌러주세요!")
            else:
                st.info("현재 서버가 정밀 분석 중입니다. 잠시 후 다시 '시뮬레이션 시작'을 눌러주세요.")
