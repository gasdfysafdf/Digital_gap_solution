import streamlit as st

# 1. 페이지 기본 설정 및 시니어 맞춤형 프리미엄 라이트 테마 강제 정의
st.set_page_config(page_title="디지털 친구 v11.0 - 논산시 실버 디지털 문해 교육 앱", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경을 따뜻하고 편안한 느낌의 실버 전용 밝은 톤으로 세팅 */
    .stApp { background-color: #F8F9FA !important; }
    
    html, body, [data-testid="stWidgetLabel"] p, h1, h2, h3, p, span {
        font-family: 'Nanum Gothic', sans-serif !important;
        color: #1A202C !important;
    }

    /* 상단 프로젝트 SDGs 아이덴티티 배너 */
    .sdgs-banner {
        background: linear-gradient(135deg, #4C51BF 0%, #2B6CB0 100%);
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(76, 81, 191, 0.2);
    }
    .sdgs-banner h2 { color: #FFFFFF !important; margin: 0; font-size: 28px; font-weight: 800; }
    .sdgs-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        margin-top: 8px;
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    /* 상단 진행 단계 표시바 디자인 업그레이드 */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
        padding: 10px 20px;
        background: #FFFFFF;
        border-radius: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        border: 1px solid #E2E8F0;
    }
    .step-dot { width: 12%; height: 14px; background-color: #E2E8F0; border-radius: 10px; transition: all 0.3s ease; }
    .step-dot.active { background-color: #4C51BF; box-shadow: 0 0 10px rgba(76, 81, 191, 0.5); }

    /* 대형 알림 가이드 박스 - 시인성 극대화 */
    .guide-box {
        font-size: 26px;
        font-weight: 800;
        color: #2D3748 !important;
        text-align: center;
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 3px solid #4C51BF;
        line-height: 1.6;
    }

    /* 흰색 정보 카드 (글자 크기 22px로 확장) */
    .info-card {
        background-color: #FFFFFF !important;
        padding: 18px;
        border-radius: 14px;
        border: 2px solid #E2E8F0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
        margin-bottom: 15px;
        font-size: 22px !important;
        font-weight: bold;
        color: #2D3748 !important;
    }

    /* 일반 선택 버튼 스타일 (모바일 터치 및 노인 신체 특성 고려 대형화) */
    .stButton>button {
        width: 100%;
        height: 75px;
        font-size: 24px !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: 2.5px solid #CBD5E0 !important;
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .stButton>button div p { color: #2D3748 !important; font-weight: 800 !important; font-size: 24px !important; }
    .stButton>button:hover { border-color: #4C51BF !important; background-color: #F7FAFC !important; }

    /* 핵심 진행용 다이렉트 버튼 (선명한 보라색 하이라이트) */
    div.stButton>button[key*="start_btn"], div.stButton>button[key*="next_btn"], div.stButton>button[key*="pay_btn"], div.stButton>button[key*="complete_btn"] {
        background: #4C51BF !important;
        color: #FFFFFF !important;
        border: none !important;
        height: 85px;
        font-size: 26px !important;
        box-shadow: 0 8px 16px rgba(76, 81, 191, 0.3) !important;
    }
    div.stButton>button[key*="start_btn"] div p, div.stButton>button[key*="next_btn"] div p, div.stButton>button[key*="pay_btn"] div p, div.stButton>button[key*="complete_btn"] div p {
        color: #FFFFFF !important;
        font-size: 26px !important;
    }

    /* 가격 표시 상자 (빨간색 경고 및 집중 톤) */
    .price-box {
        background-color: #FFF5F5 !important;
        color: #C53030 !important;
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        padding: 18px;
        border-radius: 16px;
        margin: 20px 0;
        border: 2px dashed #FEB2B2;
    }
    
    /* 하단 안심 팁 바 */
    .footer-notice {
        text-align: center;
        color: #4A5568 !important;
        font-size: 18px;
        font-weight: bold;
        margin-top: 40px;
        padding: 18px;
        background-color: #EDF2F7;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 전역 상태 관리 변수 및 입력 폼 변수 초기화
if 'mode' not in st.session_state: st.session_state.mode = "MAIN" 
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_biz' not in st.session_state: st.session_state.selected_biz = ""
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'pay_method' not in st.session_state: st.session_state.pay_method = ""
if 'bank_pass' not in st.session_state: st.session_state.bank_pass = ""

# 모바일 송금 데이터 동적 연동용 상태 변수 안정화
if 'input_bank_name' not in st.session_state: st.session_state.input_bank_name = "농협은행"
if 'input_bank_account' not in st.session_state: st.session_state.input_bank_account = "302-1234-5678-90"
if 'input_bank_money' not in st.session_state: st.session_state.input_bank_money = "50,000"

# --- 고속버스 예약 연동 상태 변수 ---
if 'bus_from' not in st.session_state: st.session_state.bus_from = ""
if 'bus_to' not in st.session_state: st.session_state.bus_to = ""
if 'bus_time' not in st.session_state: st.session_state.bus_time = ""
if 'bus_p_adult' not in st.session_state: st.session_state.bus_p_adult = 0
if 'bus_p_teen' not in st.session_state: st.session_state.bus_p_teen = 0
if 'bus_p_child' not in st.session_state: st.session_state.bus_p_child = 0
if 'bus_p_senior' not in st.session_state: st.session_state.bus_p_senior = 0
if 'bus_selected_seats' not in st.session_state: st.session_state.bus_selected_seats = []

# 데이터 허브 (로컬라이징 반영)
KIOSK_DATA = {
    "🍔 패스트푸드점 (논산 오거리점)": {"일반 햄버거": 5000, "치즈버거": 6000, "불고기버거": 5500, "감자튀김": 2000, "콜라": 1500, "치킨너겟": 3000},
    "☕ 커피 전문점 (탑정호 카페)": {"아메리카노": 3000, "카페라떼": 3500, "따뜻한 쌍화차": 4500, "생강차": 4500, "단팥빵": 2500},
    "🛒 대형 마트 (논산 하나로마트)": {"국산 삼겹살 1kg": 28000, "싱싱한 바나나": 4000, "서울우유 1L": 2900, "신라면 5봉지": 4200},
    "🏥 백제병원 수납기 / 약국": {"일반 진료비 수납": 4500, "처방전 발행": 0, "빨간약 소독제": 2000, "마시는 감기약": 1000}
}

SHOP_DATA = {
    "🌾 논산 삼광쌀 10kg": 35000, "🍓 논산 설향 딸기 세트": 25000, "🍠 가정용 꿀 고구마 5kg": 18000,
    "🍎 상주 꿀사과 1박스": 29000, "🍊 영동 곶감 세트": 32000, "🍯 6년근 홍삼정 스틱": 55000
}

BUS_PRICE_TABLE = {
    "부산종합": 36000, "대구한진": 28000, "울산": 32000, "전주": 20000, "강릉": 23000
}

# 3. 오디오 제어 및 전역 유틸리티 함수
def speak(text):
    if st.session_state.get('voice_active', True):
        js_code = f"<script>var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'ko-KR'; msg.rate = 0.88; window.speechSynthesis.speak(msg);</script>"
        st.components.v1.html(js_code, height=0)

def get_total_price():
    if st.session_state.mode == "APP":
        if st.session_state.selected_biz == "쇼핑":
            return sum(SHOP_DATA.get(name, 0) * qty for name, qty in st.session_state.cart.items())
        if st.session_state.selected_biz == "은행": 
            try:
                clean_money = "".join(filter(str.isdigit, str(st.session_state.input_bank_money)))
                return int(clean_money) if clean_money else 0
            except:
                return 50000
        if st.session_state.selected_biz == "버스":
            base = BUS_PRICE_TABLE.get(st.session_state.bus_to, 25000)
            return (st.session_state.bus_p_adult * base + 
                    st.session_state.bus_p_teen * int(base * 0.8) + 
                    st.session_state.bus_p_child * int(base * 0.5) + 
                    st.session_state.bus_p_senior * int(base * 0.8))
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
    st.session_state.input_bank_name = "농협은행"
    st.session_state.input_bank_account = "302-1234-5678-90"
    st.session_state.input_bank_money = "50,000"
    st.session_state.bus_from = ""
    st.session_state.bus_to = ""
    st.session_state.bus_time = ""
    st.session_state.bus_p_adult = 0
    st.session_state.bus_p_teen = 0
    st.session_state.bus_p_child = 0
    st.session_state.bus_p_senior = 0
    st.session_state.bus_selected_seats = []

def draw_step_bar(current_step):
    html = '<div class="step-indicator">'
    for i in range(1, 8):
        active_class = "active" if i <= current_step else ""
        html += f'<div class="step-dot {active_class}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- 👑 상단 가치 어필 SDGs 헤더 고정 배치 ---
st.markdown("""
<div class="sdgs-banner">
    <h2>논산시 실버 대면 디지털 격차 해소 프로젝트</h2>
    <div class="sdgs-badge">SDGs 목표 4: 양질의 평생 교육 보장</div>
    <div class="sdgs-badge">SDGs 목표 10: 세대·지역간 불평등 완화</div>
</div>
""", unsafe_allow_html=True)

# 발표장 스피커 제어용 토글 스위치 사이드바/상단 배치
st.session_state.voice_active = st.toggle("🔊 성우 음성 가이드 시스템 켜기", value=True)


# ==========================================
# 🏠 [메인 홈 화면]
# ==========================================
if st.session_state.mode == "MAIN":
    st.markdown('<div class="guide-box">👵 논산 어르신을 위한 맞춤형 디지털 친구 👴<br>공부하고 싶으신 기기를 선택해 보세요.</div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/grandfather-using-digital-devices-concept-illustration_114360-7053.jpg?w=500", use_container_width=True)
    
    if st.button("🏪 1. 매장 기계 (키오스크) 주문 연습하기", key="btn_main_kiosk"):
        st.session_state.mode = "KIOSK"; reset_state(); speak("매장 기계 주문 연습을 시작합니다."); st.rerun()
    if st.button("📱 2. 스마트폰 앱 (쇼핑/농협 송금/버스 예약) 연습하기", key="btn_main_app"):
        st.session_state.mode = "APP"; reset_state(); speak("스마트폰 앱 연습을 시작합니다."); st.rerun()


# ==========================================
# 🛑 [분기 1] 매장 키오스크 모드
# ==========================================
elif st.session_state.mode == "KIOSK":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">실제 가게에 있는 기계 화면과 똑같이<br>연습해 보는 공간입니다. 안심하고 누르세요!</div>', unsafe_allow_html=True)
        if st.button("연습 시작하기 🏁", key="k_start_btn"): st.session_state.step = 2; speak("연습 장소를 골라보세요."); st.rerun()
        if st.button("🏠 처음 메인 화면으로 돌아가기", key="k_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">가상으로 방문하실 장소를 터치하세요.</div>', unsafe_allow_html=True)
        for biz in KIOSK_DATA.keys():
            if st.button(biz, key=f"k_biz_{biz}"): 
                st.session_state.selected_biz = biz
                st.session_state.step = 3
                speak(f"{biz} 선택 완료. 메뉴를 장바구니에 담아보세요.")
                st.rerun()
        if st.button("⬅ 뒤로가기", key="k_b2_back"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{biz}]<br>원하는 항목을 누르고 아래의 [다음 단계로]를 누르세요.</div>', unsafe_allow_html=True)
        
        for name, price in KIOSK_DATA[biz].items():
            col_txt, col_btn = st.columns([3, 1])
            with col_txt: st.markdown(f'<div class="info-card"><span>{name} ({price:,}원)</span></div>', unsafe_allow_html=True)
            with col_btn:
                if st.button("담기", key=f"k_add_{name}"):
                    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
                    speak(f"{name} 한 개 담았습니다."); st.rerun()
                    
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 현재 장바구니 총 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 장소 다시 고르기", key="k_b3_back"): 
                st.session_state.step = 2
                st.session_state.cart = {}
                st.rerun()
        with c2:
            if st.button("다음 단계로 ➡", key="k_next_btn_3"):
                if total > 0: 
                    st.session_state.step = 4
                    speak("주문 내용을 최종 확인하세요.")
                    st.rerun()
                else: st.warning("메뉴를 하나 이상 골라주셔야 합니다!")

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 고른 메뉴 확인창<br>선택 내역을 확인하고 맞으면 결제를 누르세요.</div>', unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            st.markdown(f'<div class="info-card"><span>● {name} — {qty}개 ({KIOSK_DATA[st.session_state.selected_biz][name]*qty:,}원)</span></div>', unsafe_allow_html=True)
        
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제할 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 메뉴 다시 담기", key="k_b4_back"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("돈 내러 가기 (결제) ➡", key="k_pay_btn_4"): 
                st.session_state.step = 5
                speak("결제 방식을 선택하세요.")
                st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">결제 수단을 손가락으로 가볍게 누르세요.</div>', unsafe_allow_html=True)
        if st.button("💵 현금 결제 (지폐나 동전 투입)", key="k_pay_cash"):
            st.session_state.pay_method = "현금"; st.session_state.step = 7; speak("현금 결제가 완료되었습니다."); st.rerun()
        if st.button("💳 카드 결제 (신용/체크카드)", key="k_pay_card"):
            st.session_state.pay_method = "카드"; st.session_state.step = 6; speak("카드를 투입구에 꽂아주세요."); st.rerun()
        if st.button("📱 스마트폰 삼성페이 / 간편 태그", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"; st.session_state.step = 6; speak("스마트폰 뒷면을 기계에 대어 주세요."); st.rerun()
        if st.button("⬅ 이전으로", key="k_b5_back"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">카드를 그림처럼 투입구 끝까지 꽂아주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
            if st.button("카드를 꽂았습니다 💳", key="k_complete_btn_card"): st.session_state.step = 7; speak("성공적으로 처리되었습니다."); st.rerun()
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">스마트폰 뒷면을 리더기 기계 중앙에 대어 주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("스마트폰을 대었습니다 📱", key="k_complete_btn_nfc"): st.session_state.step = 7; speak("성공적으로 처리되었습니다."); st.rerun()
        if st.button("⬅ 이전으로", key="k_b6_back"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 축하합니다! 대면 기기 주문 성공")
        total = get_total_price()
        
        # 🛒 대형 마트 및 약국 분기 처리 고도화 (마트에는 번호표 무제거 오류 완벽 해결!)
        if "마트" in st.session_state.selected_biz:
            finish_msg = f"계산이 영리하게 완료되었습니다!<br>카트 안의 물건과 출력된 <b>종이 영수증</b>을 챙겨 가세요.<br>🧾 총 결제액: {total:,}원"
        elif "병원" in st.session_state.selected_biz:
            finish_msg = f"수납 처리가 끝났습니다!<br>기계 하단에서 <b>처방전</b>과 영수증을 반드시 받아 가세요.<br>🧾 총 수납액: {total:,}원"
        else:
            finish_msg = f"주문 완료! 주방 전광판에 내 번호가 뜨면 음식을 타가세요.<br>🧾 <b>영수증과 대기 번호표</b>를 뽑아가세요.<br>🧾 총 결제액: {total:,}원"
            
        st.markdown(f'<div class="guide-box" style="background-color:#E6FFFA !important; border: 3px solid #319795;">{finish_msg}</div>', unsafe_allow_html=True)
        if st.button("🏠 처음 메인 홈 화면으로 가기", key="k_finish_btn_home"): st.session_state.mode = "MAIN"; st.rerun()


# ==========================================
# 🛑 [분기 2] 스마트폰 앱 모드
# ==========================================
elif st.session_state.mode == "APP":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">스마트폰 앱을 켜서 장을 보거나<br>자녀에게 용돈을 송금하는 법을 연습해 봅시다!</div>', unsafe_allow_html=True)
        if st.button("스마트폰 앱 연습 시작하기 🏁", key="a_start_btn"): st.session_state.step = 2; speak("기능을 선택하세요."); st.rerun()
        if st.button("🏠 처음 화면으로 돌아가기", key="a_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습해 볼 스마트폰 기능을 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("🛍️ 1. 온라인 쇼핑몰 (논산 특산물 사이버 장보기)", key="a_biz_shop"): st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; speak("인터넷 쇼핑몰 장보기 단계입니다."); st.rerun()
        if st.button("🏦 2. 모바일 뱅킹 (스마트폰으로 안전하게 돈 보내기)", key="a_biz_bank"): st.session_state.selected_biz = "은행"; st.session_state.step = 3; speak("송금 정보를 채워주세요."); st.rerun()
        if st.button("📅 3. 고속버스 스마트 예매 (자녀 집 방문용)", key="a_biz_bus"): st.session_state.selected_biz = "버스"; st.session_state.step = 3; speak("출발지와 도착지를 골라주세요."); st.rerun()
        if st.button("⬅ 뒤로가기", key="a_b2_back"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        
        if biz == "쇼핑":
            st.markdown('<div class="guide-box">🛍️ [인터넷 쇼핑몰]<br>원하는 산지직송 논산 농산물을 장바구니에 담으세요.</div>', unsafe_allow_html=True)
            for name, pr in SHOP_DATA.items():
                col_txt, col_btn = st.columns([3, 1])
                with col_txt: st.markdown(f'<div class="info-card"><span>{name} ({pr:,}원)</span></div>', unsafe_allow_html=True)
                with col_btn:
                    if st.button("담기", key=f"s_add_{name}"): st.session_state.cart[name] = st.session_state.cart.get(name,0)+1; st.rerun()
            total = get_total_price()
            st.markdown(f'<div class="price-box">🛒 현재 장바구니 합계: {total:,}원</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ 뒤로가기", key="s_p_back"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
            with c2:
                if st.button("주문하러 가기 ➡", key="next_btn_shop"):
                    if total > 0: st.session_state.step = 4; speak("주문 내역을 검토하세요."); st.rerun()
                    else: st.warning("물건을 최소 1개 이상 담아주세요.")

        elif biz == "은행":
            st.markdown('<div class="guide-box">🏦 [스마트폰 송금 입력]<br>수정한 정보는 다음 확인 화면에 정확히 반영됩니다.</div>', unsafe_allow_html=True)
            
            bank_list = ["농협은행", "국민은행", "신한은행", "우리은행", "우체국"]
            try: sel_idx = bank_list.index(st.session_state.input_bank_name)
            except: sel_idx = 0
                
            # 💡 입력 필드에 사용자가 작성한 내역이 실시간으로 동적 갱신되도록 수식 연동 체계 구축 완비!
            st.session_state.input_bank_name = st.selectbox("1. 돈을 받을 상대방의 은행을 고르세요.", bank_list, index=sel_idx)
            st.session_state.input_bank_account = st.text_input("2. 상대방의 계좌번호를 누르세요.", st.session_state.input_bank_account)
            st.session_state.input_bank_money = st.text_input("3. 얼마를 보낼까요? (숫자만 입력)", st.session_state.input_bank_money)
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ 이전으로", key="b_p_back"): st.session_state.step = 2; st.rerun()
            with c2: 
                if st.button("송금 확인하기 ➡", key="next_btn_bank"): 
                    st.session_state.step = 4; speak("입력한 이체 정보가 맞는지 최종 확인하세요.")
                    st.rerun()

        elif biz == "버스":
            st.markdown('<div class="guide-box">🚍 [1단계: 터미널 및 시간 선택]<br>출발지, 도착지, 시간을 각각 골라주세요.</div>', unsafe_allow_html=True)
            
            st.write("📍 **1. 출발 터미널을 고르세요 (우리 지역)**")
            from_list = ["논산시외", "연무대종합", "대전복합", "서울경부"]
            c_f = st.columns(len(from_list))
            for idx, f_name in enumerate(from_list):
                if c_f[idx].button(f_name, key=f"f_{f_name}"): st.session_state.bus_from = f_name; st.rerun()
            
            st.write("📍 **2. 도착 터미널을 고르세요**")
            to_list = ["서울경부", "부산종합", "대구한진", "대전복합"]
            c_t = st.columns(len(to_list))
            for idx, t_name in enumerate(to_list):
                if c_t[idx].button(t_name, key=f"t_{t_name}"): st.session_state.bus_to = t_name; st.rerun()

            st.info(f"👉 나의 여정 선택: [ {st.session_state.bus_from if st.session_state.bus_from else '...'} ] 출발 ➡ [ {st.session_state.bus_to if st.session_state.bus_to else '...'} ] 도착")

            if st.session_state.bus_from and st.session_state.bus_to:
                st.write("⏰ **3. 고속버스 탑승 시간을 선택하세요**")
                time_list = ["08:30 (오전)", "10:15 (오전)", "14:00 (오후)", "17:45 (오후)"]
                c_time = st.columns(len(time_list))
                for idx, t_val in enumerate(time_list):
                    if c_time[idx].button(t_val, key=f"time_{idx}"): st.session_state.bus_time = t_val; st.rerun()
                
                if st.session_state.bus_time:
                    st.success(f"노선 확정: {st.session_state.bus_from} ➡ {st.session_state.bus_to} ({st.session_state.bus_time})")
                    if st.button("인원 및 좌석 선택하러 가기 ➡", key="next_btn_bus_s1"): st.session_state.step = 10; speak("몇 명이 탑승하시나요?"); st.rerun()

            if st.button("🔄 처음부터 다시 선택", key="bus_reset_all"): reset_state(); st.session_state.selected_biz="버스"; st.rerun()

    # --- [버스 상세 인원수 설정 단계] ---
    elif st.session_state.step == 10:
        st.markdown('<div class="guide-box">🚍 [2단계: 탑승 인원 설정]<br>함께 동행할 가족의 연령별 인원수를 체크하세요.</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**어른 (성인)**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_adult}명</h3>", unsafe_allow_html=True)
            if st.button("➕ 추가", key="pa_up"): st.session_state.bus_p_adult += 1; st.rerun()
            if st.button("➖ 감소", key="pa_dn"): st.session_state.bus_p_adult = max(0, st.session_state.bus_p_adult - 1); st.rerun()
        with col2:
            st.markdown("**청소년**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_teen}명</h3>", unsafe_allow_html=True)
            if st.button("➕ 추가", key="pt_up"): st.session_state.bus_p_teen += 1; st.rerun()
            if st.button("➖ 감소", key="pt_dn"): st.session_state.bus_p_teen = max(0, st.session_state.bus_p_teen - 1); st.rerun()
        with col3:
            st.markdown("**어린이**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_child}명</h3>", unsafe_allow_html=True)
            if st.button("➕ 추가", key="pc_up"): st.session_state.bus_p_child += 1; st.rerun()
            if st.button("➖ 감소", key="pc_dn"): st.session_state.bus_p_child = max(0, st.session_state.bus_p_child - 1); st.rerun()
        with col4:
            st.markdown("**어르신 (우대 할인)**")
            st.markdown(f"<h3 style='text-align:center;'>{st.session_state.bus_p_senior}명</h3>", unsafe_allow_html=True)
            if st.button("➕ 추가", key="ps_up"): st.session_state.bus_p_senior += 1; st.rerun()
            if st.button("➖ 감소", key="ps_dn"): st.session_state.bus_p_senior = max(0, st.session_state.bus_p_senior - 1); st.rerun()

        total_p = st.session_state.bus_p_adult + st.session_state.bus_p_teen + st.session_state.bus_p_child + st.session_state.bus_p_senior
        st.markdown(f"<div class='info-card' style='text-align:center;'>지정된 총 인원수: <span style='color:#4C51BF; font-size:26px;'>{total_p}명</span></div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 노선 다시 고르기", key="b_to_s3"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("좌석 고르러 가기 ➡", key="next_btn_bus_seat"):
                if total_p > 0: st.session_state.step = 11; speak("버스 내부 좌석판에서 원하는 자리를 터치해 보세요."); st.rerun()
                else: st.warning("최소 1명 이상 인원을 추가하셔야 합니다!")

    # --- [버스 우등 28석 대형 좌석표 선택] ---
    elif st.session_state.step == 11:
        total_need = st.session_state.bus_p_adult + st.session_state.bus_p_teen + st.session_state.bus_p_child + st.session_state.bus_p_senior
        st.markdown(f'<div class="guide-box">🚍 [3단계: 내 좌석 지정하기]<br>원하는 빈 자리를 선택하세요.<br>(선택 완료된 좌석수: {len(st.session_state.bus_selected_seats)} / {total_need}석)</div>', unsafe_allow_html=True)
        
        st.write("🚍 버스 운전석 방향 (앞쪽)")
        sold_seats = [3, 7, 12, 18, 22] # 선점 마감석 가상 구현
        
        for row in range(1, 10):
            cols = st.columns(4)
            
            s1 = (row - 1) * 3 + 1
            if s1 <= 28:
                if s1 in sold_seats: cols[0].button(f"❌ {s1:02d}", key=f"s_{s1}", disabled=True)
                elif s1 in st.session_state.bus_selected_seats:
                    if cols[0].button(f"⭐ {s1:02d}", key=f"s_{s1}"): st.session_state.bus_selected_seats.remove(s1); st.rerun()
                else:
                    if cols[0].button(f"💺 {s1:02d}", key=f"s_{s1}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s1); st.rerun()
                        else: st.warning("인원수만큼 좌석 배정이 이미 끝났습니다.")
                        
            s2 = (row - 1) * 3 + 2
            if s2 <= 28:
                if s2 in sold_seats: cols[1].button(f"❌ {s2:02d}", key=f"s_{s2}", disabled=True)
                elif s2 in st.session_state.bus_selected_seats:
                    if cols[1].button(f"⭐ {s2:02d}", key=f"s_{s2}"): st.session_state.bus_selected_seats.remove(s2); st.rerun()
                else:
                    if cols[1].button(f"💺 {s2:02d}", key=f"s_{s2}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s2); st.rerun()
                        else: st.warning("인원수만큼 좌석 배정이 이미 끝났습니다.")
            
            cols[2].write("") # 통로 분리선 공백
            
            s3 = (row - 1) * 3 + 3
            if s3 <= 28:
                if s3 in sold_seats: cols[3].button(f"❌ {s3:02d}", key=f"s_{s3}", disabled=True)
                elif s3 in st.session_state.bus_selected_seats:
                    if cols[3].button(f"⭐ {s3:02d}", key=f"s_{s3}"): st.session_state.bus_selected_seats.remove(s3); st.rerun()
                else:
                    if cols[3].button(f"💺 {s3:02d}", key=f"s_{s3}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s3); st.rerun()
                        else: st.warning("인원수만큼 좌석 배정이 이미 끝났습니다.")

        st.markdown(f"<div class='price-box'>💵 승차권 최종 결제 금액: {get_total_price():,}원</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 인원수 다시 변경", key="b_to_s10"): 
                st.session_state.bus_selected_seats = []
                st.session_state.step = 10; st.rerun()
        with c2:
            if st.button("예약 확인창으로 ➡", key="next_btn_bus_done"):
                if len(st.session_state.bus_selected_seats) == total_need: st.session_state.step = 4; speak("예약 승인창을 검토하세요."); st.rerun()
                else: st.error(f"인원수에 맞게 좌석을 {total_need}개 전부 고르셔야 합니다.")

    # --- [스마트폰 앱 공통 - 최종 신청 내역 확인 화면] ---
    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 스마트폰에 입력한 내용이 맞는지 최종 확인창입니다.</div>', unsafe_allow_html=True)
        
        if st.session_state.selected_biz == "버스":
            st.markdown(f"""
            <div class='info-card'>
                🚌 고속버스 스마트 발권 정보<br><br>
                • <b>노선 구간:</b> {st.session_state.bus_from} 출발 ➡ {st.session_state.bus_to} 도착<br>
                • <b>출발 시각:</b> {st.session_state.bus_time}<br>
                • <b>확정 좌석:</b> {", ".join([f"{x}번" for x in st.session_state.bus_selected_seats])}<br>
                • <b>상세 인원:</b> 성인 {st.session_state.bus_p_adult} / 청소년 {st.session_state.bus_p_teen} / 경로 {st.session_state.bus_p_senior}명
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.selected_biz == "쇼핑":
            for name, qty in st.session_state.cart.items():
                st.markdown(f'<div class="info-card"><span>● {name} — {qty}개 ({SHOP_DATA[name]*qty:,}원)</span></div>', unsafe_allow_html=True)
        elif st.session_state.selected_biz == "은행":
            # 💡 이전 화면에서 어르신이 수정한 필드값이 완벽하게 수식 매칭되어 실시간 출력됩니다!
            try: display_money = int("".join(filter(str.isdigit, str(st.session_state.input_bank_money))))
            except: display_money = 50000
            st.markdown(f"""
            <div class='info-card'>
                🏦 NH 스마트 뱅킹 이체 내역<br><br>
                • <b>보낼 은행:</b> {st.session_state.input_bank_name}<br>
                • <b>상대방 계좌:</b> {st.session_state.input_bank_account}<br>
                • <b>이체할 금액:</b> <span style='color:#E53E3E;'>{display_money:,}원</span>
            </div>
            """, unsafe_allow_html=True)

        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제/송금 총액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 처음부터 다시 하기", key="a_b4_back"): 
                b_save = st.session_state.selected_biz
                reset_state(); st.session_state.selected_biz = b_save
                st.session_state.step = 3; st.rerun()
        with c2:
            if st.session_state.selected_biz == "은행":
                if st.button("비밀번호 6자리 누르기 🔑", key="next_btn_pass"): st.session_state.step = 8; speak("통장 비밀번호 숫자 6자리를 차례대로 입력하세요."); st.rerun()
            else:
                if st.button("결제 진행하기 ➡", key="pay_btn_app4"): st.session_state.step = 5; speak("결제 방식을 고르세요."); st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">온라인 스마트 결제 종류를 선택하세요.</div>', unsafe_allow_html=True)
        if st.button("🏦 내 통장 계좌이체 연동", key="a_pay_bank"): st.session_state.pay_method = "계좌이체"; st.session_state.step = 9; st.rerun()
        if st.button("💳 앱카드 및 신용카드 번호 결제", key="a_pay_card"): st.session_state.pay_method = "카드"; st.session_state.step = 6; speak("가상 카드 정보를 입력하세요."); st.rerun()
        if st.button("⬅ 이전으로", key="a_b5_back"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        st.markdown('<div class="guide-box">💳 [카드 정보 안전 입력]<br>카드 번호와 비밀번호를 가상으로 안전하게 채워줍니다.</div>', unsafe_allow_html=True)
        st.text_input("카드번호 16자리 입력 예시", "9411 - 1234 - **** - ****")
        st.text_input("카드 비밀번호 앞 2자리", type="password")
        if st.button("안전하게 결제 승인 완료 🔒", key="complete_btn_app_card"): st.session_state.step = 7; speak("모든 스마트폰 모바일 미션에 완벽히 성공하셨습니다."); st.rerun()
        if st.button("⬅ 이전으로", key="a_b6_back"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 스마트폰 미션 최종 성공!")
        total = get_total_price()
        
        # 스마트폰 화면 및 마트 전 영역에서 "번호표 챙겨가라"는 어색한 문구 원천 박멸!
        st.markdown(f"""
        <div class="guide-box" style="background-color:#EBF8FF !important; border: 3px solid #63B3ED;">
            참 잘하셨습니다 어르신!<br>
            자녀분에게 돈이 안전하게 전송되었거나 스마트 승차권이 발행되었습니다.<br>
            종이 번호표나 지갑을 따로 안 꺼내셔도 앱 안에 다 저장되어 있습니다.<br><br>
            <b>🧾 최종 처리 총액: {total:,}원</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏠 처음 메인 홈 화면으로 가기", key="a_fin_btn_home"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 8:
        # 사용자가 수정한 금액이 비밀번호 창에도 연동되도록 완벽 수정
        try: current_money = int("".join(filter(str.isdigit, str(st.session_state.input_bank_money))))
        except: current_money = 50000
            
        st.markdown(f'<div class="guide-box">🔑 [보안 비밀번호 입력]<br>{st.session_state.input_bank_name}으로 {current_money:,}원 송금하기 직전입니다.<br>내 통장 비밀번호 숫자 6자리를 누르세요.</div>', unsafe_allow_html=True)
        stars = " ".join(["★" for _ in st.session_state.bank_pass]) + " " + " ".join(["☆" for _ in range(6 - len(st.session_state.bank_pass))])
        st.markdown(f"<h1 style='text-align:center; color:#4C51BF; letter-spacing: 5px;'>{stars}</h1>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i in range(1, 10):
            if cols[(i-1)%3].button(str(i), key=f"num_{i}"): st.session_state.bank_pass += str(i); st.rerun()
        if st.columns(3)[1].button("0", key="num_0"): st.session_state.bank_pass += "0"; st.rerun()
        
        if len(st.session_state.bank_pass) >= 6: st.session_state.pay_method = "은행"; st.session_state.step = 7; speak("이체가 완벽하게 마무리되었습니다."); st.rerun()
        if st.button("❌ 번호 잘못 눌렀음 (지우기)", key="num_clear"): st.session_state.bank_pass = ""; st.rerun()

    elif st.session_state.step == 9:
        st.markdown('<div class="guide-box">내 통장 계좌 정보가 맞는지 최종 체크하세요.</div>', unsafe_allow_html=True)
        st.selectbox("돈이 빠져나갈 내 통장 은행명", ["농협은행 (논산 지점)", "국민은행", "우체국"])
        st.text_input("내 계좌번호 입력", "110-345-******")
        if st.button("안전하게 계좌이체 승인 🔒", key="complete_btn_app_tr"): st.session_state.step = 7; speak("스마트 금융 처리가 끝났습니다."); st.rerun()
        if st.button("⬅ 이전으로", key="a_b9_back"): st.session_state.step = 5; st.rerun()


# --- ⚠️ 모든 연습 화면 하단 안심 가이드 상시 고정 배정 ---
st.markdown('<div class="footer-notice">⚠️ 안심하세요! 이 프로그램은 돈이 실제로 빠져나가지 않는 안전한 교육용 가상 앱입니다. 실수해도 괜찮으니 마음껏 연습하세요!</div>', unsafe_allow_html=True)

# --- 상호작용형 특수 컨텍스트 기반 TTS 보정 스크립트 ---
if st.session_state.step > 1:
    if st.session_state.mode == "APP" and st.session_state.step == 10: speak("탑승하실 인원을 어른, 어린이, 경로 항목별로 더해 주세요.")
    elif st.session_state.mode == "APP" and st.session_state.step == 11: speak("원하시는 버스 좌석 번호를 인원수만큼 직접 눌러서 선택하세요.")
