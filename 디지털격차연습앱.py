import streamlit as st

# 1. 페이지 기본 설정 및 시니어 맞춤형 프리미엄 라이트 테마 정의
st.set_page_config(page_title="디지털 친구 v12.0 - 논산시 실버 디지털 문해 교육 앱", layout="centered")

# 전역 폰트 크기 및 상태 기본값 정의 (가장 먼저 수행)
if 'font_size' not in st.session_state: st.session_state.font_size = "large"
if 'mode' not in st.session_state: st.session_state.mode = "MAIN" 
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_biz' not in st.session_state: st.session_state.selected_biz = ""
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'pay_method' not in st.session_state: st.session_state.pay_method = ""
if 'bank_pass' not in st.session_state: st.session_state.bank_pass = ""

# 누적 통계용 대시보드 변수
if 'stat_total_money' not in st.session_state: st.session_state.stat_total_money = 0
if 'stat_success_count' not in st.session_state: st.session_state.stat_success_count = 0

# 송금 데이터 동적 연동용 상태 변수
if 'input_bank_name' not in st.session_state: st.session_state.input_bank_name = "농협은행"
if 'input_bank_account' not in st.session_state: st.session_state.input_bank_account = "302-1234-5678-90"
if 'input_bank_money' not in st.session_state: st.session_state.input_bank_money = "50,000"

# 고속버스 예약 연동 상태 변수
if 'bus_from' not in st.session_state: st.session_state.bus_from = ""
if 'bus_to' not in st.session_state: st.session_state.bus_to = ""
if 'bus_time' not in st.session_state: st.session_state.bus_time = ""
if 'bus_p_adult' not in st.session_state: st.session_state.bus_p_adult = 0
if 'bus_p_teen' not in st.session_state: st.session_state.bus_p_teen = 0
if 'bus_p_child' not in st.session_state: st.session_state.bus_p_child = 0
if 'bus_p_senior' not in st.session_state: st.session_state.bus_p_senior = 0
if 'bus_selected_seats' not in st.session_state: st.session_state.bus_selected_seats = []

