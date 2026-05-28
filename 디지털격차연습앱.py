import streamlit as st

# 1. 페이지 기본 설정 및 디자인 (v6 디자인 대폭 강화)
st.set_page_config(page_title="디지털 친구 - 시니어 맞춤형 교육 앱", layout="centered")

st.markdown("""
    <style>
    /* 배경색 및 기본 폰트 설정 */
    .main {
        background-color: #FAF9F6; /* 따뜻한 크림색 배경 */
    }
    
    html, body, [data-testid="stWidgetLabel"] p {
        font-family: 'Nanum Gothic', sans-serif;
        color: #2D3748 !important;
    }

    /* 진행 단계 표시바 스타일 */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
        padding: 10px;
        background: white;
        border-radius: 50px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .step-dot {
        width: 12%;
        height: 10px;
        background-color: #E2E8F0;
        border-radius: 10px;
    }
    .step-dot.active {
        background-color: #6366F1;
        box-shadow: 0 0 8px rgba(99, 102, 241, 0.5);
    }

    /* 가이드 박스 (말풍선 느낌) */
    .guide-box {
        font-size: 28px;
        font-weight: 800;
        color: #1A365D;
        text-align: center;
        background-color: #FFFFFF;
        padding: 35px;
        border-radius: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 2px solid #E2E8F0;
        line-height: 1.5;
    }

    /* 버튼 스타일 디자인 (고급형) */
    .stButton>button {
        width: 100%;
        height: 85px;
        font-size: 26px !important;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        background-color: #FFFFFF;
        color: #2D3748;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }
    
    .stButton>button:hover {
        background-color: #F7FAFC;
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }

    /* 메인 강조 버튼 (파란색) */
    div.stButton>button[key*="start"], div.stButton>button[key*="next"], div.stButton>button[key*="pay"], div.stButton>button[key*="complete"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: white !important;
        height: 95px;
        font-size: 28px !important;
    }

    /* 가격 표시 상자 */
    .price-box {
        background: #FFF5F5;
        color: #C53030;
        font-size: 30px;
        font-weight: 800;
        text-align: center;
        padding: 25px;
        border-radius: 25px;
        margin: 20px 0;
        border: 2px dashed #FEB2B2;
    }
    
    /* 좌석/정보 선택 카드 */
    .info-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        border-left: 8px solid #6366F1;
        margin-bottom: 10px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 전역 상태 관리
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

# --- [메인 홈] ---
if st.session_state.mode == "MAIN":
    st.markdown('<div class="guide-box">🏠 안녕하세요, 어르신!<br>배우고 싶으신 공부를 선택해 보세요.</div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/grandfather-using-digital-devices-concept-illustration_114360-7053.jpg?w=500", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏪 매장 기계\n(키오스크) 연습", key="main_kiosk"):
            st.session_state.mode = "KIOSK"; reset_state(); st.rerun()
    with col2:
        if st.button("📱 스마트폰 앱\n(쇼핑/은행) 연습", key="main_app"):
            st.session_state.mode = "APP"; reset_state(); st.rerun()

# ==========================================
# 🛑 [분기 1] 매장 키오스크 모드
# ==========================================
elif st.session_state.mode == "KIOSK":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">실제 매장에 있는 기계(키오스크)로<br>주문하는 방법을 차근차근 배워봅시다!</div>', unsafe_allow_html=True)
        if st.button("연습 시작하기 🏁", key="k_start_btn"): st.session_state.step = 2; st.rerun()
        if st.button("처음 화면으로 돌아가기 🏠", key="k_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습하실 장소를 골라주세요.</div>', unsafe_allow_html=True)
        for biz in KIOSK_DATA.keys():
            if st.button(biz, key=f"k_biz_{biz}"): st.session_state.selected_biz = biz; st.session_state.step = 3; st.rerun()
        if st.button("⬅ 뒤로가기", key="k_b2_1"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{biz}]<br>원하는 음식을 누르고 [다음]을 누르세요.</div>', unsafe_allow_html=True)
        for name, price in KIOSK_DATA[biz].items():
            col_txt, col_btn = st.columns([3, 1])
            with col_txt: st.markdown(f'<div class="info-card">🍴 **{name}** ({price:,}원)</div>', unsafe_allow_html=True)
            with col_btn:
                if st.button("담기", key=f"k_add_{name}"):
                    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
                    speak(f"{name}을 담았습니다."); st.rerun()
        total = get_total_price()
        st.markdown(f'<div class="price-box">결제할 금액: {total:,}원</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("이전", key="k_b3_2"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
        with c2:
            if st.button("다음 단계로", key="k_n3_4_btn"):
                if total > 0: st.session_state.step = 4; st.rerun()
                else: st.warning("메뉴를 담아주세요!")

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">선택하신 메뉴가 맞는지 확인하세요.</div>', unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            st.markdown(f'<div class="info-card">✅ **{name}** {qty}개 — {KIOSK_DATA[st.session_state.selected_biz][name]*qty:,}원</div>', unsafe_allow_html=True)
        total = get_total_price()
        st.markdown(f'<div class="price-box">총 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("이전", key="k_b4_3"): st.session_state.step = 3; st.rerun()
        with c2: 
            if st.button("결제하기 (돈 내기)", key="k_n4_5_btn"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">돈을 어떻게 내시겠습니까?</div>', unsafe_allow_html=True)
        if st.button("💵 현금 (지폐/동전) 넣기", key="k_pay_cash"):
            st.session_state.pay_method = "현금"; st.session_state.step = 7; speak("현금 결제 완료"); st.rerun()
        if st.button("💳 카드 (신용/체크) 꽂기", key="k_pay_card"):
            st.session_state.pay_method = "카드"; st.session_state.step = 6; st.rerun()
        if st.button("📱 스마트폰 페이 (NFC) 태그", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"; st.session_state.step = 6; st.rerun()
        if st.button("이전으로", key="k_b5_4"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">카드를 기계에 끝까지 꽂아주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
            if st.button("카드 넣기 완료 💳", key="k_card_complete"): st.session_state.step = 7; st.rerun()
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">폰 뒷면을 기계 마크에 대어 주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("태그 완료 📱", key="k_nfc_complete"): st.session_state.step = 7; st.rerun()
        if st.button("이전으로", key="k_b6_5"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 주문을 성공적으로 마쳤습니다!")
        total = get_total_price()
        st.markdown(f'<div class="guide-box" style="background-color:#F0FFF4; border: 2px solid #68D391;">참 잘하셨습니다!<br>총 {total:,}원이 결제되었습니다.</div>', unsafe_allow_html=True)
        if st.button("홈 화면으로 돌아가기 🏠", key="k_finish_btn"): st.session_state.mode = "MAIN"; st.rerun()

# ==========================================
# 🛑 [분기 2] 스마트폰 앱 모드
# ==========================================
elif st.session_state.mode == "APP":
    draw_step_bar(st.session_state.step)
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">스마트폰으로 물건을 사고,<br>차표를 예약하는 법을 마스터해 봅시다!</div>', unsafe_allow_html=True)
        if st.button("앱 연습 시작하기 🏁", key="a_start_btn"): st.session_state.step = 2; st.rerun()
        if st.button("처음 화면으로 돌아가기 🏠", key="a_home_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">어떤 기능을 연습해 볼까요?</div>', unsafe_allow_html=True)
        if st.button("🛍️ 온라인 쇼핑 (물건 장보기)", key="a_biz_shop"): st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; st.rerun()
        if st.button("🏦 송금하기 (돈 보내기)", key="a_biz_bank"): st.session_state.selected_biz = "은행"; st.session_state.step = 3; st.rerun()
        if st.button("📅 버스 예약 (차표 예매)", key="a_biz_bus"): st.session_state.selected_biz = "버스"; st.session_state.step = 3; st.rerun()
        if st.button("⬅ 뒤로가기", key="a_b2_1"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        if biz == "쇼핑":
            st.markdown('<div class="guide-box">장바구니에 물건을 골라 담으세요.</div>', unsafe_allow_html=True)
            for name, pr in SHOP_DATA.items():
                col_txt, col_btn = st.columns([3, 1])
                with col_txt: st.markdown(f'<div class="info-card">📦 **{name}** ({pr:,}원)</div>', unsafe_allow_html=True)
                with col_btn:
                    if st.button("담기", key=f"s_add_{name}"): st.session_state.cart[name] = st.session_state.cart.get(name,0)+1; st.rerun()
            total = get_total_price()
            st.markdown(f'<div class="price-box">장바구니 합계: {total:,}원</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("이전", key="s_p"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
            with c2:
                if st.button("결제 진행", key="s_n"):
                    if total > 0: st.session_state.step = 4; st.rerun()
                    else: st.warning("물건을 골라주세요.")

        elif biz == "은행":
            st.markdown('<div class="guide-box">보낼 분의 정보를 입력하세요.</div>', unsafe_allow_html=True)
            st.selectbox("은행 선택", ["농협", "국민", "신한", "우리"])
            st.text_input("계좌번호 입력", "302-1234-5678-90")
            st.text_input("보낼 금액 (원)", "50,000")
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("이전", key="b_p"): st.session_state.step = 2; st.rerun()
            with c2: 
                if st.button("송금 확인", key="b_n"): st.session_state.step = 4; st.rerun()

        elif biz == "버스":
            st.markdown('<div class="guide-box">여정을 순서대로 선택하세요.</div>', unsafe_allow_html=True)
            st.write("📍 **1. 출발/도착지**")
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("출발: 서울경부", key="loc_s"): st.session_state.bus_from = "서울"; st.rerun()
            with c2: 
                if st.button("도착: 부산종합", key="loc_b"): st.session_state.bus_to = "부산"; st.rerun()
            st.write(f"경로: **{st.session_state.bus_from} ➡ {st.session_state.bus_to}**")
            
            if st.session_state.bus_to:
                st.write("⏰ **2. 시간/유형**")
                c3, c4 = st.columns(2)
                with c3: 
                    if st.button("09:00 출발", key="t_09"): st.session_state.bus_time = "09:00"; st.rerun()
                with c4: 
                    if st.button("경로 (우대할인)", key="age_e"): st.session_state.bus_age = "경로"; st.session_state.bus_price = 16100; st.rerun()
            
            if st.session_state.bus_age:
                st.write("💺 **3. 좌석 선택**")
                if st.button("💺 06번 (예약 가능)", key="seat_06"): st.session_state.step = 4; speak("좌석 선택 완료"); st.rerun()
            if st.button("⬅ 다시 입력", key="bus_re"): reset_state(); st.session_state.selected_biz="버스"; st.session_state.step=3; st.rerun()

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">입력하신 내용이 맞습니까?</div>', unsafe_allow_html=True)
        total = get_total_price()
        st.markdown(f'<div class="price-box">최종 예정 금액: {total:,}원</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("이전", key="a_b4_p"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.session_state.selected_biz == "은행":
                if st.button("비밀번호 입력", key="a_b4_pass"): st.session_state.step = 8; st.rerun()
            else:
                if st.button("결제하기", key="a_b4_pay"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">결제 수단을 골라주세요.</div>', unsafe_allow_html=True)
        if st.button("🏦 계좌이체 (통장 송금)", key="a_pay_bank"): st.session_state.pay_method = "계좌이체"; st.session_state.step = 9; st.rerun()
        if st.button("💳 신용/체크카드 (번호 입력)", key="a_pay_card"): st.session_state.pay_method = "카드"; st.session_state.step = 6; st.rerun()
        if st.button("이전으로", key="a_b5_p"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        st.markdown('<div class="guide-box">카드 정보 16자리와<br>비밀번호 앞 2자리를 입력하세요.</div>', unsafe_allow_html=True)
        st.text_input("카드번호", "1234 - **** - **** - ****")
        st.text_input("비밀번호 앞2자리", type="password")
        if st.button("결제 승인 🔒", key="a_card_done"): st.session_state.step = 7; st.rerun()
        if st.button("이전", key="a_b6_p"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 미션을 성공적으로 마쳤습니다!")
        total = get_total_price()
        st.markdown(f'<div class="guide-box" style="background-color:#EBF8FF; border:2px solid #90CDF4;">대단하세요 어르신!<br>총 {total:,}원의 업무가 완료되었습니다.</div>', unsafe_allow_html=True)
        if st.button("홈 화면으로 🏠", key="a_fin_btn"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 8:
        st.markdown('<div class="guide-box">송금을 위해<br>비밀번호 6자리를 누르세요.</div>', unsafe_allow_html=True)
        stars = " ".join(["★" for _ in st.session_state.bank_pass]) + " " + " ".join(["☆" for _ in range(6 - len(st.session_state.bank_pass))])
        st.markdown(f"<h1 style='text-align:center; color:#4F46E5;'>{stars}</h1>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i in range(1, 10):
            if cols[(i-1)%3].button(str(i), key=f"num_{i}"): st.session_state.bank_pass += str(i); st.rerun()
        if st.columns(3)[1].button("0", key="num_0"): st.session_state.bank_pass += "0"; st.rerun()
        if len(st.session_state.bank_pass) >= 6: st.session_state.pay_method = "은행"; st.session_state.step = 7; st.rerun()
        if st.button("지우기", key="num_c"): st.session_state.bank_pass = ""; st.rerun()

    elif st.session_state.step == 9:
        st.markdown('<div class="guide-box">출금하실 은행과<br>계좌번호를 확인하세요.</div>', unsafe_allow_html=True)
        st.selectbox("내 은행", ["농협", "국민", "우체국"])
        st.text_input("내 계좌번호", "110-***-******")
        if st.button("이체 승인 🔒", key="a_tr_done"): st.session_state.step = 7; st.rerun()
        if st.button("이전", key="a_b9_p"): st.session_state.step = 5; st.rerun()

# --- 음성 안내 ---
if st.session_state.step > 1:
    if st.session_state.mode == "KIOSK" and st.session_state.step == 2: speak("연습하실 장소를 골라주세요.")
    elif st.session_state.step == 8: speak("비밀번호 숫자 6자리를 누르세요.")
