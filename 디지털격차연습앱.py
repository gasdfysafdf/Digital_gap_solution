import streamlit as st

# 1. 페이지 기본 설정 및 시니어 맞춤형 라이트 테마 강제 정의
st.set_page_config(page_title="디지털 친구 - 시니어 맞춤형 교육 앱 v7.0", layout="centered")

# 시스템 다크모드를 무시하고 무조건 밝고 선명하게 만드는 CSS
st.markdown("""
    <style>
    /* 전체 배경색을 따뜻하고 밝은 크림색으로 강제 고정 */
    .stApp {
        background-color: #F7F6F0 !important;
    }
    
    /* 기본 글자색을 진한 검은색 계열로 통일 */
    html, body, [data-testid="stWidgetLabel"] p, h1, h2, h3, p, span {
        font-family: 'Nanum Gothic', sans-serif !important;
        color: #1A202C !important;
    }

    /* 상단 진행 단계 표시바 */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
        padding: 8px 15px;
        background: #FFFFFF;
        border-radius: 30px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
    }
    .step-dot {
        width: 12%;
        height: 12px;
        background-color: #EDF2F7;
        border-radius: 10px;
    }
    .step-dot.active {
        background-color: #4C51BF;
        box-shadow: 0 0 8px rgba(76, 81, 191, 0.4);
    }

    /* 대형 알림 가이드 박스 */
    .guide-box {
        font-size: 26px;
        font-weight: 800;
        color: #1A202C !important;
        text-align: center;
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 2px solid #4C51BF;
        line-height: 1.5;
    }

    /* [중요] 흰색 카드 스타일 - 내부 글씨를 무조건 진한 검은색으로 */
    .info-card {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #CBD5E0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 12px;
        font-size: 24px !important;
        font-weight: bold;
        color: #1A202C !important; /* 글씨 안 보이는 버그 완벽 해결 */
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .info-card strong {
        color: #1A202C !important;
    }

    /* 일반 선택 버튼 스타일 (큼직하고 선명하게) */
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        border: 2px solid #CBD5E0 !important;
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    
    /* 버튼 글자색 유지를 위한 강제 설정 */
    .stButton>button div p {
        color: #2D3748 !important;
        font-weight: bold !important;
    }

    /* 다음/결제/시작 등 우측 핵심 진행 버튼 (선명한 파란색 고정) */
    div.stButton>button[key*="start"], div.stButton>button[key*="next"], div.stButton>button[key*="pay"], div.stButton>button[key*="complete"], div.stButton>button[key*="n3_4"] {
        background: #4C51BF !important;
        color: #FFFFFF !important;
        border: none !important;
        height: 85px;
        font-size: 26px !important;
    }
    div.stButton>button[key*="start"] div p, div.stButton>button[key*="next"] div p, div.stButton>button[key*="pay"] div p, div.stButton>button[key*="complete"] div p, div.stButton>button[key*="n3_4"] div p {
        color: #FFFFFF !important;
    }

    /* 가격 표시 강렬한 붉은 상자 */
    .price-box {
        background-color: #FFF5F5 !important;
        color: #E53E3E !important;
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px dashed #FEB2B2;
    }
    
    /* 안심 하단 바 */
    .footer-notice {
        text-align: center;
        color: #718096 !important;
        font-size: 18px;
        font-weight: bold;
        margin-top: 30px;
        padding: 15px;
        background-color: #EDF2F7;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 전역 상태 관리 변수 초기화
if 'mode' not in st.session_state: st.session_state.mode = "MAIN" 
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_biz' not in st.session_state: st.session_state.selected_biz = ""
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'pay_method' not in st.session_state: st.session_state.pay_method = ""
if 'bank_pass' not in st.session_state: st.session_state.bank_pass = ""
if 'bus_from' not in st.session_state: st.session_state.bus_from = ""
if 'bus_to' not in st.session_state: st.session_state.bus_to = ""
if 'bus_time' not in st.session_state: st.session_state.bus_time = ""
if 'bus_age' not in st.session_state: st.session_state.bus_age = ""
if 'bus_price' not in st.session_state: st.session_state.bus_price = 0

KIOSK_DATA = {
    "🍔 패스트푸드점": {"햄버거": 5000, "치즈버거": 6000, "감자튀김": 2000, "콜라": 1500, "치킨너겟": 3000},
    "☕ 커피 전문점": {"아메리카노": 3000, "카페라떼": 3500, "바닐라라떼": 4000, "단팥빵": 2500, "조각케이크": 5000},
    "🏥 병원 / 약국": {"일반 진료비": 4500, "처방전 발행": 0, "영양제 수납": 15000, "보호 마스크": 3000}
}

SHOP_DATA = {
    "🌾 국산 유기농 쌀 10kg": 35000,
    "🐟 완도 전복 세트": 45000,
    "🍠 가정용 꿀 고구마 5kg": 18000
}

def get_total_price():
    if st.session_state.mode == "APP":
        if st.session_state.selected_biz == "쇼핑":
            return sum(SHOP_DATA.get(name, 0) * qty for name, qty in st.session_state.cart.items())
        if st.session_state.selected_biz == "은행": return 50000
        if st.session_state.selected_biz == "버스": return st.session_state.bus_price
        return 0
    biz = st.session_state.selected_biz
    if not biz or biz not in KIOSK_DATA: return 0
    return sum(KIOSK_DATA[biz].get(name, 0) * qty for name, qty in st.session_state.cart.items())

def speak(text):
    js_code = f"<script>var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'ko-KR'; msg.rate = 0.85; window.speechSynthesis.speak(msg);</script>"
    st.components.v1.html(js_code, height=0)

def reset_state():
    st.session_state.step = 1
    st.session_state.cart = {}
    st.session_state.selected_biz = ""
    st.session_state.pay_method = ""
    st.session_state.bank_pass = ""
    st.session_state.bus_from = ""
    st.session_state.bus_to = ""
    st.session_state.bus_time = ""
    st.session_state.bus_age = ""
    st.session_state.bus_price = 0

def draw_step_bar(current_step):
    html = '<div class="step-indicator">'
    for i in range(1, 8):
        active_class = "active" if i <= current_step else ""
        html += f'<div class="step-dot {active_class}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# --- [메인 홈 화면] ---
if st.session_state.mode == "MAIN":
    st.markdown('<div class="guide-box">👵 어르신 디지털 세상 똑똑이 연습 앱 👴<br>공부하고 싶으신 곳을 선택해 주세요.</div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/grandfather-using-digital-devices-concept-illustration_114360-7053.jpg?w=500", use_container_width=True)
    
    if st.button("🏪 1. 매장 기계 (키오스크) 주문 연습하기", key="main_kiosk"):
        st.session_state.mode = "KIOSK"; reset_state(); st.rerun()
    if st.button("📱 2. 스마트폰 앱 (쇼핑/은행/예약) 연습하기", key="main_app"):
        st.session_state.mode = "APP"; reset_state(); st.rerun()


# ==========================================
# 🛑 [분기 1] 매장 키오스크 모드
# ==========================================
elif st.session_state.mode == "KIOSK":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">실제 가게에 있는 화면과 똑같이<br>연습해 보는 공간입니다. 안심하고 누르세요!</div>', unsafe_allow_html=True)
        if st.button("연습 시작하기 🏁", key="k_start_btn"): st.session_state.step = 2; st.rerun()
        if st.button("🏠 처음 메인 화면으로 돌아가기", key="k_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습하고 싶으신 장소를 골라보세요.</div>', unsafe_allow_html=True)
        for biz in KIOSK_DATA.keys():
            if st.button(biz, key=f"k_biz_{biz}"): st.session_state.selected_biz = biz; st.session_state.step = 3; st.rerun()
        if st.button("⬅ 뒤로가기", key="k_b2_1"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{biz}]<br>원하는 음식을 누르고 아래의 [다음]을 누르세요.</div>', unsafe_allow_html=True)
        
        for name, price in KIOSK_DATA[biz].items():
            col_txt, col_btn = st.columns([3, 1])
            with col_txt: 
                # 흰색 카드 내부에 검은색 글씨를 완벽하게 강제 적용
                st.markdown(f'<div class="info-card"><span>{name} ({price:,}원)</span></div>', unsafe_allow_html=True)
            with col_btn:
                if st.button("담기", key=f"k_add_{name}"):
                    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
                    speak(f"{name} 담기 완료"); st.rerun()
                    
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 현재 담은 총 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 이전으로", key="k_b3_2"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
        with c2:
            if st.button("다음 단계로 ➡", key="k_n3_4_btn"):
                if total > 0: st.session_state.step = 4; st.rerun()
                else: st.warning("메뉴를 하나 이상 골라주셔야 합니다!")

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 고른 메뉴 확인창<br>고르신 음식을 확인하고 맞으면 결제를 누르세요.</div>', unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            st.markdown(f'<div class="info-card"><span>● {name} — {qty}개 ({KIOSK_DATA[st.session_state.selected_biz][name]*qty:,}원)</span></div>', unsafe_allow_html=True)
        
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제할 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 이전으로", key="k_b4_3"): st.session_state.step = 3; st.rerun()
        with c2: 
            if st.button("돈 내러 가기 (결제) ➡", key="k_n4_5_btn"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">결제 방법을 손가락으로 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("💵 현금 결제 (지폐나 동전 투입)", key="k_pay_cash"):
            st.session_state.pay_method = "현금"; st.session_state.step = 7; speak("현금 주문이 끝났습니다."); st.rerun()
        if st.button("💳 카드 결제 (신용카드나 체크카드)", key="k_pay_card"):
            st.session_state.pay_method = "카드"; st.session_state.step = 6; st.rerun()
        if st.button("📱 스마트폰 삼성페이 / 간편결제 태그", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"; st.session_state.step = 6; st.rerun()
        if st.button("⬅ 이전으로", key="k_b5_4"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">카드를 그림처럼 투입구 끝까지 꽂아주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
            if st.button("카드를 꽂았습니다 💳", key="k_card_complete"): st.session_state.step = 7; st.rerun()
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">스마트폰 뒷면을 리더기 기계에 대어 주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("스마트폰을 대었습니다 📱", key="k_nfc_complete"): st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="k_b6_5"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 축하합니다! 주문에 성공하셨습니다.")
        total = get_total_price()
        st.markdown(f'<div class="guide-box" style="background-color:#E6FFFA !important; border: 3px solid #319795;">주문이 완료되었습니다!<br>영수증과 번호표를 챙겨 가세요.<br>🧾 결제액: {total:,}원</div>', unsafe_allow_html=True)
        if st.button("🏠 처음 화면으로 이동하기", key="k_finish_btn"): st.session_state.mode = "MAIN"; st.rerun()


# ==========================================
# 🛑 [분기 2] 스마트폰 앱 모드
# ==========================================
elif st.session_state.mode == "APP":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">스마트폰 앱을 켜서 장을 보거나<br>돈을 송금하는 방법을 배워봅시다!</div>', unsafe_allow_html=True)
        if st.button("스마트폰 앱 연습 시작하기 🏁", key="a_start_btn"): st.session_state.step = 2; st.rerun()
        if st.button("🏠 처음 화면으로 돌아가기", key="a_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습해 볼 스마트폰 기능을 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("🛍️ 1. 온라인 쇼핑몰 (농산물 사보기)", key="a_biz_shop"): st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; st.rerun()
        if st.button("🏦 2. 모바일 뱅킹 (자식에게 돈 보내기)", key="a_biz_bank"): st.session_state.selected_biz = "은행"; st.session_state.step = 3; st.rerun()
        if st.button("📅 3. 고속버스 예약 (버스 차표 예매하기)", key="a_biz_bus"): st.session_state.selected_biz = "버스"; st.session_state.step = 3; st.rerun()
        if st.button("⬅ 뒤로가기", key="a_b2_1"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        if biz == "쇼핑":
            st.markdown('<div class="guide-box">🛍️ [인터넷 쇼핑몰]<br>원하는 농산물을 골라 장바구니에 담으세요.</div>', unsafe_allow_html=True)
            for name, pr in SHOP_DATA.items():
                col_txt, col_btn = st.columns([3, 1])
                with col_txt: st.markdown(f'<div class="info-card"><span>{name} ({pr:,}원)</span></div>', unsafe_allow_html=True)
                with col_btn:
                    if st.button("담기", key=f"s_add_{name}"): st.session_state.cart[name] = st.session_state.cart.get(name,0)+1; st.rerun()
            total = get_total_price()
            st.markdown(f'<div class="price-box">🛒 현재 장바구니 합계: {total:,}원</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ 이전으로", key="s_p"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
            with c2:
                if st.button("주문하러 가기 ➡", key="s_n"):
                    if total > 0: st.session_state.step = 4; st.rerun()
                    else: st.warning("물건을 최소 1개 이상 담아주세요.")

        elif biz == "은행":
            st.markdown('<div class="guide-box">🏦 [모바일 송금]<br>돈을 보낼 계좌 정보를 가상으로 입력합니다.</div>', unsafe_allow_html=True)
            st.selectbox("1. 어디 은행으로 보낼까요?", ["농협은행", "국민은행", "신한은행", "우리은행"])
            st.text_input("2. 상대방 계좌번호를 확인하세요", "302-1234-5678-90")
            st.text_input("3. 얼마를 보낼까요?", "50,000원")
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ 이전으로", key="b_p"): st.session_state.step = 2; st.rerun()
            with c2: 
                if st.button("송금 확인하기 ➡", key="b_n"): st.session_state.step = 4; st.rerun()

        elif biz == "버스":
            st.markdown('<div class="guide-box">🚍 [고속버스 예매]<br>순서대로 노선을 꾹 눌러주세요.</div>', unsafe_allow_html=True)
            st.write("📍 **1단계: 터미널 선택**")
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("출발: 서울경부", key="loc_s"): st.session_state.bus_from = "서울"; st.rerun()
            with c2: 
                if st.button("도착: 부산종합", key="loc_b"): st.session_state.bus_to = "부산"; st.rerun()
            st.info(f"선택 여정: {st.session_state.bus_from} 출발 ➡ {st.session_state.bus_to} 도착")
            
            if st.session_state.bus_to:
                st.write("⏰ **2단계: 시간 및 할인 유형**")
                c3, c4 = st.columns(2)
                with c3: 
                    if st.button("오전 09:00 출발", key="t_09"): st.session_state.bus_time = "09:00"; st.rerun()
                with c4: 
                    if st.button("👴 어르신 (경로 우대 할인)", key="age_e"): st.session_state.bus_age = "경로우대"; st.session_state.bus_price = 16100; st.rerun()
            
            if st.session_state.bus_age:
                st.write("💺 **3단계: 버스 자리 고르기**")
                if st.button("💺 빈 좌석 06번 선택하기", key="seat_06"): st.session_state.step = 4; speak("좌석 선택 완료"); st.rerun()
            if st.button("🔄 처음부터 다시 입력", key="bus_re"): reset_state(); st.session_state.selected_biz="버스"; st.session_state.step=3; st.rerun()

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 신청한 내용이 전부 맞는지 확인하세요.</div>', unsafe_allow_html=True)
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제/송금 금액: {total:,}원</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 이전으로", key="a_b4_p"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.session_state.selected_biz == "은행":
                if st.button("비밀번호 입력하기 🔑", key="a_b4_pass"): st.session_state.step = 8; st.rerun()
            else:
                if st.button("결제 단계로 가기 ➡", key="a_b4_pay"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">온라인 결제 방법을 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("🏦 통장 계좌이체 결제", key="a_pay_bank"): st.session_state.pay_method = "계좌이체"; st.session_state.step = 9; st.rerun()
        if st.button("💳 신용/체크카드 번호 적기 결제", key="a_pay_card"): st.session_state.pay_method = "카드"; st.session_state.step = 6; st.rerun()
        if st.button("⬅ 이전으로", key="a_b5_p"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        st.markdown('<div class="guide-box">💳 [카드 번호 입력]<br>카드 번호와 비밀번호를 가상으로 채워줍니다.</div>', unsafe_allow_html=True)
        st.text_input("카드번호 16자리 예시", "9411 - **** - **** - ****")
        st.text_input("비밀번호 앞 2자리 입력", type="password")
        if st.button("안전하게 결제 확인 승인 🔒", key="a_card_done"): st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="a_b6_p"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 축하합니다! 스마트폰 미션을 완벽히 성공하셨습니다.")
        total = get_total_price()
        st.markdown(f'<div class="guide-box" style="background-color:#EBF8FF !important; border: 2px solid #63B3ED;">참 잘하셨습니다 어르신!<br>모든 스마트폰 미션이 성공적으로 처리되었습니다.<br>🧾 처리 총액: {total:,}원</div>', unsafe_allow_html=True)
        if st.button("🏠 처음 화면으로 이동하기", key="a_fin_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 8:
        st.markdown('<div class="guide-box">🔑 [비밀번호 입력]<br>송금을 완료하기 위해 비밀번호 숫자 6자리를 누르세요.</div>', unsafe_allow_html=True)
        stars = " ".join(["★" for _ in st.session_state.bank_pass]) + " " + " ".join(["☆" for _ in range(6 - len(st.session_state.bank_pass))])
        st.markdown(f"<h1 style='text-align:center; color:#4C51BF;'>{stars}</h1>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i in range(1, 10):
            if cols[(i-1)%3].button(str(i), key=f"num_{i}"): st.session_state.bank_pass += str(i); st.rerun()
        if st.columns(3)[1].button("0", key="num_0"): st.session_state.bank_pass += "0"; st.rerun()
        
        if len(st.session_state.bank_pass) >= 6: st.session_state.pay_method = "은행"; st.session_state.step = 7; st.rerun()
        if st.button("❌ 처음부터 다시 누르기", key="num_c"): st.session_state.bank_pass = ""; st.rerun()

    elif st.session_state.step == 9:
        st.markdown('<div class="guide-box">내 계좌정보가 맞는지 확인해 주세요.</div>', unsafe_allow_html=True)
        st.selectbox("내 통장 은행", ["농협은행", "국민은행", "우체국"])
        st.text_input("내 계좌번호 예시", "110-***-******")
        if st.button("안전하게 송금/결제 이체 승인 🔒", key="a_tr_done"): st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="a_b9_p"): st.session_state.step = 5; st.rerun()


# --- 모든 화면 하단 안심 가이드 고정 배치 ---
st.markdown('<div class="footer-notice">⚠️ 이 앱은 실제 돈이 나가지 않는 교육용 연습 앱입니다. 안심하고 마음껏 누르셔도 됩니다!</div>', unsafe_allow_html=True)

# --- 자동 음성 가이드 시스템 ---
if st.session_state.step > 1:
    if st.session_state.mode == "KIOSK" and st.session_state.step == 2: speak("연습하고 싶으신 장소를 마우스나 손가락으로 골라주세요.")
    elif st.session_state.step == 8: speak("앱 비밀번호 숫자 여섯 자리를 차례대로 누르세요.")
