import streamlit as st
import random
from datetime import datetime

# =====================================================
# 📱 디지털 친구 v13.0 - 논산시 노인 디지털 문해 교육 앱
# =====================================================

st.set_page_config(
    page_title="디지털 친구 v13.0 - 논산시 실버 디지털 교육",
    page_icon="📱",
    layout="centered"
)

# ─────────────────── 전역 상태 초기화 ───────────────────
defaults = {
    'font_size': 'large',
    'mode': 'MAIN',
    'step': 1,
    'selected_biz': '',
    'cart': {},
    'pay_method': '',
    'bank_pass': '',
    'voice_active': True,
    'voice_speed': 0.85,
    # 통계
    'stat_total_money': 0,
    'stat_success_count': 0,
    'stat_quiz_correct': 0,
    'stat_quiz_total': 0,
    # 배지
    'badges': [],
    # 은행
    'input_bank_name': '농협은행',
    'input_bank_account': '302-1234-5678-90',
    'input_bank_money': '50,000',
    # 버스
    'bus_from': '', 'bus_to': '', 'bus_time': '',
    'bus_p_adult': 0, 'bus_p_teen': 0,
    'bus_p_child': 0, 'bus_p_senior': 0,
    'bus_selected_seats': [],
    # 퀴즈
    'quiz_idx': 0,
    'quiz_answered': False,
    'quiz_result': '',
    # 튜토리얼
    'tutorial_step': 0,
    # SOS
    'sos_triggered': False,
    # 날씨 (가상)
    'weather': '☀️ 맑음 25°C',
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────── 동적 폰트 크기 ───────────────────
g_box_font = "30px" if st.session_state.font_size == "large" else "22px"
card_font  = "25px" if st.session_state.font_size == "large" else "18px"
btn_font   = "26px" if st.session_state.font_size == "large" else "19px"

# ─────────────────── CSS 전체 스타일 ───────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');

/* 전체 배경 */
.stApp {{ background: linear-gradient(160deg, #EEF2FF 0%, #F0FDF4 100%) !important; }}

html, body, p, span, label {{
    font-family: 'Nanum Gothic', sans-serif !important;
    color: #1F2937 !important;
}}

/* ── 사이드바 ── */
[data-testid="stSidebar"] {{
    background-color: #1E3A5F !important;
    border-right: none;
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}}
[data-testid="stSidebar"] .stMetric label,
[data-testid="stSidebar"] .stMetric [data-testid="metric-container"] p {{
    color: #93C5FD !important;
    font-size: 14px !important;
}}
[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {{
    color: #FFFFFF !important;
    font-size: 22px !important;
    font-weight: 900 !important;
}}

/* ── 메인 폰 컨테이너 ── */
.phone-container {{
    background: #FFFFFF;
    border-radius: 32px;
    padding: 28px 24px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.12);
    border: 1px solid #E2E8F0;
    margin-bottom: 20px;
    position: relative;
}}

/* ── SDGs 배너 ── */
.sdgs-banner {{
    background: linear-gradient(135deg, #1D4ED8 0%, #7C3AED 100%);
    color: #FFFFFF !important;
    padding: 22px 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 22px;
    box-shadow: 0 8px 20px rgba(29,78,216,0.3);
}}
.sdgs-banner h2 {{ color: #FFFFFF !important; margin:0; font-size:24px; font-weight:900; }}
.sdgs-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px 2px 0;
    font-weight: 800;
    border: 1px solid rgba(255,255,255,0.4);
    color: #FFFFFF !important;
}}

/* ── 진행 바 ── */
.step-indicator {{
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 20px;
}}
.step-dot {{
    width: 36px; height: 10px;
    background: #E2E8F0;
    border-radius: 10px;
    transition: all 0.3s;
}}
.step-dot.active {{
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    box-shadow: 0 0 8px rgba(37,99,235,0.5);
}}

/* ── 안내 박스 ── */
.guide-box {{
    font-size: {g_box_font};
    font-weight: 800;
    color: #1E3A5F !important;
    text-align: center;
    background: linear-gradient(135deg, #EFF6FF, #F0F9FF);
    padding: 24px 20px;
    border-radius: 20px;
    margin-bottom: 18px;
    border: 2.5px solid #3B82F6;
    line-height: 1.7;
    box-shadow: 0 4px 12px rgba(59,130,246,0.1);
}}

/* ── 성공 안내 박스 ── */
.guide-box-success {{
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5) !important;
    border: 2.5px solid #10B981 !important;
    color: #065F46 !important;
}}

/* ── 정보 카드 ── */
.info-card {{
    background: #F8FAFC;
    padding: 16px 20px;
    border-radius: 14px;
    border: 2px solid #E2E8F0;
    margin-bottom: 10px;
    font-size: {card_font};
    font-weight: 700;
    color: #334155 !important;
    line-height: 1.5;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}}

/* ── 금액 박스 ── */
.price-box {{
    background: linear-gradient(135deg, #FFF1F2, #FEE2E2);
    color: #B91C1C !important;
    font-size: 28px;
    font-weight: 900;
    text-align: center;
    padding: 18px;
    border-radius: 16px;
    margin: 14px 0;
    border: 2px dashed #FCA5A5;
    box-shadow: 0 4px 12px rgba(252,165,165,0.3);
}}

/* ── 배지 박스 ── */
.badge-box {{
    display: inline-block;
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    border: 2px solid #F59E0B;
    padding: 8px 16px;
    border-radius: 30px;
    font-size: 16px;
    font-weight: 800;
    color: #92400E !important;
    margin: 4px;
    box-shadow: 0 2px 6px rgba(245,158,11,0.3);
}}

/* ── 성과 리포트 박스 ── */
.report-box {{
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    border: 2px solid #10B981;
    padding: 22px;
    border-radius: 20px;
    margin: 16px 0;
    color: #065F46 !important;
    box-shadow: 0 4px 12px rgba(16,185,129,0.15);
}}
.report-box h4 {{ color: #065F46 !important; font-weight:900; margin-top:0; font-size:18px; }}

/* ── 퀴즈 정답/오답 박스 ── */
.quiz-correct {{
    background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
    border: 3px solid #10B981;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    font-size: 26px;
    font-weight: 900;
    color: #065F46 !important;
    margin: 12px 0;
}}
.quiz-wrong {{
    background: linear-gradient(135deg, #FEE2E2, #FECACA);
    border: 3px solid #EF4444;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    color: #7F1D1D !important;
    margin: 12px 0;
}}

/* ── SOS 버튼 ── */
.sos-btn {{
    background: linear-gradient(135deg, #DC2626, #B91C1C) !important;
    color: #FFFFFF !important;
    font-size: 22px !important;
    font-weight: 900 !important;
    border-radius: 50px !important;
    padding: 12px 30px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(220,38,38,0.4) !important;
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%, 100% {{ box-shadow: 0 4px 15px rgba(220,38,38,0.4); }}
    50% {{ box-shadow: 0 4px 25px rgba(220,38,38,0.7); }}
}}

/* ── 일반 버튼 ── */
.stButton>button {{
    width: 100%;
    min-height: 72px;
    font-size: {btn_font} !important;
    font-weight: 800 !important;
    border-radius: 16px !important;
    border: 2.5px solid #CBD5E1 !important;
    background: #FFFFFF !important;
    color: #1E3A5F !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.06) !important;
    margin-bottom: 8px;
    transition: all 0.2s;
}}
.stButton>button:hover {{
    border-color: #3B82F6 !important;
    background: #EFF6FF !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(59,130,246,0.2) !important;
}}

/* ── 주요 액션 버튼 (파랑) ── */
div[data-testid="column"] .stButton>button[kind="primary"],
.stButton>button[key*="start_btn"],
.stButton>button[key*="next_btn"],
.stButton>button[key*="pay_btn"],
.stButton>button[key*="complete_btn"] {{
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: #FFFFFF !important;
    border: none !important;
    min-height: 80px;
    box-shadow: 0 6px 16px rgba(37,99,235,0.35) !important;
}}

/* ── 푸터 ── */
.footer-notice {{
    text-align: center;
    color: #64748B !important;
    font-size: 15px;
    font-weight: 700;
    margin-top: 30px;
    padding: 18px;
    background: #F8FAFC;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    line-height: 1.6;
}}

/* ── 오늘의 날씨 ── */
.weather-card {{
    background: linear-gradient(135deg, #0EA5E9, #0284C7);
    color: #FFFFFF !important;
    padding: 12px 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 16px;
}}
.weather-card span {{ color: #FFFFFF !important; }}

/* ── 튜토리얼 말풍선 ── */
.tooltip-box {{
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    border: 2px solid #F59E0B;
    padding: 16px 20px;
    border-radius: 16px;
    font-size: 20px;
    font-weight: 800;
    color: #78350F !important;
    margin: 10px 0;
    position: relative;
}}
.tooltip-box::before {{
    content: "💡 도움말";
    display: block;
    font-size: 14px;
    color: #92400E !important;
    margin-bottom: 6px;
}}

/* ── 홈 메뉴 카드 ── */
.menu-card {{
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
    border: 3px solid #E2E8F0;
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    margin: 8px 0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    transition: all 0.2s;
    cursor: pointer;
}}
.menu-card:hover {{ border-color: #3B82F6; transform: translateY(-2px); }}
</style>
""", unsafe_allow_html=True)

# ─────────────────── 데이터 정의 ───────────────────
KIOSK_DATA = {
    "🍔 패스트푸드점 (논산 오거리점)": {
        "일반 햄버거": 5000, "치즈버거": 6000,
        "불고기버거": 5500, "감자튀김(M)": 2000, "콜라(M)": 1500
    },
    "☕ 커피 전문점 (탑정호 카페)": {
        "아메리카노": 3000, "카페라떼": 3500,
        "따뜻한 쌍화차": 4500, "생강차": 4500, "녹차라떼": 4000
    },
    "🛒 논산 농협하나로마트": {
        "국산 삼겹살 1kg": 28000, "바나나 한송이": 4000,
        "서울우유 1L": 2900, "신라면 5봉지": 4200, "계란 10구": 3500
    },
    "🏥 백제병원 무인수납기": {
        "일반 외래 진료비": 4500,
        "처방전 발행": 0,
        "소독약·붕대세트": 2500
    },
}
SHOP_DATA = {
    "🍓 논산 설향 딸기 1kg": 25000,
    "🌾 논산 삼광쌀 10kg": 35000,
    "🍠 연무대 꿀 고구마 5kg": 18000,
    "🍯 6년근 홍삼정 스틱 30포": 55000,
    "🥬 갓 따온 표고버섯 500g": 12000,
}
BUS_PRICE = {"서울경부": 15000, "부산종합": 32000, "대구한진": 26000, "대전복합": 6000}

# ─────────────────── 퀴즈 데이터 ───────────────────
QUIZ_DATA = [
    {
        "q": "키오스크에서 메뉴를 잘못 담았을 때 어떻게 하나요?",
        "choices": ["그냥 계산한다", "장바구니에서 빼기(➖)를 누른다", "기계를 끈다", "직원을 부른다"],
        "ans": 1,
        "explain": "장바구니 화면에서 ➖ 버튼을 누르면 수량을 줄이거나 삭제할 수 있어요!"
    },
    {
        "q": "스마트폰으로 돈을 송금할 때 가장 먼저 확인해야 할 것은?",
        "choices": ["계좌번호가 맞는지 확인", "배터리가 충분한지 확인", "신호가 잡히는지 확인", "빠른 시간 내에 보내기"],
        "ans": 0,
        "explain": "계좌번호가 틀리면 돈이 엉뚱한 곳으로 가요! 반드시 먼저 확인하세요."
    },
    {
        "q": "카드 결제 시 카드를 꽂는 방향은?",
        "choices": ["아무 방향이나 넣어도 된다", "카드 앞면(숫자 있는 면)이 보이게 넣는다", "뒷면이 보이게 넣는다", "카드마다 다르다"],
        "ans": 1,
        "explain": "대부분의 카드 단말기는 카드 앞면(번호가 있는 면)이 정면으로 보이게 꽂아야 해요!"
    },
    {
        "q": "온라인 쇼핑에서 결제 후 상품이 안 오면 어디에 연락하나요?",
        "choices": ["경찰에 신고", "앱 안 '고객센터' 또는 '1:1 문의'에 연락", "아무것도 하지 않는다", "직접 판매자 집에 찾아간다"],
        "ans": 1,
        "explain": "앱 안에 있는 고객센터나 1:1 문의에 연락하면 환불·재배송을 도와줘요!"
    },
    {
        "q": "고속버스 예매 후 표를 잃어버리면 어떻게 하나요?",
        "choices": ["다시 예매해야 한다", "스마트폰 앱에서 예매 내역을 확인하면 된다", "표가 없으면 탈 수 없다", "터미널 직원에게 물어봐야 한다"],
        "ans": 1,
        "explain": "모바일 앱 예매는 종이 표가 없어도 스마트폰 앱의 '예매 내역'으로 탑승할 수 있어요!"
    },
    {
        "q": "개인 비밀번호(PIN)를 입력할 때 주의할 점은?",
        "choices": ["빨리 입력한다", "주변에 있는 사람이 못 보도록 손으로 가리고 입력한다", "번호를 크게 말하면서 입력한다", "번호를 메모장에 적어놓는다"],
        "ans": 1,
        "explain": "비밀번호는 반드시 손으로 가리고 입력해야 개인정보를 지킬 수 있어요! 🔒"
    },
    {
        "q": "키오스크에서 주문이 완료됐을 때 꼭 챙겨야 할 것은?",
        "choices": ["기계를 닫는다", "대기 번호표와 영수증을 챙긴다", "바로 자리에 앉아서 기다린다", "직원에게 알린다"],
        "ans": 1,
        "explain": "주문 후 나오는 대기 번호표와 영수증은 반드시 챙기세요! 분실 시 교환이 어려울 수 있어요."
    },
]

# ─────────────────── 유틸 함수 ───────────────────
def speak(text):
    if st.session_state.get('voice_active', True):
        spd = st.session_state.get('voice_speed', 0.85)
        clean = text.replace("'", " ").replace('"', ' ')
        js = f"<script>var u=new SpeechSynthesisUtterance('{clean}');u.lang='ko-KR';u.rate={spd};window.speechSynthesis.cancel();window.speechSynthesis.speak(u);</script>"
        st.components.v1.html(js, height=0)

def get_total_price():
    m = st.session_state.mode
    biz = st.session_state.selected_biz
    if m == "APP":
        if biz == "쇼핑":
            return sum(SHOP_DATA.get(n, 0) * q for n, q in st.session_state.cart.items())
        if biz == "은행":
            try: return int("".join(filter(str.isdigit, str(st.session_state.input_bank_money))))
            except: return 50000
        if biz == "버스":
            base = BUS_PRICE.get(st.session_state.bus_to, 15000)
            return (st.session_state.bus_p_adult * base
                    + st.session_state.bus_p_teen * int(base*0.8)
                    + st.session_state.bus_p_child * int(base*0.5)
                    + st.session_state.bus_p_senior * int(base*0.7))
    if not biz or biz not in KIOSK_DATA: return 0
    return sum(KIOSK_DATA[biz].get(n, 0) * q for n, q in st.session_state.cart.items())

def reset_state():
    keys = ['step','cart','selected_biz','pay_method','bank_pass',
            'bus_from','bus_to','bus_time',
            'bus_p_adult','bus_p_teen','bus_p_child','bus_p_senior',
            'bus_selected_seats']
    for k in keys:
        if isinstance(defaults[k], dict): st.session_state[k] = {}
        elif isinstance(defaults[k], list): st.session_state[k] = []
        elif isinstance(defaults[k], int): st.session_state[k] = 0
        else: st.session_state[k] = defaults[k]

def draw_step_bar(current, total=7):
    html = '<div class="step-indicator">'
    for i in range(1, total+1):
        cls = "active" if i <= current else ""
        html += f'<div class="step-dot {cls}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def give_badge(badge):
    if badge not in st.session_state.badges:
        st.session_state.badges.append(badge)
        st.balloons()

def show_badges():
    if st.session_state.badges:
        st.markdown("**🏅 내가 받은 배지:**")
        html = "".join(f'<span class="badge-box">{b}</span>' for b in st.session_state.badges)
        st.markdown(html, unsafe_allow_html=True)

# ─────────────────── SDGs 배너 ───────────────────
st.markdown("""
<div class="sdgs-banner">
    <h2>📱 디지털 친구 v13.0</h2>
    <div style="color:#BFDBFE; font-size:14px; margin:6px 0 10px;">논산시 노인 디지털 사회 격차 해소 프로젝트</div>
    <span class="sdgs-badge">UN SDGs 4 · 양질의 평생 교육</span>
    <span class="sdgs-badge">UN SDGs 10 · 정보 불평등 완화</span>
    <span class="sdgs-badge">UN SDGs 11 · 포용적 지역사회</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────── 사이드바 ───────────────────
with st.sidebar:
    st.markdown("## ⚙️ 스마트 가이드 설정")

    # 날씨
    now_h = datetime.now().hour
    weather_list = ["☀️ 맑음 24°C", "⛅ 구름조금 22°C", "🌤️ 맑음 26°C"]
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0EA5E9,#0284C7);
                color:#FFF;padding:12px;border-radius:12px;
                text-align:center;font-size:18px;font-weight:800;margin-bottom:12px;">
        🌤️ 오늘 논산 날씨<br>{weather_list[now_h % 3]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.session_state.voice_active = st.checkbox("🔊 음성 가이드 켜기", value=True)
    st.session_state.voice_speed = st.slider("🐢 말하기 속도", 0.5, 1.2, 0.85, 0.05)

    f_choice = st.radio("👵 글씨 크기", ["크게 보기 (추천)", "보통 보기"])
    st.session_state.font_size = "large" if "크게" in f_choice else "normal"

    st.markdown("---")
    st.markdown("### 📊 내 학습 현황")
    st.metric("✅ 성공 횟수", f"{st.session_state.stat_success_count}회")
    st.metric("💰 가상 연습 금액", f"{st.session_state.stat_total_money:,}원")
    if st.session_state.stat_quiz_total > 0:
        pct = int(st.session_state.stat_quiz_correct / st.session_state.stat_quiz_total * 100)
        st.metric("🧠 퀴즈 정답률", f"{pct}%")

    st.markdown("---")
    # 배지 목록
    if st.session_state.badges:
        st.markdown("### 🏅 내 배지")
        for b in st.session_state.badges:
            st.markdown(f"- {b}")

    st.markdown("---")
    # SOS 버튼
    st.markdown("### 🆘 도움이 필요하세요?")
    if st.button("🆘 선생님 도움 요청", key="sos_sidebar"):
        st.session_state.sos_triggered = True
        st.session_state.mode = "SOS"
        st.rerun()

# ─────────────────── 폰 프레임 시작 ───────────────────
st.markdown('<div class="phone-container">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 🏠 메인 홈 화면
# ══════════════════════════════════════════════
if st.session_state.mode == "MAIN":
    hour = datetime.now().hour
    greet = "좋은 아침이에요" if hour < 12 else ("좋은 오후예요" if hour < 18 else "좋은 저녁이에요")
    st.markdown(f'<div class="guide-box">{greet}! 어르신 😊<br>오늘도 차근차근 같이 해봐요!</div>',
                unsafe_allow_html=True)

    show_badges()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏪 무인 기계\n(키오스크) 연습", key="btn_main_kiosk"):
            st.session_state.mode = "KIOSK"; reset_state()
            speak("무인 기계 주문 연습을 시작합니다."); st.rerun()
    with col2:
        if st.button("📱 스마트폰 앱\n(송금·쇼핑·버스) 연습", key="btn_main_app"):
            st.session_state.mode = "APP"; reset_state()
            speak("스마트폰 앱 연습을 시작합니다."); st.rerun()

    if st.button("🧠 디지털 상식 퀴즈 풀기 (OX·사지선다)", key="btn_main_quiz"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_idx = 0
        st.session_state.quiz_answered = False
        speak("퀴즈 도전을 시작합니다!"); st.rerun()

    if st.button("📖 기초 사용법 보기 (튜토리얼)", key="btn_main_tutorial"):
        st.session_state.mode = "TUTORIAL"
        st.session_state.tutorial_step = 0
        speak("기초 사용 방법 안내를 시작합니다."); st.rerun()

    # 하단 정보
    st.markdown(f"""
    <div class="info-card" style="margin-top:14px; text-align:center;">
        📅 오늘 날짜: {datetime.now().strftime('%Y년 %m월 %d일 (%A)').replace('Monday','월요일').replace('Tuesday','화요일').replace('Wednesday','수요일').replace('Thursday','목요일').replace('Friday','금요일').replace('Saturday','토요일').replace('Sunday','일요일')}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 📖 기초 튜토리얼 모드
# ══════════════════════════════════════════════
elif st.session_state.mode == "TUTORIAL":
    tutorials = [
        {
            "title": "📱 스마트폰이란?",
            "img": "https://img.freepik.com/free-vector/smartphone-concept-illustration_114360-7046.jpg?w=400",
            "content": "스마트폰은 작은 컴퓨터예요. 전화만 하는 게 아니라 인터넷 검색, 쇼핑, 버스 예매까지 모두 할 수 있어요! 😊",
            "tip": "화면을 가볍게 한 번 누르면 '터치', 두 번 빠르게 누르면 '더블 터치'예요."
        },
        {
            "title": "🏪 무인 기계(키오스크)란?",
            "img": "https://img.freepik.com/free-vector/kiosk-concept-illustration_114360-7046.jpg?w=400",
            "content": "식당, 마트, 병원에 있는 큰 화면의 기계예요. 직원 대신 내가 직접 주문하고 결제할 수 있어요.",
            "tip": "잘못 눌렀다고 걱정 마세요! '취소' 또는 '뒤로 가기' 버튼을 누르면 언제든지 다시 할 수 있어요."
        },
        {
            "title": "💳 카드 결제 방법",
            "img": "https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-cartoon-illustration_107791-3860.jpg?w=400",
            "content": "카드 앞면(숫자 있는 면)이 보이게 꽂으세요. '삑' 소리가 나면 완료! 비밀번호를 손으로 가리고 입력하세요.",
            "tip": "카드를 천천히 완전히 끝까지 밀어 넣어야 해요. 반쯤만 넣으면 오류가 나요."
        },
        {
            "title": "📲 QR코드·바코드 결제",
            "img": "https://img.freepik.com/free-vector/qr-code-concept-illustration_114360-7037.jpg?w=400",
            "content": "스마트폰 앱에서 바코드가 표시되면, 기계 앞에 있는 빨간 불빛이 나오는 곳에 가까이 대어 주세요.",
            "tip": "빛이 나오는 곳에서 약 5~10cm 거리에서 대면 '삑' 소리가 나며 인식돼요!"
        },
        {
            "title": "🔑 비밀번호 안전하게 지키기",
            "img": "https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg?w=400",
            "content": "비밀번호는 절대 다른 사람에게 알려주지 마세요. 입력할 때는 반드시 손으로 가려주세요.",
            "tip": "전화로 은행 직원이라며 비밀번호를 묻는다면 100% 사기예요! 절대 알려주지 마세요."
        },
    ]

    t = st.session_state.tutorial_step
    if t < len(tutorials):
        item = tutorials[t]
        draw_step_bar(t+1, len(tutorials))
        st.markdown(f'<div class="guide-box">{item["title"]}</div>', unsafe_allow_html=True)
        try:
            st.image(item["img"], use_container_width=True)
        except:
            pass
        st.markdown(f'<div class="info-card">{item["content"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tooltip-box">{item["tip"]}</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if t > 0:
                if st.button("⬅ 이전", key="tut_prev"):
                    st.session_state.tutorial_step -= 1; st.rerun()
        with c2:
            if t < len(tutorials)-1:
                if st.button("다음 ➡", key="tut_next"):
                    st.session_state.tutorial_step += 1
                    speak(tutorials[t+1]["title"]); st.rerun()
            else:
                if st.button("✅ 튜토리얼 완료!", key="tut_done"):
                    give_badge("📖 튜토리얼 수료")
                    st.session_state.mode = "MAIN"; st.rerun()
        if st.button("🏠 홈으로", key="tut_home"):
            st.session_state.mode = "MAIN"; st.rerun()
    else:
        st.session_state.mode = "MAIN"; st.rerun()


# ══════════════════════════════════════════════
# 🧠 퀴즈 모드
# ══════════════════════════════════════════════
elif st.session_state.mode == "QUIZ":
    idx = st.session_state.quiz_idx

    if idx >= len(QUIZ_DATA):
        # 퀴즈 완료
        correct = st.session_state.stat_quiz_correct
        total_q = st.session_state.stat_quiz_total
        pct = int(correct / total_q * 100) if total_q > 0 else 0
        st.markdown(f'<div class="guide-box guide-box-success">🎓 퀴즈 완료!<br>총 {total_q}문제 중 {correct}개 정답!<br>정답률 {pct}% 🏆</div>',
                    unsafe_allow_html=True)
        if pct >= 80:
            give_badge("🧠 퀴즈 우수 수료")
            st.markdown('<div class="quiz-correct">👏 훌륭해요! 디지털 지식 박사 등극!</div>', unsafe_allow_html=True)
        elif pct >= 50:
            give_badge("📝 퀴즈 도전 완료")
            st.markdown('<div class="info-card">잘 하셨어요! 틀린 문제도 다시 복습해 봐요.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="quiz-wrong">조금 더 연습해봐요! 다시 도전해 보세요 💪</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 다시 풀기", key="quiz_retry"):
                st.session_state.quiz_idx = 0
                st.session_state.quiz_answered = False
                st.session_state.quiz_result = ''
                st.rerun()
        with c2:
            if st.button("🏠 홈으로", key="quiz_home"):
                st.session_state.mode = "MAIN"; st.rerun()
    else:
        q = QUIZ_DATA[idx]
        draw_step_bar(idx+1, len(QUIZ_DATA))
        st.markdown(f'<div class="guide-box">❓ 문제 {idx+1}/{len(QUIZ_DATA)}<br>{q["q"]}</div>',
                    unsafe_allow_html=True)

        if not st.session_state.quiz_answered:
            for ci, choice in enumerate(q["choices"]):
                if st.button(f"{ci+1}. {choice}", key=f"quiz_c_{idx}_{ci}"):
                    st.session_state.stat_quiz_total += 1
                    if ci == q["ans"]:
                        st.session_state.stat_quiz_correct += 1
                        st.session_state.quiz_result = "correct"
                        speak("정답입니다! 훌륭해요!")
                    else:
                        st.session_state.quiz_result = "wrong"
                        speak("아쉽지만 틀렸어요. 정답을 확인해보세요.")
                    st.session_state.quiz_answered = True
                    st.rerun()
        else:
            if st.session_state.quiz_result == "correct":
                st.markdown('<div class="quiz-correct">🎉 정답! 아주 잘 아시네요!</div>', unsafe_allow_html=True)
            else:
                wrong_ans = q["choices"][q["ans"]]
                st.markdown(f'<div class="quiz-wrong">😅 아쉬워요! 정답은:<br>✅ {wrong_ans}</div>',
                            unsafe_allow_html=True)
            st.markdown(f'<div class="tooltip-box">{q["explain"]}</div>', unsafe_allow_html=True)

            if st.button("다음 문제 ➡", key=f"quiz_next_{idx}"):
                st.session_state.quiz_idx += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_result = ''
                st.rerun()

        if st.button("🏠 홈으로 나가기", key="quiz_exit"):
            st.session_state.mode = "MAIN"; st.rerun()


# ══════════════════════════════════════════════
# 🆘 SOS 도움 요청 화면
# ══════════════════════════════════════════════
elif st.session_state.mode == "SOS":
    st.markdown("""
    <div class="guide-box" style="background:linear-gradient(135deg,#FFF1F2,#FEE2E2)!important;
         border:3px solid #EF4444!important;">
        🆘 선생님에게 도움 요청 중...<br>잠시만 기다려주세요!
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card" style="border:2px solid #EF4444;">
        📞 긴급 연락처<br>
        • 논산시 디지털 교육 담당자: 041-746-XXXX<br>
        • 논산시청 노인복지과: 041-746-5XXX<br>
        • 전국 디지털 배움터: 1800-0096 (무료)
    </div>
    """, unsafe_allow_html=True)
    st.info("📢 선생님이 곧 오실 거예요. 손을 들어 주세요!")
    if st.button("✅ 괜찮아졌어요, 돌아가기", key="sos_back"):
        st.session_state.sos_triggered = False
        st.session_state.mode = "MAIN"; st.rerun()


# ══════════════════════════════════════════════
# 🏪 키오스크 모드
# ══════════════════════════════════════════════
elif st.session_state.mode == "KIOSK":
    draw_step_bar(st.session_state.step)

    # ── 1단계: 시작 안내 ──
    if st.session_state.step == 1:
        st.markdown("""
        <div class="guide-box">
            잘못 눌러도 돈이 나가지 않아요! 😊<br>
            부담 없이 마음껏 눌러보세요.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="tooltip-box">키오스크는 24시간 줄 없이 혼자 주문할 수 있는 스마트 기계예요!</div>',
                    unsafe_allow_html=True)
        if st.button("연습 시작하기 🏁", key="k_start_btn"):
            st.session_state.step = 2; speak("연습할 매장을 골라주세요."); st.rerun()
        if st.button("🏠 메인 홈으로 나가기", key="k_home_btn"):
            st.session_state.mode = "MAIN"; st.rerun()

    # ── 2단계: 매장 선택 ──
    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습할 매장을 골라주세요!</div>', unsafe_allow_html=True)
        for biz in KIOSK_DATA:
            if st.button(biz, key=f"k_biz_{biz}"):
                st.session_state.selected_biz = biz
                st.session_state.step = 3
                speak(f"{biz}를 선택하셨습니다."); st.rerun()
        if st.button("⬅ 뒤로", key="k_b2_back"):
            st.session_state.step = 1; st.rerun()

    # ── 3단계: 메뉴 담기 ──
    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">🍽️ {biz}<br>원하는 메뉴를 담고 다음을 누르세요.</div>',
                    unsafe_allow_html=True)
        for name, price in KIOSK_DATA[biz].items():
            qty = st.session_state.cart.get(name, 0)
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                badge = f' <span style="background:#DBEAFE;color:#1D4ED8;padding:2px 8px;border-radius:10px;font-size:16px;">{qty}개</span>' if qty > 0 else ""
                st.markdown(f'<div class="info-card">{name} ({price:,}원){badge}</div>',
                            unsafe_allow_html=True)
            with col2:
                if st.button("➕", key=f"k_add_{name}"):
                    st.session_state.cart[name] = qty + 1
                    speak(f"{name} 담기 완료"); st.rerun()
            with col3:
                if qty > 0 and st.button("➖", key=f"k_del_{name}"):
                    if qty == 1: del st.session_state.cart[name]
                    else: st.session_state.cart[name] = qty - 1
                    st.rerun()

        total = get_total_price()
        st.markdown(f'<div class="price-box">🛒 담은 금액: {total:,}원</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅ 매장 바꾸기", key="k_b3_back"):
                st.session_state.step = 2; st.session_state.cart = {}; st.rerun()
        with c2:
            if st.button("다음 단계 ➡", key="k_next_btn_3"):
                if total > 0: st.session_state.step = 4; speak("주문 내역을 확인하세요."); st.rerun()
                else: st.warning("⚠️ 메뉴를 하나 이상 담아주세요!")

    # ── 4단계: 장바구니 확인 ──
    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">🛒 장바구니 확인<br>내용이 맞으면 결제를 눌러주세요.</div>',
                    unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            price = KIOSK_DATA[st.session_state.selected_biz][name]
            st.markdown(f'<div class="info-card">✅ {name} — {qty}개 ({price*qty:,}원)</div>',
                        unsafe_allow_html=True)
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅ 더 담기", key="k_b4_back"):
                st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("결제하기 ➡", key="k_pay_btn_4"):
                st.session_state.step = 5; speak("결제 방법을 골라주세요."); st.rerun()

    # ── 5단계: 결제 수단 선택 ──
    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">💳 어떤 방법으로 결제하실래요?</div>', unsafe_allow_html=True)
        st.markdown('<div class="tooltip-box">카드를 꽂거나, 스마트폰을 대거나, 현금을 넣을 수 있어요.</div>',
                    unsafe_allow_html=True)
        if st.button("💵 현금 결제 (지폐를 투입구에 넣기)", key="k_pay_cash"):
            st.session_state.pay_method = "현금"; st.session_state.step = 7; st.rerun()
        if st.button("💳 카드 결제 (신용·체크카드 꽂기)", key="k_pay_card"):
            st.session_state.pay_method = "카드"; st.session_state.step = 6
            speak("카드를 방향에 맞게 깊숙이 넣어주세요."); st.rerun()
        if st.button("📱 논산사랑상품권 (바코드 스캔)", key="k_pay_nonsan"):
            st.session_state.pay_method = "지역화폐"; st.session_state.step = 6
            speak("상품권 바코드를 빨간 불빛에 가까이 대세요."); st.rerun()
        if st.button("📱 삼성페이·카카오페이 (스마트폰 태그)", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"; st.session_state.step = 6
            speak("스마트폰 뒷면을 리더기에 대주세요."); st.rerun()
        if st.button("⬅ 이전으로", key="k_b5_back"):
            st.session_state.step = 4; st.rerun()

    # ── 6단계: 결제 진행 ──
    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">💳 카드를 방향에 맞게<br>깊숙이 꽂아주세요!</div>',
                        unsafe_allow_html=True)
            try:
                st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-cartoon-illustration_107791-3860.jpg?w=500",
                         use_container_width=True)
            except: pass
            st.markdown('<div class="tooltip-box">앞면(숫자 있는 면)이 보이게 끝까지 밀어 넣으세요!</div>',
                        unsafe_allow_html=True)
            if st.button("카드를 꽂았어요 💳", key="k_complete_btn_card"):
                st.session_state.step = 7; st.rerun()
        elif st.session_state.pay_method == "지역화폐":
            st.markdown('<div class="guide-box">📱 논산사랑상품권 앱 바코드를<br>기계 아래 빨간 불빛에 대주세요!</div>',
                        unsafe_allow_html=True)
            if st.button("바코드를 스캔했어요 📱", key="k_complete_btn_nonsan"):
                st.session_state.step = 7; speak("상품권 결제 완료!"); st.rerun()
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">📱 스마트폰 뒷면을<br>기계 중앙 카드 표시 위에 올려놓으세요.</div>',
                        unsafe_allow_html=True)
            try:
                st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500",
                         use_container_width=True)
            except: pass
            if st.button("스마트폰을 올렸어요 📱", key="k_complete_btn_nfc"):
                st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="k_b6_back"):
            st.session_state.step = 5; st.rerun()

    # ── 7단계: 완료 ──
    elif st.session_state.step == 7:
        st.success("🎉 미션 성공! 완벽하게 해내셨어요!")
        total = get_total_price()
        st.session_state.stat_total_money += total
        st.session_state.stat_success_count += 1
        give_badge("🏪 키오스크 마스터")

        if "마트" in st.session_state.selected_biz:
            msg = f"계산 완료! 영수증을 받고 카트 물건을 챙기세요.<br>🧾 결제금액: {total:,}원"
        elif "병원" in st.session_state.selected_biz:
            msg = f"수납 완료! 약국 제출용 처방전을 꼭 챙기세요.<br>🧾 수납액: {total:,}원"
        else:
            msg = f"주문 완료! 전광판에 번호 뜨면 찾아가세요.<br>🎫 대기 번호표와 영수증을 챙기세요!<br>🧾 결제금액: {total:,}원"

        st.markdown(f'<div class="guide-box guide-box-success">{msg}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="report-box">
            <h4>📊 오늘의 디지털 성장 리포트</h4>
            🏅 오늘의 등급: <b>키오스크 당당 마스터!</b><br>
            🌿 이제 논산 어디서든 혼자서 자신 있게 주문할 수 있어요!<br>
            📈 누적 성공 횟수: <b>{st.session_state.stat_success_count}회</b>
        </div>
        """, unsafe_allow_html=True)
        show_badges()
        if st.button("🏠 처음으로 돌아가기", key="k_finish_btn_home"):
            st.session_state.mode = "MAIN"; st.rerun()
        if st.button("🔄 다시 한번 연습하기", key="k_retry_btn"):
            reset_state(); st.session_state.mode = "KIOSK"; st.rerun()


# ══════════════════════════════════════════════
# 📱 스마트폰 앱 모드
# ══════════════════════════════════════════════
elif st.session_state.mode == "APP":
    draw_step_bar(st.session_state.step)

    # ── 1단계 ──
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">📱 스마트폰 앱을 익히면<br>집에서 편하게 모든 걸 해결할 수 있어요!</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="tooltip-box">앱은 스마트폰 화면에 있는 작은 아이콘이에요. 누르면 바로 열려요!</div>',
                    unsafe_allow_html=True)
        if st.button("스마트폰 앱 연습 시작 🏁", key="a_start_btn"):
            st.session_state.step = 2; speak("연습할 앱을 골라주세요."); st.rerun()
        if st.button("🏠 홈으로", key="a_home_btn"):
            st.session_state.mode = "MAIN"; st.rerun()

    # ── 2단계: 앱 선택 ──
    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습하실 앱을 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("🛍️ 1. 논산 특산물 온라인 쇼핑", key="a_biz_shop"):
            st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; st.rerun()
        if st.button("🏦 2. NH 농협 뱅킹 (가상 송금)", key="a_biz_bank"):
            st.session_state.selected_biz = "은행"; st.session_state.step = 3; st.rerun()
        if st.button("🚍 3. 고속버스 티켓 예매", key="a_biz_bus"):
            st.session_state.selected_biz = "버스"; st.session_state.step = 3; st.rerun()
        if st.button("⬅ 뒤로", key="a_b2_back"):
            st.session_state.step = 1; st.rerun()

    # ── 3단계: 각 앱별 입력 ──
    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz

        # 🛍️ 쇼핑
        if biz == "쇼핑":
            st.markdown('<div class="guide-box">🛍️ 논산 농특산물 장터<br>사고 싶은 상품을 담아보세요!</div>',
                        unsafe_allow_html=True)
            for name, pr in SHOP_DATA.items():
                qty = st.session_state.cart.get(name, 0)
                c1, c2, c3 = st.columns([4, 1, 1])
                with c1:
                    badge = f' <span style="background:#DBEAFE;color:#1D4ED8;padding:2px 8px;border-radius:10px;font-size:16px;">{qty}개</span>' if qty > 0 else ""
                    st.markdown(f'<div class="info-card">{name} — {pr:,}원{badge}</div>', unsafe_allow_html=True)
                with c2:
                    if st.button("➕", key=f"s_add_{name}"):
                        st.session_state.cart[name] = qty + 1; st.rerun()
                with c3:
                    if qty > 0 and st.button("➖", key=f"s_del_{name}"):
                        if qty == 1: del st.session_state.cart[name]
                        else: st.session_state.cart[name] = qty - 1
                        st.rerun()
            total = get_total_price()
            st.markdown(f'<div class="price-box">🛒 장바구니 합계: {total:,}원</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⬅ 뒤로", key="s_p_back"):
                    st.session_state.step = 2; st.session_state.cart = {}; st.rerun()
            with c2:
                if st.button("주문하기 ➡", key="next_btn_shop"):
                    if total > 0: st.session_state.step = 4; speak("주문 내역을 확인하세요."); st.rerun()
                    else: st.warning("⚠️ 상품을 하나 이상 담아주세요.")

        # 🏦 은행
        elif biz == "은행":
            st.markdown('<div class="guide-box">🏦 NH 가상 모바일 뱅킹<br>송금 정보를 입력하세요.</div>',
                        unsafe_allow_html=True)
            st.markdown('<div class="tooltip-box">계좌번호를 틀리면 엉뚱한 곳에 돈이 가요! 꼭 확인하세요.</div>',
                        unsafe_allow_html=True)
            bank_list = ["농협은행", "국민은행", "신한은행", "우리은행", "우체국", "하나은행"]
            try: sel_idx = bank_list.index(st.session_state.input_bank_name)
            except: sel_idx = 0
            st.session_state.input_bank_name = st.selectbox(
                "1️⃣ 어느 은행으로 보낼까요?", bank_list, index=sel_idx)
            st.session_state.input_bank_account = st.text_input(
                "2️⃣ 받는 분 계좌번호", st.session_state.input_bank_account)
            st.session_state.input_bank_money = st.text_input(
                "3️⃣ 보낼 금액 (숫자만)", st.session_state.input_bank_money)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⬅ 이전", key="b_p_back"): st.session_state.step = 2; st.rerun()
            with c2:
                if st.button("송금 확인하기 ➡", key="next_btn_bank"):
                    st.session_state.step = 4; speak("입력하신 정보가 맞는지 확인하세요."); st.rerun()

        # 🚍 버스
        elif biz == "버스":
            st.markdown('<div class="guide-box">🚍 고속버스 예매<br>출발지와 목적지를 골라주세요.</div>',
                        unsafe_allow_html=True)
            st.write("📍 **1. 출발지 선택**")
            from_list = ["논산금호시외", "연무대터미널", "대전복합", "서울경부"]
            cf = st.columns(len(from_list))
            for i, fn in enumerate(from_list):
                highlight = "🔵 " if st.session_state.bus_from == fn else ""
                if cf[i].button(f"{highlight}{fn}", key=f"f_{fn}"):
                    st.session_state.bus_from = fn; st.rerun()
            st.write("📍 **2. 목적지 선택**")
            to_list = ["서울경부", "부산종합", "대구한진", "대전복합"]
            ct = st.columns(len(to_list))
            for i, tn in enumerate(to_list):
                highlight = "🔵 " if st.session_state.bus_to == tn else ""
                if ct[i].button(f"{highlight}{tn}", key=f"t_{tn}"):
                    st.session_state.bus_to = tn; st.rerun()
            if st.session_state.bus_from and st.session_state.bus_to:
                st.info(f"👉 여정: {st.session_state.bus_from} ➡ {st.session_state.bus_to}")
                st.write("⏰ **3. 버스 시간 선택**")
                times = ["08:00 (오전 이른)", "11:20 (오전 늦)", "14:50 (오후 이른)", "18:10 (오후 저녁)"]
                ctime = st.columns(2)
                for i, tv in enumerate(times):
                    highlight = "✅ " if st.session_state.bus_time == tv else ""
                    if ctime[i % 2].button(f"{highlight}{tv}", key=f"time_{i}"):
                        st.session_state.bus_time = tv; st.rerun()
                if st.session_state.bus_time:
                    st.success(f"✅ 선택: {st.session_state.bus_from} → {st.session_state.bus_to} / {st.session_state.bus_time}")
                    if st.button("인원수 정하러 가기 ➡", key="next_btn_bus_s1"):
                        st.session_state.step = 10; speak("몇 명이 탑승하시나요?"); st.rerun()
            if st.button("🔄 처음부터 다시 선택", key="bus_reset_all"):
                reset_state(); st.session_state.selected_biz = "버스"; st.rerun()

    # ── 10단계: 버스 인원 선택 ──
    elif st.session_state.step == 10:
        st.markdown('<div class="guide-box">🚍 탑승 인원 선택<br>➕➖ 버튼으로 인원을 조절하세요.</div>',
                    unsafe_allow_html=True)
        cols = st.columns(4)
        labels = [("어른\n(일반)", 'bus_p_adult'), ("청소년\n(중·고)", 'bus_p_teen'),
                  ("어린이\n(초등)", 'bus_p_child'), ("어르신\n(경로우대)", 'bus_p_senior')]
        for col, (label, key) in zip(cols, labels):
            with col:
                st.markdown(f"**{label}**")
                val = st.session_state[key]
                st.markdown(f"<h3 style='text-align:center;color:#1E3A5F;'>{val}명</h3>",
                            unsafe_allow_html=True)
                if st.button("➕", key=f"{key}_up"): st.session_state[key] += 1; st.rerun()
                if st.button("➖", key=f"{key}_dn"):
                    st.session_state[key] = max(0, val - 1); st.rerun()
        total_p = sum(st.session_state[k] for _, k in labels)
        st.markdown(f"<div class='price-box'>총 탑승 인원: {total_p}명</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅ 시간 다시", key="b_to_s3"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("좌석 고르기 ➡", key="next_btn_bus_seat"):
                if total_p > 0: st.session_state.step = 11; speak("좌석을 골라주세요."); st.rerun()
                else: st.warning("최소 1명 이상 선택하세요!")

    # ── 11단계: 좌석 선택 ──
    elif st.session_state.step == 11:
        total_need = sum(st.session_state[k] for k in
                         ['bus_p_adult','bus_p_teen','bus_p_child','bus_p_senior'])
        sel = st.session_state.bus_selected_seats
        st.markdown(f'<div class="guide-box">💺 좌석 선택<br>빈 좌석을 눌러서 {total_need}자리를 고르세요.<br>({len(sel)}/{total_need}석 선택됨)</div>',
                    unsafe_allow_html=True)
        st.caption("🚍 버스 앞쪽 방향 →")
        fixed_sold = [2, 5, 11, 19, 24]
        for row in range(1, 10):
            cols = st.columns([2, 2, 1, 2])
            for col_idx, seat_offset in enumerate([0, 1, None, 2]):
                if seat_offset is None:
                    cols[col_idx].write("")
                    continue
                seat_num = (row-1)*3 + seat_offset + 1
                if seat_num > 28: continue
                if seat_num in fixed_sold:
                    cols[col_idx].button(f"❌{seat_num:02d}", key=f"s_{seat_num}", disabled=True)
                elif seat_num in sel:
                    if cols[col_idx].button(f"⭐{seat_num:02d}", key=f"s_{seat_num}"):
                        sel.remove(seat_num); st.rerun()
                else:
                    if cols[col_idx].button(f"💺{seat_num:02d}", key=f"s_{seat_num}"):
                        if len(sel) < total_need: sel.append(seat_num); st.rerun()
                        else: st.warning("이미 모두 선택하셨어요!")
        st.markdown(f'<div class="price-box">💰 예상 운임: {get_total_price():,}원</div>',
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅ 인원 변경", key="b_to_s10"):
                st.session_state.bus_selected_seats = []; st.session_state.step = 10; st.rerun()
        with c2:
            if st.button("예약 확인 ➡", key="next_btn_bus_done"):
                if len(sel) == total_need: st.session_state.step = 4; speak("마지막으로 정보를 확인하세요."); st.rerun()
                else: st.error(f"좌석을 {total_need}개 모두 골라야 해요!")

    # ── 4단계: 최종 확인 ──
    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">✅ 신청 내용 최종 확인<br>정확한지 꼭 확인하세요!</div>',
                    unsafe_allow_html=True)
        biz = st.session_state.selected_biz
        if biz == "버스":
            st.markdown(f"""
            <div class='info-card'>
                🚌 고속버스 예매 정보<br>
                • <b>여정:</b> {st.session_state.bus_from} ➡ {st.session_state.bus_to}<br>
                • <b>시간:</b> {st.session_state.bus_time}<br>
                • <b>좌석:</b> {', '.join([f'{x}번' for x in st.session_state.bus_selected_seats])}
            </div>
            """, unsafe_allow_html=True)
        elif biz == "쇼핑":
            for name, qty in st.session_state.cart.items():
                st.markdown(f'<div class="info-card">✅ {name} — {qty}개 ({SHOP_DATA[name]*qty:,}원)</div>',
                            unsafe_allow_html=True)
        elif biz == "은행":
            try: dm = int("".join(filter(str.isdigit, str(st.session_state.input_bank_money))))
            except: dm = 50000
            st.markdown(f"""
            <div class='info-card'>
                🏦 NH 뱅킹 이체 정보<br>
                • <b>받는 은행:</b> {st.session_state.input_bank_name}<br>
                • <b>계좌번호:</b> {st.session_state.input_bank_account}<br>
                • <b>이체 금액:</b> <span style='color:#B91C1C;font-size:26px;'>{dm:,}원</span>
            </div>
            """, unsafe_allow_html=True)
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 금액: {total:,}원</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅ 수정하기", key="a_b4_back"):
                sv = biz; reset_state(); st.session_state.selected_biz = sv
                st.session_state.step = 3; st.rerun()
        with c2:
            if biz == "은행":
                if st.button("비밀번호 입력 🔑", key="next_btn_pass"):
                    st.session_state.step = 8; speak("비밀번호 6자리를 누르세요."); st.rerun()
            else:
                if st.button("결제하기 ➡", key="pay_btn_app4"):
                    st.session_state.step = 5; speak("결제 방법을 고르세요."); st.rerun()

    # ── 5단계: 결제 수단 ──
    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">📲 온라인 결제 방법을 선택하세요.</div>', unsafe_allow_html=True)
        if st.button("🏦 내 통장 계좌이체", key="a_pay_bank"):
            st.session_state.pay_method = "계좌이체"; st.session_state.step = 9; st.rerun()
        if st.button("📱 논산사랑상품권 QR 결제", key="a_pay_nonsan"):
            st.session_state.pay_method = "지역화폐"; st.session_state.step = 6
            speak("지역화폐 결제 단계입니다."); st.rerun()
        if st.button("💳 카드 번호 입력 결제", key="a_pay_card"):
            st.session_state.pay_method = "카드"; st.session_state.step = 6
            speak("카드 번호를 입력하세요."); st.rerun()
        if st.button("⬅ 이전", key="a_b5_back"): st.session_state.step = 4; st.rerun()

    # ── 6단계: 결제 처리 ──
    elif st.session_state.step == 6:
        if st.session_state.pay_method == "지역화폐":
            st.markdown('<div class="guide-box">📱 논산사랑상품권 가맹점 QR이 연결됐어요!<br>아래 버튼으로 결제를 확정하세요.</div>',
                        unsafe_allow_html=True)
            st.markdown('<div class="tooltip-box">QR코드를 가맹점에서 스캔하면 바로 결제가 돼요!</div>',
                        unsafe_allow_html=True)
            if st.button("지역화폐 결제 확정 🔒", key="complete_btn_app_nonsan"):
                st.session_state.step = 7; speak("상품권 결제 완료!"); st.rerun()
        else:
            st.markdown('<div class="guide-box">💳 카드 번호를 안전하게 입력하세요.</div>', unsafe_allow_html=True)
            st.text_input("카드 번호 16자리 (예시)", "9410 - 4567 - **** - ****")
            st.text_input("비밀번호 앞 2자리", type="password")
            if st.button("안전 결제 승인 🔒", key="complete_btn_app_card"):
                st.session_state.step = 7; speak("스마트폰 결제 성공!"); st.rerun()
        if st.button("⬅ 이전", key="a_b6_back"): st.session_state.step = 5; st.rerun()

    # ── 7단계: 완료 ──
    elif st.session_state.step == 7:
        st.success("🎉 미션 최종 성공! 훌륭하게 하셨어요!")
        total = get_total_price()
        st.session_state.stat_total_money += total
        st.session_state.stat_success_count += 1
        give_badge("📱 스마트폰 앱 마스터")

        st.markdown(f"""
        <div class="guide-box guide-box-success">
            참 잘하셨어요 어르신! 👏<br>
            스마트폰으로 처리가 모두 완료됐어요.<br>
            종이 없이도 스마트폰에 안전하게 보관돼요!<br>
            🧾 처리 금액: {total:,}원
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="report-box">
            <h4>📊 오늘의 디지털 성장 리포트</h4>
            🏆 오늘의 등급: <b>모바일 스마트 챔피언!</b><br>
            📉 이제 은행·터미널 줄 없이 집에서 모두 해결할 수 있어요!<br>
            📈 누적 성공 횟수: <b>{st.session_state.stat_success_count}회</b>
        </div>
        """, unsafe_allow_html=True)
        show_badges()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 홈으로", key="a_fin_btn_home"):
                st.session_state.mode = "MAIN"; st.rerun()
        with c2:
            if st.button("🔄 다시 연습", key="a_retry_btn"):
                reset_state(); st.session_state.mode = "APP"; st.rerun()

    # ── 8단계: 비밀번호 ──
    elif st.session_state.step == 8:
        try: target = int("".join(filter(str.isdigit, str(st.session_state.input_bank_money))))
        except: target = 50000
        st.markdown(f'<div class="guide-box">🔑 보안 비밀번호 입력<br>{st.session_state.input_bank_name}으로 {target:,}원 송금<br>6자리 숫자를 차례로 눌러주세요.</div>',
                    unsafe_allow_html=True)
        pw = st.session_state.bank_pass
        stars = "★" * len(pw) + "☆" * (6 - len(pw))
        st.markdown(f"<h1 style='text-align:center;color:#2563EB;letter-spacing:10px;font-size:40px;'>{stars}</h1>",
                    unsafe_allow_html=True)
        st.markdown('<div class="tooltip-box">손으로 화면을 가리고 비밀번호를 입력하세요! 🔒</div>',
                    unsafe_allow_html=True)

        # 번호 셔플로 보안 강화
        if 'num_order' not in st.session_state:
            nums = list(range(1, 10))
            random.shuffle(nums)
            st.session_state.num_order = nums

        rows = [st.session_state.num_order[i:i+3] for i in range(0, 9, 3)]
        for row_nums in rows:
            cols = st.columns(3)
            for col, n in zip(cols, row_nums):
                if col.button(str(n), key=f"num_{n}"):
                    st.session_state.bank_pass += str(n)
                    if len(st.session_state.bank_pass) >= 6:
                        if 'num_order' in st.session_state:
                            del st.session_state.num_order
                        st.session_state.pay_method = "은행"
                        st.session_state.step = 7
                        speak("통장에서 안전하게 전송됐습니다.")
                    st.rerun()

        mid = st.columns(3)
        if mid[1].button("0", key="num_0"):
            st.session_state.bank_pass += "0"
            if len(st.session_state.bank_pass) >= 6:
                if 'num_order' in st.session_state: del st.session_state.num_order
                st.session_state.pay_method = "은행"; st.session_state.step = 7
                speak("안전하게 전송됐습니다.")
            st.rerun()
        if st.button("❌ 잘못 눌렀어요 (다시 입력)", key="num_clear"):
            st.session_state.bank_pass = ""; st.rerun()

    # ── 9단계: 계좌이체 확인 ──
    elif st.session_state.step == 9:
        st.markdown('<div class="guide-box">내 은행 계좌를 확인하고 승인을 눌러주세요.</div>',
                    unsafe_allow_html=True)
        st.selectbox("출금 통장 선택", ["농협은행 (논산 시청지점)", "우체국", "국민은행"])
        st.text_input("내 계좌번호 (예시)", "302-5678-****")
        if st.button("안전 이체 최종 승인 🔒", key="complete_btn_app_tr"):
            st.session_state.step = 7; speak("안전하게 처리됐습니다."); st.rerun()
        if st.button("⬅ 이전", key="a_b9_back"): st.session_state.step = 5; st.rerun()


# ─────────────────── 폰 프레임 종료 ───────────────────
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────── 하단 안심 문구 ───────────────────
st.markdown("""
<div class="footer-notice">
    ⚠️ <b>안심하세요!</b> 이 앱은 교육용 모의 프로그램입니다.<br>
    가상의 돈으로 연습하는 것이니 실수가 나와도 실제 돈이 나가지 않아요. 마음껏 눌러보세요! 😊<br>
    <br>
    📞 <b>도움이 필요하면?</b> 전국 디지털 배움터: <b>1800-0096</b> (무료)
</div>
""", unsafe_allow_html=True)
