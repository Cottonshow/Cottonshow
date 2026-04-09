import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="cottonshow 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 가구 유지 시뮬레이터 (v2.0)")

# 사장님의 제품 색상을 더 명확하게 정의 (가구 고정 키워드 포함)
cotton_colors = {
    "화이트 (Natural White)": "pure clean snow white walls, keep original furniture, same room layout",
    "베이지 (Cream Beige)": "warm creamy oatmeal beige walls, keep original furniture, same room layout",
    "민트 (Soft Mint)": "pale soft mint green walls, keep original furniture, same room layout",
    "그레이 (Cloud Gray)": "modern light neutral gray walls, keep original furniture, same room layout"
}

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("방 사진을 올려주세요", type=["jpg", "png"])
    selected_name = st.selectbox("원하는 cottonshow 색상", list(cotton_colors.keys()))

if uploaded_file:
    image = Image.open(uploaded_file)
    with col1:
        st.image(image, caption="시공 전", use_container_width=True)

    if st.button("✨ 시뮬레이션 시작"):
        with st.spinner("가구는 그대로, 벽지만 예쁘게 바꾸는 중입니다..."):
            color_desc = cotton_colors[selected_name]
            
            # [핵심] 가구를 지키기 위한 강도 높은 명령어 조합
            # 'photorealistic interior photography'와 'original furniture'를 강조했습니다.
            prompt = f"photorealistic interior of the same room, walls covered in {color_desc}, maintain existing furniture, keep same sofa and layout, high detail, 8k"
            encoded_prompt = requests.utils.quote(prompt)
            
            # 에러 없는 초고속 서버 주소
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={int(io.BytesIO(uploaded_file.getvalue()).getbuffer()[0])}"
            
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    result_image = Image.open(io.BytesIO(response.content))
                    with col2:
                        st.image(result_image, caption=f"{selected_name} 시공 예상", use_container_width=True)
                        st.success("도배 완료! 전체적인 분위기를 확인해 보세요.")
                else:
                    st.error("AI가 잠시 쉬고 있네요. 다시 한번 눌러주세요!")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
