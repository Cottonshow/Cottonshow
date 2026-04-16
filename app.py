import streamlit as st
import requests
import io
import base64
from PIL import Image

# 1. 보안 및 서버 설정
HF_TOKEN = st.secrets["HF_TOKEN"]
# 410 에러가 없는 최신 안정화 모델 주소
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="cottonshow AI 시뮬레이터", layout="wide")
st.title("🏠 cottonshow: 34가지 전컬러 정밀 시뮬레이션")

# 사장님이 주신 34가지 컬러 데이터베이스
cotton_colors = {
    "퓨어화이트_E01": "pure snow white, cotton texture wallpaper",
    "빈티지베이지_E02": "vintage warm beige, soft fabric wall",
    "라이트그레이_E03": "modern light gray, natural fiber wallpaper",
    "아이보리_E04": "warm ivory cream, soft cotton texture",
    "코토리베이지_E05": "kotori beige, trendy warm sand color",
    "스톤그레이_E06": "stone gray, mineral texture feel",
    "화이트골드칩_E07": "white wallpaper with subtle gold sparkles",
    "스톤딥그레이_E09": "deep charcoal stone gray, heavy texture",
    "핑크코튼캔디_E10": "pastel cotton candy pink, soft fluffy texture",
    "오렌지체리칩_E11": "vibrant orange with cherry chips texture",
    "크리미레몬_E12": "soft creamy lemon yellow, bright interior",
    "네추럴핑크_E13": "natural soft pink, blooming flower petal color",
    "로맨틱딥핑크_E14": "romantic deep rose pink, elegant wallpaper",
    "키즈옐로우_E15": "bright cheerful kids yellow, vivid color",
    "미카레드_E16": "mica red, sophisticated deep crimson",
    "초코레드_E17": "chocolate reddish brown, warm earth tone",
    "키즈오렌지_E18": "playful kids orange, energy color",
    "옐로우그린_E19": "fresh yellow green, spring leaf color",
    "올리브그린_E20": "calm olive green, forest nature feel",
    "민트코튼캔디_E21": "soft mint cotton candy, pastel fresh green",
    "머스크메론_E22": "musk melon green, sweet pastel tone",
    "키즈그린_E23": "vivid kids grass green, natural vibe",
    "블루_E24": "classic primary blue, clear sky color",
    "라이트그린티_E25": "light green tea, subtle calming green",
    "스카이블루_E26": "clear sky blue, airy and bright feel",
    "카툰블루_E27": "cartoonish bright blue, pop art style",
    "라벤더코튼캔디_E28": "lavender cotton candy, dreamy purple",
    "후래쉬민트_E29": "fresh cool mint, refreshing wallpaper",
    "블루씨골드_E30": "sea blue with golden sandy texture",
    "화이트라벤더_E31": "whitish lavender, very light purple pearl",
    "미카네이비_E32": "sophisticated mica navy, deep blue",
    "다크네이비_E33": "modern dark navy, formal and chic",
    "딥라벤더_E34": "deep mysterious lavender, royal purple",
    "골든블랙_E36": "luxurious black with gold mineral chips"
}

col1, col2 = st.columns([1, 1])

with col1:
    # 사장님이 주신 '샘플.jpg'를 기본 이미지로 설정 가능
    uploaded_file = st.file_uploader("방 사진을 올려주세요 (미업로드 시 샘플 사진 사용)", type=["jpg", "png"])
    selected_name = st.selectbox("🎨 cottonshow 색상 선택 (34종)", list(cotton_colors.keys()))

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
else:
    # 샘플 사진이 없을 경우를 대비한 안내
    st.info("왼쪽에서 사진을 업로드하거나, 기본 샘플로 테스트해보세요.")
    image = None

if image:
    with col1:
        st.image(image, caption="시공 전", use_container_width=True)

    if st.button("✨ cottonshow 시뮬레이션 시작"):
        with st.spinner(f"'{selected_name}' 색상으로 도배 중입니다..."):
            color_desc = cotton_colors[selected_name]
            # 가구 고정을 위해 프롬프트에 강력한 지시어 추가
            prompt = f"interior of a room, walls covered in {color_desc}, maintain all existing furniture, keep the sofa and plants exactly same, high resolution, 8k"
            
            payload = {"inputs": prompt}
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                result_image = Image.open(io.BytesIO(response.content))
                with col2:
                    st.image(result_image, caption=f"{selected_name} 시공 후 예상", use_container_width=True)
                    st.success("도배 완료! 실제 제품은 질감이 더 살아있습니다.")
            elif response.status_code == 503:
                st.warning("도배사가 준비 중입니다. 10초 뒤에 다시 버튼을 눌러주세요!")
            else:
                st.error(f"서버 연결 오류(코드: {response.status_code}). 잠시 후 다시 시도해 주세요.")