# 동적 스타일 크기 분기
g_box_font = "28px" if st.session_state.font_size == "large" else "22px"
card_font = "24px" if st.session_state.font_size == "large" else "18px"
btn_font = "25px" if st.session_state.font_size == "large" else "19px"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #F3F4F6 !important; }}
    
    html, body, [data-testid="stWidgetLabel"] p, h1, h2, h3, p, span {{
        font-family: 'Nanum Gothic', sans-serif !important;
        color: #1F2937 !important;
    }}

    /* 스마트폰 내부 화면 형태의 프레임워크 디자인 구성 */
    .phone-container {{
        background-color: #FFFFFF !important;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border: 1px solid #E5E7EB;
        margin-bottom: 20px;
    }}

    /* 상단 프로젝트 SDGs 배너 */
    .sdgs-banner {{
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.2);
    }}
    .sdgs-banner h2 {{ color: #FFFFFF !important; margin: 0; font-size: 26px; font-weight: 800; }}
    .sdgs-badge {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin-top: 6px;
        font-weight: bold;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    /* 시각적 진행 바 */
    .step-indicator {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
        padding: 10px 20px;
        background: #F9FAFB;
        border-radius: 30px;
        border: 1px solid #E5E7EB;
    }}
    .step-dot {{ width: 12%; height: 12px; background-color: #E5E7EB; border-radius: 10px; }}
    .step-dot.active {{ background-color: #2563EB; box-shadow: 0 0 8px rgba(37, 99, 235, 0.5); }}

    /* 대형 안내 박스 - 실시간 글자크기 제어 연동 */
    .guide-box {{
        font-size: {g_box_font};
        font-weight: 800;
        color: #111827 !important;
        text-align: center;
        background-color: #EFF6FF;
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 20px;
        border: 2.5px solid #3B82F6;
        line-height: 1.6;
    }}

    /* 화려한 성과 통계 대시보드 리포트 상자 */
    .report-box {{
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 2px solid #10B981;
        padding: 20px;
        border-radius: 18px;
        margin: 20px 0;
        color: #065F46 !important;
    }}
    .report-box h4 {{ color: #065F46 !important; font-weight:800; margin-top:0; }}

    /* 정보 표시 카드 */
    .info-card {{
        background-color: #F9FAFB !important;
        padding: 16px;
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        margin-bottom: 12px;
        font-size: {card_font} !important;
        font-weight: bold;
        color: #374151 !important;
    }}

    /* 시니어 친화형 광폭 터치 버튼 */
    .stButton>button {{
        width: 100%;
        height: 74px;
        font-size: {btn_font} !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: 2px solid #D1D5DB !important;
        background-color: #FFFFFF !important;
        color: #374151 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03) !important;
        margin-bottom: 8px;
    }}
    .stButton>button div p {{ color: #374151 !important; font-weight: 800 !important; font-size: {btn_font} !important; }}
    .stButton>button:hover {{ border-color: #2563EB !important; background-color: #F3F4F6 !important; }}

    /* 핵심 동작 하이라이트 버튼 (블루 테마) */
    div.stButton>button[key*="start_btn"], div.stButton>button[key*="next_btn"], div.stButton>button[key*="pay_btn"], div.stButton>button[key*="complete_btn"] {{
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        height: 82px;
    }}
    div.stButton>button[key*="start_btn"] div p, div.stButton>button[key*="next_btn"] div p, div.stButton>button[key*="pay_btn"] div p, div.stButton>button[key*="complete_btn"] div p {{
        color: #FFFFFF !important;
    }}

    /* 금액 전용 인포 박스 */
    .price-box {{
        background-color: #FEF2F2 !important;
        color: #DC2626 !important;
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        padding: 16px;
        border-radius: 14px;
        margin: 15px 0;
        border: 2px dashed #FCA5A5;
    }}
    
    .footer-notice {{
        text-align: center;
        color: #4B5563 !important;
        font-size: 17px;
        font-weight: bold;
        margin-top: 35px;
        padding: 16px;
        background-color: #F3F4F6;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }}
    </style>
    """, unsafe_allow_html=True)

# 데이터 에셋 정보 정의
KIOSK_DATA = {
    "🍔 패스트푸드점 (논산 오거리점)": {"일반 햄버거": 5000, "치즈버거": 6000, "불고기버거": 5500, "감자튀김": 2000, "콜라": 1500},
    "☕ 커피 전문점 (탑정호 출렁다리 카페)": {"아메리카노": 3000, "카페라떼": 3500, "따뜻한 쌍화차": 4500, "생강차": 4500},
    "🛒 대형 마트 (논산 농협하나로마트)": {"국산 삼겹살 1kg": 28000, "싱싱한 바나나": 4000, "서울우유 1L": 2900, "신라면 5봉지": 4200},
    "🏥 백제병원 무인수납기": {"일반 외래 진료비": 4500, "처방전 영수증 발행": 0, "소독약 및 붕대": 2500}
}
SHOP_DATA = {
    "🍓 논산 설향 딸기 특강 특산품": 25000, "🌾 논산 삼광쌀 10kg": 35000, "🍠 연무대 꿀 고구마 5kg": 18000, "🍯 6년근 홍삼정 스틱": 55000
}
BUS_PRICE_TABLE = {"서울경부": 15000, "부산종합": 32000, "대구한진": 26000, "대전복합": 6000}

# 오디오 및 가상 연동 함수
def speak(text):
    if st.session_state.get('voice_active', True):
        js_code = f"<script>var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'ko-KR'; msg.rate = 0.9; window.speechSynthesis.speak(msg);</script>"
        st.components.v1.html(js_code, height=0)

def get_total_price():
    if st.session_state.mode == "APP":
        if st.session_state.selected_biz == "쇼핑":
            return sum(SHOP_DATA.get(name, 0) * qty for name, qty in st.session_state.cart.items())
        if st.session_state.selected_biz == "은행": 
            try:
                clean = "".join(filter(str.isdigit, str(st.session_state.input_bank_money)))
                return int(clean) if clean else 0
            except: return 50000
        if st.session_state.selected_biz == "버스":
            base = BUS_PRICE_TABLE.get(st.session_state.bus_to, 15000)
            return (st.session_state.bus_p_adult * base + st.session_state.bus_p_teen * int(base*0.8) + 
                    st.session_state.bus_p_child * int(base*0.5) + st.session_state.bus_p_senior * int(base*0.8))
        return 0
    biz = st.session_state.selected_biz
    if not biz or biz not in KIOSK_DATA: return 0
    return sum(KIOSK_DATA[biz].get(name, 0) * qty for name, qty in st.session_state.cart.items())

def reset_state():
    st.session_state.step = 1
    st.session_state.cart = {}
    st.session_state.selected_biz = ""
    st.session_state.pay_method = ""
    st.session_state.bank_pass = ""
    st.session_state.bus_from = ""
    st.session_state.bus_to = ""
    st.session_state.bus_time = ""
    st.session_state.bus_p_adult = 0
    st.session_state.bus_p_teen = 0
    st.session_state.bus_p_child = 0
    st.session_state.bus_p_senior = 0
    st.session_state.bus_selected_seats = []

# --- 👑 1. SDGs 고정 배너 명시 ---
st.markdown("""
<div class="sdgs-banner">
    <h2>논산시 노인 디지털 사회적 격차 해소 프로젝트</h2>
    <div class="sdgs-badge">UN SDGs 4: 양질의 평생 교육 보장</div>
    <div class="sdgs-badge">UN SDGs 10: 세대·지역 정보 불평등 완화</div>
</div>
""", unsafe_allow_html=True)

# --- 🔍 2. 접근성 제어 사이드바 톱니바퀴 영역 ---
with st.sidebar:
    st.header("⚙️ 스마트 가이드 설정")
    st.session_state.voice_active = st.checkbox("🔊 음성 가이드 활성화", value=True)
    f_choice = st.radio("👵 글씨 크기 선택", ["크게 보기", "보통 보기"])
    st.session_state.font_size = "large" if f_choice == "크게 보기" else "normal"
    st.markdown("---")
    st.subheader("📊 누적 모니터링 대시보드")
    st.metric("오늘 어르신 성공 횟수", f"{st.session_state.stat_success_count} 회")
    st.metric("가상 훈련 거래액", f"{st.session_state.stat_total_money:,} 원")

# --- 📱 3. 가상 폰 프레임 시작 컨테이너 ---
st.markdown('<div class="phone-container">', unsafe_allow_html=True)

# ==========================================
# 🏠 [메인 화면]
# ==========================================
if st.session_state.mode == "MAIN":
    st.markdown('<div class="guide-box">안녕하세요 어르신! 😊<br>오늘 연습하고 싶으신 기계를 터치해 주세요.</div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/grandfather-using-digital-devices-concept-illustration_114360-7053.jpg?w=500", use_container_width=True)
    
    if st.button("🏪 1. 식당/마트 무인 기계 (키오스크) 연습하기", key="btn_main_kiosk"):
        st.session_state.mode = "KIOSK"; reset_state(); speak("무인 기계 주문 연습을 시작합니다."); st.rerun()
    if st.button("📱 2. 스마트폰 앱 (농협 송금 / 고속버스 예매) 연습하기", key="btn_main_app"):
        st.session_state.mode = "APP"; reset_state(); speak("스마트폰 앱 연습을 시작합니다."); st.rerun()


# ==========================================
# 🏪 [분기 1] 매장 키오스크 모드
# ==========================================
elif st.session_state.mode == "KIOSK":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">잘못 눌러도 돈이 나가지 않으니<br>부담 없이 편하게 눌러보세요!</div>', unsafe_allow_html=True)
        if st.button("연습 시작하기 🏁", key="k_start_btn"): st.session_state.step = 2; speak("가고 싶으신 매장을 고르세요."); st.rerun()
        if st.button("🏠 메인 홈 화면으로 나가기", key="k_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습해 볼 매장을 선택해 보세요.</div>', unsafe_allow_html=True)
        for biz in KIOSK_DATA.keys():
            if st.button(biz, key=f"k_biz_{biz}"): 
                st.session_state.selected_biz = biz; st.session_state.step = 3
                speak(f"{biz}를 선택하셨습니다. 먹고 싶은 메뉴를 담아보세요."); st.rerun()
        if st.button("⬅ 뒤로가기", key="k_b2_back"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{biz}]<br>원하는 음식을 담고 [다음 단계로]를 누르세요.</div>', unsafe_allow_html=True)
        
        for name, price in KIOSK_DATA[biz].items():
            col_txt, col_btn = st.columns([3, 1])
            with col_txt: st.markdown(f'<div class="info-card">{name} ({price:,}원)</div>', unsafe_allow_html=True)
            with col_btn:
                if st.button("담기", key=f"k_add_{name}"):
                    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
                    speak(f"{name} 담기 완료"); st.rerun()
                    
        total = get_total_price()
        st.markdown(f'<div class="price-box">🛒 현재 담은 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 매장 바꾸기", key="k_b3_back"): st.session_state.step = 2; st.session_state.cart = {}; st.rerun()
        with c2:
            if st.button("다음 단계로 ➡", key="k_next_btn_3"):
                if total > 0: st.session_state.step = 4; speak("내가 담은 메뉴가 맞는지 확인해 보세요."); st.rerun()
                else: st.warning("메뉴를 하나 이상 골라주세요!")

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">장바구니 확인창<br>선택하신 물품이 맞으면 결제를 누르세요.</div>', unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            st.markdown(f'<div class="info-card">● {name} — {qty}개 ({KIOSK_DATA[st.session_state.selected_biz][name]*qty:,}원)</div>', unsafe_allow_html=True)
        
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 더 담으러 가기", key="k_b4_back"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("결제하기 ➡", key="k_pay_btn_4"): st.session_state.step = 5; speak("결제 수단을 골라주세요."); st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">어떤 방법으로 돈을 낼지 선택하세요.</div>', unsafe_allow_html=True)
        if st.button("💵 현금 결제 (지폐 투입구에 넣기)", key="k_pay_cash"):
            st.session_state.pay_method = "현금"; st.session_state.step = 7; st.rerun()
        if st.button("💳 카드 결제 (신용/체크카드 투입)", key="k_pay_card"):
            st.session_state.pay_method = "카드"; st.session_state.step = 6; speak("카드를 끝까지 투입구에 넣어주세요."); st.rerun()
        if st.button("📱 스마트폰 삼성페이 태그", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"; st.session_state.step = 6; speak("핸드폰 뒷면을 리더기에 대주세요."); st.rerun()
        if st.button("⬅ 이전으로", key="k_b5_back"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">카드를 방향에 맞춰 깊숙이 넣어주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
            if st.button("카드를 꽂았습니다 💳", key="k_complete_btn_card"): st.session_state.step = 7; st.rerun()
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">스마트폰 뒷면을 기계 중앙 카드 표시판에 대세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("스마트폰을 대었습니다 📱", key="k_complete_btn_nfc"): st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="k_b6_back"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 미션 성공! 완벽하게 주문하셨습니다.")
        total = get_total_price()
        
        # 데이터 업데이트
        st.session_state.stat_total_money += total
        st.session_state.stat_success_count += 1
        
        # 🛒 대형 마트 및 병원 무인기 전 기기 번호표 완벽 분기 수정완료
        if "마트" in st.session_state.selected_biz:
            finish_msg = f"계산이 완료되었습니다!<br>영수증을 확인하시고 카트 안의 물건을 챙기세요.<br>🧾 결제금액: {total:,}원"
        elif "병원" in st.session_state.selected_biz:
            finish_msg = f"외래 수납이 완료되었습니다!<br>나오는 <b>약국 제출용 처방전</b>을 잊지 말고 꼭 챙겨가세요.<br>🧾 수납액: {total:,}원"
        else:
            finish_msg = f"주문 완료! 전광판에 대기 번호가 뜨면 음식을 찾아가세요.<br>🧾 <b>대기 번호표와 영수증</b>을 챙기세요.<br>🧾 결제금액: {total:,}원"
            
        st.markdown(f'<div class="guide-box" style="background-color:#F0FDF4 !important; border: 3px solid #10B981;">{finish_msg}</div>', unsafe_allow_html=True)
        
        # 📈 4. 발표 극찬용 실시간 SDGs 임팩트 리포트 화면 노출
        st.markdown(f"""
        <div class="report-box">
            <h4>📊 오늘 나의 디지털 실력 성장 리포트 (SDGs 4 & 10)</h4>
            • <b>오늘의 역량 등급:</b> 디지털 실버 똑똑이 마스터 단계 등극 🏅<br>
            • <b>탄소 절감 효과:</b> 스마트 배움으로 종이 낭비 절감 기여 🌿<br>
            • <b>사회적 효과:</b> 이제 논산 오거리 매장 어디서든 소외되지 않고 자신 있게 주문할 수 있습니다!
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 처음 화면으로 돌아가기", key="k_finish_btn_home"): st.session_state.mode = "MAIN"; st.rerun()


# ==========================================
# 📱 [분기 2] 스마트폰 앱 모드
# ==========================================
elif st.session_state.mode == "APP":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">스마트폰 앱 기능을 마스터하면<br>집 안방에서도 편하게 모든 일을 볼 수 있습니다!</div>', unsafe_allow_html=True)
        if st.button("스마트폰 앱 연습 시작하기 🏁", key="a_start_btn"): st.session_state.step = 2; speak("연습하고 싶은 앱을 터치하세요."); st.rerun()
        if st.button("🏠 처음 화면으로 돌아가기", key="a_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습하실 스마트폰 가상 앱을 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("🛍️ 1. 온라인 쇼핑 앱 (논산 특산물 사이버 시장)", key="a_biz_shop"): st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; st.rerun()
        if st.button("🏦 2. NH 농협 뱅킹 앱 (자녀에게 가상 돈 보내기)", key="a_biz_bank"): st.session_state.selected_biz = "銀行" if 'selected_biz' in st.session_state and st.session_state.selected_biz == "은행" else "은행"; st.session_state.step = 3; st.rerun()
        if st.button("📅 3. 고속버스 티켓 예매 앱 (영외면회 및 역귀성용)", key="a_biz_bus"): st.session_state.selected_biz = "버스"; st.session_state.step = 3; st.rerun()
        if st.button("⬅ 뒤로가기", key="a_b2_back"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        
        if biz == "쇼핑":
            st.markdown('<div class="guide-box">🛍️ [논산 농특산물 장터]<br>사고 싶으신 싱싱한 상품을 장바구니에 담으세요.</div>', unsafe_allow_html=True)
            for name, pr in SHOP_DATA.items():
                col_txt, col_btn = st.columns([3, 1])
                with col_txt: st.markdown(f'<div class="info-card">{name} ({pr:,}원)</div>', unsafe_allow_html=True)
                with col_btn:
                    if st.button("담기", key=f"s_add_{name}"): st.session_state.cart[name] = st.session_state.cart.get(name,0)+1; st.rerun()
            total = get_total_price()
            st.markdown(f'<div class="price-box">🛒 장바구니 합계: {total:,}원</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ 뒤로가기", key="s_p_back"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
            with c2:
                if st.button("주문하기 ➡", key="next_btn_shop"):
                    if total > 0: st.session_state.step = 4; speak("주문 내역을 검토하세요."); st.rerun()
                    else: st.warning("물건을 최소 1개 이상 골라주세요.")

        elif biz == "은행" or biz == "銀行":
            st.markdown('<div class="guide-box">🏦 [NH 가상 모바일 뱅킹]<br>상대방 정보와 금액을 입력창에 적어주세요.</div>', unsafe_allow_html=True)
            
            bank_list = ["농협은행", "국민은행", "신한은행", "우리은행", "우체국"]
            try: sel_idx = bank_list.index(st.session_state.input_bank_name)
            except: sel_idx = 0
                
            # 💡 완벽한 실시간 수정 양방향 바인딩 구조 연동 완료
            st.session_state.input_bank_name = st.selectbox("1. 어디 은행으로 돈을 보낼까요?", bank_list, index=sel_idx)
            st.session_state.input_bank_account = st.text_input("2. 상대방의 계좌번호를 확인 및 수정하세요.", st.session_state.input_bank_account)
            st.session_state.input_bank_money = st.text_input("3. 송금할 금액을 적으세요 (숫자만 입력)", st.session_state.input_bank_money)
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ 이전으로", key="b_p_back"): st.session_state.step = 2; st.rerun()
            with c2: 
                if st.button("송금 확인하기 ➡", key="next_btn_bank"): 
                    st.session_state.step = 4; speak("내가 입력한 정보가 정확히 맞는지 다음 화면에서 확인하세요.")
                    st.rerun()

        elif biz == "버스":
            st.markdown('<div class="guide-box">🚍 [논산 육군훈련소 영외면회 및 가족 방문용]<br>출발지와 목적지 터미널을 각각 터치해 주세요.</div>', unsafe_allow_html=True)
            
            st.write("📍 **1. 버스를 타실 출발지를 선택하세요**")
            from_list = ["논산금호시외", "연무대터미널", "대전복합", "서울경부"]
            c_f = st.columns(len(from_list))
            for idx, f_name in enumerate(from_list):
                if c_f[idx].button(f_name, key=f"f_{f_name}"): st.session_state.bus_from = f_name; st.rerun()
            
            st.write("📍 **2. 내리실 목적지를 선택하세요**")
            to_list = ["서울경부", "부산종합", "대구한진", "대전복합"]
            c_t = st.columns(len(to_list))
            for idx, t_name in enumerate(to_list):
                if c_t[idx].button(t_name, key=f"t_{t_name}"): st.session_state.bus_to = t_name; st.rerun()

            st.info(f"👉 현재 여정: [ {st.session_state.bus_from if st.session_state.bus_from else '...'} ] 출발 ➡ [ {st.session_state.bus_to if st.session_state.bus_to else '...'} ] 도착")

            if st.session_state.bus_from and st.session_state.bus_to:
                st.write("⏰ **3. 버스 시간을 정하세요**")
                time_list = ["08:00 (오전)", "11:20 (오전)", "14:50 (오후)", "18:10 (오후)"]
                c_time = st.columns(len(time_list))
                for idx, t_val in enumerate(time_list):
                    if c_time[idx].button(t_val, key=f"time_{idx}"): st.session_state.bus_time = t_val; st.rerun()
                
                if st.session_state.bus_time:
                    st.success(f"선택 완료: {st.session_state.bus_from} 에서 {st.session_state.bus_to}행 버스 ({st.session_state.bus_time})")
                    if st.button("인원수 정하러 가기 ➡", key="next_btn_bus_s1"): st.session_state.step = 10; speak("몇 분이 탑승하시는지 지정하세요."); st.rerun()

            if st.button("🔄 처음부터 다시 지정", key="bus_reset_all"): reset_state(); st.session_state.selected_biz="버스"; st.rerun()

    # --- [버스 인원 지정 단계] ---
    elif st.session_state.step == 10:
        st.markdown('<div class="guide-box">🚍 [탑승 인원수 체크]<br>추가하려면 ➕ 버튼을, 빼려면 ➖ 버튼을 누르세요.</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**어른**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_adult}명</h3>", unsafe_allow_html=True)
            if st.button("➕", key="pa_up"): st.session_state.bus_p_adult += 1; st.rerun()
            if st.button("➖", key="pa_dn"): st.session_state.bus_p_adult = max(0, st.session_state.bus_p_adult - 1); st.rerun()
        with col2:
            st.markdown("**청소년**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_teen}명</h3>", unsafe_allow_html=True)
            if st.button("➕", key="pt_up"): st.session_state.bus_p_teen += 1; st.rerun()
            if st.button("➖", key="pt_dn"): st.session_state.bus_p_teen = max(0, st.session_state.bus_p_teen - 1); st.rerun()
        with col3:
            st.markdown("**어린이**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_child}명</h3>", unsafe_allow_html=True)
            if st.button("➕", key="pc_up"): st.session_state.bus_p_child += 1; st.rerun()
            if st.button("➖", key="pc_dn"): st.session_state.bus_p_child = max(0, st.session_state.bus_p_child - 1); st.rerun()
        with col4:
            st.markdown("**어르신(우대)**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_senior}명</h3>", unsafe_allow_html=True)
            if st.button("➕", key="ps_up"): st.session_state.bus_p_senior += 1; st.rerun()
            if st.button("➖", key="ps_dn"): st.session_state.bus_p_senior = max(0, st.session_state.bus_p_senior - 1); st.rerun()

        total_p = st.session_state.bus_p_adult + st.session_state.bus_p_teen + st.session_state.bus_p_child + st.session_state.bus_p_senior
        st.markdown(f"<div class='info-card' style='text-align:center;'>체크된 승객 총 인원: {total_p}명</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 시간 다시 정하기", key="b_to_s3"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("의자 자리 고르기 ➡", key="next_btn_bus_seat"):
                if total_p > 0: st.session_state.step = 11; speak("원하시는 버스 의자 자리를 인원수만큼 누르세요."); st.rerun()
                else: st.warning("최소 한 명 이상 선택하셔야 합니다!")

    # --- [버스 좌석표 배치도] ---
    elif st.session_state.step == 11:
        total_need = st.session_state.bus_p_adult + st.session_state.bus_p_teen + st.session_state.bus_p_child + st.session_state.bus_p_senior
        st.markdown('<div class="guide-box">🚍 [3단계: 원하는 좌석 번호 지정]<br>💺 모양의 빈자리를 누르세요.<br>(선택 완료: {} / {}석)</div>'.format(len(st.session_state.bus_selected_seats), total_need), unsafe_allow_html=True)
        
        st.write("🚍 버스 앞쪽 (운전석 방향)")
        fixed_sold = [2, 5, 11, 19] # 선점 좌석
        
        for row in range(1, 10):
            cols = st.columns(4)
            
            s1 = (row - 1) * 3 + 1
            if s1 <= 28:
                if s1 in fixed_sold: cols[0].button(f"❌ {s1:02d}", key=f"s_{s1}", disabled=True)
                elif s1 in st.session_state.bus_selected_seats:
                    if cols[0].button(f"⭐ {s1:02d}", key=f"s_{s1}"): st.session_state.bus_selected_seats.remove(s1); st.rerun()
                else:
                    if cols[0].button(f"💺 {s1:02d}", key=f"s_{s1}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s1); st.rerun()
                        else: st.warning("이미 자리를 모두 정하셨습니다.")
                        
            s2 = (row - 1) * 3 + 2
            if s2 <= 28:
                if s2 in fixed_sold: cols[1].button(f"❌ {s2:02d}", key=f"s_{s2}", disabled=True)
                elif s2 in st.session_state.bus_selected_seats:
                    if cols[1].button(f"⭐ {s2:02d}", key=f"s_{s2}"): st.session_state.bus_selected_seats.remove(s2); st.rerun()
                else:
                    if cols[1].button(f"💺 {s2:02d}", key=f"s_{s2}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s2); st.rerun()
                        else: st.warning("이미 자리를 모두 정하셨습니다.")
            
            cols[2].write("") # 통로 구조
            
            s3 = (row - 1) * 3 + 3
            if s3 <= 28:
                if s3 in fixed_sold: cols[3].button(f"❌ {s3:02d}", key=f"s_{s3}", disabled=True)
                elif s3 in st.session_state.bus_selected_seats:
                    if cols[3].button(f"⭐ {s3:02d}", key=f"s_{s3}"): st.session_state.bus_selected_seats.remove(s3); st.rerun()
                else:
                    if cols[3].button(f"💺 {s3:02d}", key=f"s_{s3}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s3); st.rerun()
                        else: st.warning("이미 자리를 모두 정하셨습니다.")

        st.markdown(f"<div class='price-box'>💵 승차권 가격 합계: {get_total_price():,}원</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 승객 인원 변경", key="b_to_s10"): st.session_state.bus_selected_seats = []; st.session_state.step = 10; st.rerun()
        with c2:
            if st.button("예약 내역 확인 ➡", key="next_btn_bus_done"):
                if len(st.session_state.bus_selected_seats) == total_need: st.session_state.step = 4; speak("마지막 신청 정보를 검토하세요."); st.rerun()
                else: st.error(f"지정하신 인원수에 맞게 좌석을 {total_need}개 다 고르셔야 합니다.")

    # --- [스마트폰 앱 최종 신청 내역 확인창] ---
    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 신청한 화면의 정보가 정확히 맞는지 최종 확인하세요.</div>', unsafe_allow_html=True)
        
        if st.session_state.selected_biz == "버스":
            st.markdown(f"""
            <div class='info-card'>
                🚌 모바일 고속버스 승차권 정보<br>
                • <b>여정:</b> {st.session_state.bus_from} 출발 ➡ {st.session_state.bus_to} 도착<br>
                • <b>시각:</b> {st.session_state.bus_time}<br>
                • <b>지정석:</b> {", ".join([f"{x}번 좌석" for x in st.session_state.bus_selected_seats])}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.selected_biz == "쇼핑":
            for name, qty in st.session_state.cart.items():
                st.markdown(f'<div class="info-card">● {name} — {qty}개 ({SHOP_DATA[name]*qty:,}원)</div>', unsafe_allow_html=True)
        elif "은행" in str(st.session_state.selected_biz):
            # 💡 수정 반영 누락 버그 완벽해결: 전 장에서 바인딩된 수정 계좌/은행이 실시간 연동되어 출력됩니다.
            try: display_money = int("".join(filter(str.isdigit, str(st.session_state.input_bank_money))))
            except: display_money = 50000
            st.markdown(f"""
            <div class='info-card'>
                🏦 NH 스마트 뱅킹 이체 내역 확인<br>
                • <b>받는 기관:</b> {st.session_state.input_bank_name}<br>
                • <b>계좌 번호:</b> {st.session_state.input_bank_account}<br>
                • <b>이체 금액:</b> <span style='color:#DC2626;'>{display_money:,}원</span>
            </div>
            """, unsafe_allow_html=True)

        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 처리 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 수정하러 돌아가기", key="a_b4_back"): 
                sv = st.session_state.selected_biz
                reset_state(); st.session_state.selected_biz = sv; st.session_state.step = 3; st.rerun()
        with c2:
            if "은행" in str(st.session_state.selected_biz):
                if st.button("비밀번호 입력하기 🔑", key="next_btn_pass"): st.session_state.step = 8; speak("보안 비밀번호 6자리를 누르세요."); st.rerun()
            else:
                if st.button("결제하기 ➡", key="pay_btn_app4"): st.session_state.step = 5; speak("결제 방식을 고르세요."); st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">핸드폰 온라인 결제 수단을 고르세요.</div>', unsafe_allow_html=True)
        if st.button("🏦 내 통장에서 바로 빠져나가는 계좌이체", key="a_pay_bank"): st.session_state.pay_method = "계좌이체"; st.session_state.step = 9; st.rerun()
        if st.button("💳 카드 번호 입력 결제", key="a_pay_card"): st.session_state.pay_method = "카드"; st.session_state.step = 6; speak("가상 카드 번호를 채워주세요."); st.rerun()
        if st.button("⬅ 이전으로", key="a_b5_back"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        st.markdown('<div class="guide-box">💳 [카드 번호 안전 입력]<br>카드 번호를 안전하게 가상으로 채운 뒤 승인을 누르세요.</div>', unsafe_allow_html=True)
        st.text_input("신용카드/체크카드 16자리 예시 입력창", "9410 - 4567 - **** - ****")
        st.text_input("비밀번호 앞 2자리", type="password")
        if st.button("안전 결제 승인 완료 🔒", key="complete_btn_app_card"): st.session_state.step = 7; speak("스마트폰 미션에 훌륭하게 성공하셨습니다."); st.rerun()
        if st.button("⬅ 이전으로", key="a_b6_back"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 미션 최종 성공! 완벽하게 다루셨습니다.")
        total = get_total_price()
        
        # 데이터 대시보드 저장
        st.session_state.stat_total_money += total
        st.session_state.stat_success_count += 1
        
        # 📱 마트와 스마트폰 전 구역 내 번호표 챙겨가라는 어색한 지시문 완전 삭제 분기 처리 완비
        st.markdown(f"""
        <div class="guide-box" style="background-color:#F0FDF4 !important; border: 3px solid #10B981;">
            참 잘하셨습니다 어르신! 👏<br>
            스마트폰 처리가 완료되었습니다. 지갑이나 종이 표를 따로 안 뽑으셔도 핸드폰 안에 안전하게 보관되어 있습니다.<br>
            🧾 최종 전송/이체액: {total:,}원
        </div>
        """, unsafe_allow_html=True)
        
        # 📊 실시간 SDGs 통계 리포트 피드백 화면
        st.markdown(f"""
        <div class="report-box">
            <h4>📊 오늘 나의 디지털 실력 성장 리포트 (SDGs 4 & 10)</h4>
            • <b>오늘의 역량 등급:</b> 모바일 금융/스마트 쇼핑 챔피언 단계 등극 🏆<br>
            • <b>불평등 해소 지표:</b> 은행 지점이나 터미널에 줄을 서지 않고 스스로 해결할 수 있습니다!<br>
            • <b>포용적 사회 기여:</b> 디지털 기술 발전에서 소외되지 않는 당당한 스마트 시니어가 되셨습니다.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 처음 메인 홈 화면으로 이동하기", key="a_fin_btn_home"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 8:
        try: target_money = int("".join(filter(str.isdigit, str(st.session_state.input_bank_money))))
        except: target_money = 50000
            
        st.markdown(f'<div class="guide-box">🔑 [금융 암호 입력]<br>{st.session_state.input_bank_name}으로 {target_money:,}원을 송금합니다.<br>비밀번호 숫자 6자리를 차례대로 터치하세요.</div>', unsafe_allow_html=True)
        stars = " ".join(["★" for _ in st.session_state.bank_pass]) + " " + " ".join(["☆" for _ in range(6 - len(st.session_state.bank_pass))])
        st.markdown(f"<h1 style='text-align:center; color:#2563EB; letter-spacing: 5px;'>{stars}</h1>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i in range(1, 10):
            if cols[(i-1)%3].button(str(i), key=f"num_{i}"): st.session_state.bank_pass += str(i); st.rerun()
        if st.columns(3)[1].button("0", key="num_0"): st.session_state.bank_pass += "0"; st.rerun()
        
        if len(st.session_state.bank_pass) >= 6: st.session_state.pay_method = "은행"; st.session_state.step = 7; speak("통장에서 돈이 안전하게 전송되었습니다."); st.rerun()
        if st.button("❌ 번호 잘못 눌렀음 (다시 치기)", key="num_clear"): st.session_state.bank_pass = ""; st.rerun()

    elif st.session_state.step == 9:
        st.markdown('<div class="guide-box">내 은행 계좌가 맞는지 확인 후 승인을 누르세요.</div>', unsafe_allow_html=True)
        st.selectbox("출금 통장 은행 선택", ["농협은행 (논산 시청지점)", "우체국"])
        st.text_input("내 계좌번호 예시", "302-5678-****")
        if st.button("안전 이체 최종 승인 🔒", key="complete_btn_app_tr"): st.session_state.step = 7; speak("안전하게 전송 처리되었습니다."); st.rerun()
        if st.button("⬅ 이전으로", key="a_b9_back"): st.session_state.step = 5; st.rerun()

st.markdown('</div>', unsafe_allow_html=True) # 가상 스마트폰 프레임 종료 컨테이너

# --- ⚠️ 모든 연습 화면 하단 안심 가이드 상시 고정 배정 ---
st.markdown('<div class="footer-notice">⚠️ 안심 팁: 이 앱은 교육을 위해 만들어진 모의 프로그램입니다. 가상의 돈으로 연습하는 것이니 실수가 나와도 절대 실제 돈이 나가지 않습니다. 마음껏 눌러보세요!</div>', unsafe_allow_html=True)
