import streamlit as st
import requests
import io
import base64
from PIL import Image

# 1. 보안 설정
HF_TOKEN = st.secrets["HF_TOKEN"]
# 주소를 더 튼튼한 v1.1 버전으로 교체했습니다!
API_URL = "https://api-inference.huggingface.co/models/lllyasviel/control_v11p_sd15_canny"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="cottonshow AI 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 가구 그대로! 정밀 시뮬레이션")

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
        st.image(image, caption="시공 전", use_container_width=True)

    if st.button("✨ 정밀 시뮬레이션 시작"):
        with st.spinner("가구 위치를 고정하고 도배 중입니다..."):
            img_str = image_to_base64(image)
            color_prompt = cotton_colors[selected_name]
            
            payload = {
                "inputs": f"interior design, walls in {color_prompt}, fabric texture, realistic lighting, 8k",
                "image": img_str,
                "parameters": {
                    "negative_prompt": "change furniture, move items, distorted, blurry, low quality",
                    "num_inference_steps": 20
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                try:
                    result_image = Image.open(io.BytesIO(response.content))
                    with col2:
                        st.image(result_image, caption=f"{selected_name} 시공 후", use_container_width=True)
                        st.success("성공! 가구가 그대로인지 확인해 보세요.")
                except:
                    st.error("AI가 사진 대신 다른 응답을 보냈습니다. 다시 한번 눌러주세요.")
            elif response.status_code == 503:
                st.warning("모델이 부팅 중입니다. 15초 뒤에 다시 시도해 주세요!")
            else:
                st.error(f"오류 발생 (코드: {response.status_code}). 다른 주소를 찾아보겠습니다.")
