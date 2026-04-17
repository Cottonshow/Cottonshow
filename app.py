import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="cottonshow 시뮬레이터", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    stButton>button { width: 100%; background-color: #d4a373; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🏠 cottonshow 실시간 벽지 체험")
st.info("💡 사진을 올린 후, 바꾸고 싶은 '벽면'을 마우스로 클릭해 주세요!")

# 34가지 색상 데이터 (HEX 코드 포함)
# 사장님, 실제 제품의 정확한 HEX 코드를 넣으시면 더 리얼해집니다!
cotton_colors = {
    "퓨어화이트_E01": "#FFFFFF", "빈티지베이지_E02": "#E5D3B3", "라이트그레이_E03": "#D3D3D3",
    "아이보리_E04": "#FFFFF0", "코토리베이지_E05": "#C5B4A2", "스톤그레이_E06": "#888888",
    "화이트골드칩_E07": "#FDF5E6", "스톤딥그레이_E09": "#4F4F4F", "핑크코튼캔디_E10": "#FFD1DC",
    "오렌지체리칩_E11": "#FFA500", "크리미레몬_E12": "#FFF44F", "네추럴핑크_E13": "#F8C8DC",
    "로맨틱딥핑크_E14": "#FF8DA1", "키즈옐로우_E15": "#FFF700", "미카레드_E16": "#B22222",
    "초코레드_E17": "#8B4513", "키즈오렌지_E18": "#FF8C00", "옐로우그린_E19": "#ADFF2F",
    "올리브그린_E20": "#808000", "민트코튼캔디_E21": "#AAF0D1", "머스크메론_E22": "#C3FDB8",
    "키즈그린_E23": "#00FF00", "블루_E24": "#0000FF", "라이트그린티_E25": "#D0F0C0",
    "스카이블루_E26": "#87CEEB", "카툰블루_E27": "#1E90FF", "라벤더코튼캔디_E28": "#E6E6FA",
    "후래쉬민트_E29": "#BDFCC9", "블루씨골드_E30": "#0077BE", "화이트라벤더_E31": "#F3E5AB",
    "미카네이비_E32": "#000080", "다크네이비_E33": "#000040", "딥라벤더_E34": "#800080",
    "골든블랙_E36": "#1A1A1A"
}

# 1. 색상 선택창
selected_color = st.selectbox("🎨 cottonshow 색상을 선택하세요", list(cotton_colors.keys()))
hex_color = cotton_colors[selected_name = selected_color]

# 2. 메인 시뮬레이터 엔진 (HTML/JS)
html_code = f"""
<div style="display: flex; flex-direction: column; align-items: center;">
    <input type="file" id="upload" accept="image/*" style="margin-bottom: 10px;">
    <canvas id="canvas" style="max-width: 100%; border: 2px solid #ddd; cursor: crosshair;"></canvas>
    <div style="margin-top: 10px;">
        <button onclick="resetImage()" style="padding: 10px; cursor: pointer;">되돌리기</button>
    </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const upload = document.getElementById('upload');
let originalData = null;

upload.addEventListener('change', (e) => {{
    const reader = new FileReader();
    reader.onload = (event) => {{
        const img = new Image();
        img.onload = () => {{
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            originalData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        }};
        img.src = event.target.result;
    }};
    reader.readAsDataURL(e.target.files[0]);
}});

canvas.addEventListener('mousedown', (e) => {{
    if (!originalData) return;
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) * (canvas.width / rect.width));
    const y = Math.floor((e.clientY - rect.top) * (canvas.height / rect.height));
    
    floodFill(x, y, '{hex_color}');
}});

function floodFill(startX, startY, fillColor) {{
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    const targetColor = getPixelColor(startX, startY, data);
    const replacementColor = hexToRgb(fillColor);
    
    if (colorsMatch(targetColor, replacementColor, 10)) return;

    const queue = [[startX, startY]];
    const visited = new Uint8Array(canvas.width * canvas.height);
    
    while (queue.length > 0) {{
        const [x, y] = queue.shift();
        const idx = (y * canvas.width + x) * 4;

        if (x < 0 || x >= canvas.width || y < 0 || y >= canvas.height) continue;
        if (visited[y * canvas.width + x]) continue;
        if (!colorsMatch(targetColor, getPixelColor(x, y, data), 30)) continue;

        data[idx] = replacementColor[0];
        data[idx+1] = replacementColor[1];
        data[idx+2] = replacementColor[2];
        
        visited[y * canvas.width + x] = 1;
        queue.push([x+1, y], [x-1, y], [x, y+1], [x, y-1]);
    }}
    ctx.putImageData(imageData, 0, 0);
}}

function getPixelColor(x, y, data) {{
    const idx = (y * canvas.width + x) * 4;
    return [data[idx], data[idx+1], data[idx+2]];
}}

function colorsMatch(c1, c2, threshold) {{
    return Math.abs(c1[0] - c2[0]) < threshold &&
           Math.abs(c1[1] - c2[1]) < threshold &&
           Math.abs(c1[2] - c2[2]) < threshold;
}}

function hexToRgb(hex) {{
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return [r, g, b];
}}

function resetImage() {{
    if (originalData) ctx.putImageData(originalData, 0, 0);
}}
</script>
"""

components.html(html_code, height=800, scrolling=True)
