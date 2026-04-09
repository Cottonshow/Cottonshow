import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="cottonshow 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 내 방 시뮬레이터 (Ultra Fast)")

# 실제 제품 색상과 매칭되는 명령어
cotton_colors = {
    "화이트 (Natural White)": "pure clean snow white fabric wall",
    "베이지 (Cream Beige)": "warm creamy oatmeal beige fabric wall",
    "민트 (Soft Mint)": "pale soft mint green fabric wall",
    "그레이 (Cloud Gray)": "modern neutral light gray fabric wall"
}

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("방 사진을 올려주세요", type=["jpg", "png"])
    selected_name = st.selectbox("원하는 cottonshow 색상", list(cotton_colors.keys()))

if uploaded_file:
    # 원본 사진 표시
    image = Image.open(uploaded_file)
    with col1:
        st.image(image, caption="시공 전", use_container_width=True)

    if st.button("✨ 시뮬레이션 시작"):
        with st.spinner("AI가 즉시 도배 중입니다..."):
            # Pollinations AI는 주소만으로 이미지를 생성합니다 (토큰 불필요!)
            color_prompt = cotton_colors[selected_name]
            # 인테리어 전문 명령어로 보강
            prompt = f"realistic interior photo, room with {color_prompt}, cotton texture, high quality, 8k"
            encoded_prompt = requests.utils.quote(prompt)
            
            # 이 주소가 바로 이미지를 뱉어줍니다
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    result_image = Image.open(io.BytesIO(response.content))
                    with col2:
                        st.image(result_image, caption=f"{selected_name} 시공 후 예상 모습", use_container_width=True)
                        st.success("완료! 실제 cottonshow 제품과 색감을 비교해 보세요.")
                else:
                    st.error("AI 서버 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
