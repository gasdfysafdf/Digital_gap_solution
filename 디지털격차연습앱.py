import streamlit as st

# 1. 페이지 기본 설정 및 시니어 맞춤형 라이트 테마 강제 정의
st.set_page_config(page_title="디지털 친구 - 시니어 맞춤형 교육 앱 v9.0", layout="centered")

# 시스템 다크모드를 무시하고 밝고 선명한 디자인 유지
st.markdown("""
    <style>
    .stApp { background-color: #F7F6F0 !important; }
    
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
    .step-dot { width: 12%; height: 12px; background-color: #EDF2F7; border-radius: 10px; }
    .step-dot.active { background-color: #4C51BF; box-shadow: 0 0 8px rgba(76, 81, 191, 0.4); }

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

    /* 흰색 정보 카드 */
    .info-card {
        background-color: #FFFFFF !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #CBD5E0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 12px;
        font-size: 20px !important;
        font-weight: bold;
        color: #1A202C !important;
    }

    /* 일반 선택 버튼 스타일 */
    .stButton>button {
        width: 100%;
        height: 70px;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: 2px solid #CBD5E0 !important;
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 8px;
    }
    .stButton>button div p { color: #2D3748 !important; font-weight: bold !important; }

    /* 좌석 전용 버튼 스타일 (선택됨 / 일반 / 매진) */
    .seat-selected { background-color: #4C51BF !important; color: white !important; }
    .seat-sold { background-color: #E53E3E !important; color: white !important; opacity: 0.6; }

    /* 다음/결제/시작 등 핵심 진행 버튼 (선명한 보라색) */
    div.stButton>button[key*="start_btn"], div.stButton>button[key*="next_btn"], div.stButton>button[key*="pay_btn"], div.stButton>button[key*="complete_btn"] {
        background: #4C51BF !important;
        color: #FFFFFF !important;
        border: none !important;
        height: 85px;
        font-size: 26px !important;
    }
    div.stButton>button[key*="start_btn"] div p, div.stButton>button[key*="next_btn"] div p, div.stButton>button[key*="pay_btn"] div p, div.stButton>button[key*="complete_btn"] div p {
        color: #FFFFFF !important;
    }

    /* 가격 표시 상자 */
    .price-box {
        background-color: #FFF5F5 !important;
        color: #E53E3E !important;
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        padding: 15px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px dashed #FEB2B2;
    }
    
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

# --- 버스 예약 전용 상태 변수 대폭 확장 ---
if 'bus_from' not in st.session_state: st.session_state.bus_from = ""
if 'bus_to' not in st.session_state: st.session_state.bus_to = ""
if 'bus_time' not in st.session_state: st.session_state.bus_time = ""
if 'bus_total_seats' not in st.session_state: st.session_state.bus_total_seats = 1
if 'bus_p_adult' not in st.session_state: st.session_state.bus_p_adult = 0
if 'bus_p_teen' not in st.session_state: st.session_state.bus_p_teen = 0
if 'bus_p_child' not in st.session_state: st.session_state.bus_p_child = 0
if 'bus_p_senior' not in st.session_state: st.session_state.bus_p_senior = 0
if 'bus_selected_seats' not in st.session_state: st.session_state.bus_selected_seats = []

# 데이터베이스 기본 정의
KIOSK_DATA = {
    "🍔 패스트푸드점": {"일반 햄버거": 5000, "치즈버거": 6000, "불고기버거": 5500, "감자튀김": 2000, "콜라": 1500, "치킨너겟": 3000},
    "☕ 커피 전문점": {"아메리카노": 3000, "카페라떼": 3500, "따뜻한 쌍화차": 4500, "생강차": 4500, "단팥빵": 2500},
    "🛒 대형 마트": {"국산 삼겹살 1kg": 28000, "싱싱한 바나나": 4000, "서울우유 1L": 2900, "신라면 5봉지": 4200},
    "🏥 병원 / 약국": {"일반 진료비 수납": 4500, "처방전 발행": 0, "빨간약 소독제": 2000, "마시는 감기약": 1000}
}

SHOP_DATA = {
    "🌾 국산 유기농 쌀 10kg": 35000, "🐟 완도 전복 세트": 45000, "🍠 가정용 꿀 고구마 5kg": 18000,
    "🍎 상주 꿀사과 1박스": 29000, "🍊 영동 곶감 세트": 32000, "🍯 6년근 홍삼정 스틱": 55000
}

# 고속버스 기본 가격표 (서울 출발 기준 성인 요금)
BUS_PRICE_TABLE = {
    "부산종합": 36000, "대구한진": 28000, "울산": 32000, "전주": 20000, "강릉": 23000
}

def get_total_price():
    if st.session_state.mode == "APP":
        if st.session_state.selected_biz == "쇼핑":
            return sum(SHOP_DATA.get(name, 0) * qty for name, qty in st.session_state.cart.items())
        if st.session_state.selected_biz == "은행": return 50000
        if st.session_state.selected_biz == "버스":
            base = BUS_PRICE_TABLE.get(st.session_state.bus_to, 25000)
            total = (st.session_state.bus_p_adult * base + 
                     st.session_state.bus_p_teen * int(base * 0.8) + 
                     st.session_state.bus_p_child * int(base * 0.5) + 
                     st.session_state.bus_p_senior * int(base * 0.8))
            return total
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
    st.session_state.bus_total_seats = 1
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


# --- [메인 홈 화면] ---
if st.session_state.mode == "MAIN":
    st.markdown('<div class="guide-box">👵 어르신 디지털 세상 똑똑이 연습 앱 👴<br>공부하고 싶으신 곳을 선택해 주세요.</div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/grandfather-using-digital-devices-concept-illustration_114360-7053.jpg?w=500", use_container_width=True)
    
    if st.button("🏪 1. 매장 기계 (키오스크) 주문 연습하기", key="btn_main_kiosk"):
        st.session_state.mode = "KIOSK"; reset_state(); st.rerun()
    if st.button("📱 2. 스마트폰 앱 (쇼핑/은행/예약) 연습하기", key="btn_main_app"):
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
        if st.button("⬅ 뒤로가기", key="k_b2_back"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{biz}]<br>원하는 음식을 누르고 아래의 [다음 단계로]를 누르세요.</div>', unsafe_allow_html=True)
        
        for name, price in KIOSK_DATA[biz].items():
            col_txt, col_btn = st.columns([3, 1])
            with col_txt: st.markdown(f'<div class="info-card"><span>{name} ({price:,}원)</span></div>', unsafe_allow_html=True)
            with col_btn:
                if st.button("담기", key=f"k_add_{name}"):
                    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
                    speak(f"{name} 담기 완료"); st.rerun()
                    
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 현재 담은 총 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: if st.button("⬅ 장소 다시 고르기", key="k_b3_back"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
        with c2:
            if st.button("다음 단계로 ➡", key="k_next_btn_3"):
                if total > 0: st.session_state.step = 4; st.rerun()
                else: st.warning("메뉴를 하나 이상 골라주셔야 합니다!")

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 고른 메뉴 확인창<br>고르신 음식을 확인하고 맞으면 결제를 누르세요.</div>', unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            st.markdown(f'<div class="info-card"><span>● {name} — {qty}개 ({KIOSK_DATA[st.session_state.selected_biz][name]*qty:,}원)</span></div>', unsafe_allow_html=True)
        
        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제할 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: if st.button("⬅ 메뉴 다시 담기", key="k_b4_back"): st.session_state.step = 3; st.rerun()
        with c2: if st.button("돈 내러 가기 (결제) ➡", key="k_pay_btn_4"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">결제 방법을 손가락으로 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("💵 현금 결제 (지폐나 동전 투입)", key="k_pay_cash"):
            st.session_state.pay_method = "현금"; st.session_state.step = 7; speak("현금 주문이 끝났습니다."); st.rerun()
        if st.button("💳 카드 결제 (신용카드나 체크카드)", key="k_pay_card"):
            st.session_state.pay_method = "카드"; st.session_state.step = 6; st.rerun()
        if st.button("📱 스마트폰 삼성페이 / 간편결제 태그", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"; st.session_state.step = 6; st.rerun()
        if st.button("⬅ 이전으로", key="k_b5_back"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">카드를 그림처럼 투입구 끝까지 꽂아주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
            if st.button("카드를 꽂았습니다 💳", key="k_complete_btn_card"): st.session_state.step = 7; st.rerun()
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">스마트폰 뒷면을 리더기 기계에 대어 주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("스마트폰을 대었습니다 📱", key="k_complete_btn_nfc"): st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="k_b6_back"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 축하합니다! 주문에 성공하셨습니다.")
        total = get_total_price()
        st.markdown(f'<div class="guide-box" style="background-color:#E6FFFA !important; border: 3px solid #319795;">주문이 완료되었습니다!<br>영수증 and 번호표를 챙겨 가세요.<br>🧾 결제액: {total:,}원</div>', unsafe_allow_html=True)
        if st.button("🏠 처음 화면으로 이동하기", key="k_finish_btn_home"): st.session_state.mode = "MAIN"; st.rerun()


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
        if st.button("🛍️ 1. 온라인 쇼핑몰 (지자체 특산물 장보기)", key="a_biz_shop"): st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; st.rerun()
        if st.button("🏦 2. 모바일 뱅킹 (용돈/보일러값 돈 보내기)", key="a_biz_bank"): st.session_state.selected_biz = "은행"; st.session_state.step = 3; st.rerun()
        if st.button("📅 3. 고속버스 예약 (다양한 선택지 연습!)", key="a_biz_bus"): st.session_state.selected_biz = "버스"; st.session_state.step = 3; st.rerun()
        if st.button("⬅ 뒤로가기", key="a_b2_back"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        
        # --- [스마트폰 앱 - 쇼핑 기능] ---
        if biz == "쇼핑":
            st.markdown('<div class="guide-box">🛍️ [인터넷 쇼핑몰]<br>원하는 산지직송 상품을 장바구니에 담으세요.</div>', unsafe_allow_html=True)
            for name, pr in SHOP_DATA.items():
                col_txt, col_btn = st.columns([3, 1])
                with col_txt: st.markdown(f'<div class="info-card"><span>{name} ({pr:,}원)</span></div>', unsafe_allow_html=True)
                with col_btn:
                    if st.button("담기", key=f"s_add_{name}"): st.session_state.cart[name] = st.session_state.cart.get(name,0)+1; st.rerun()
            total = get_total_price()
            st.markdown(f'<div class="price-box">🛒 현재 장바구니 합계: {total:,}원</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: if st.button("⬅ 메뉴판 나가기", key="s_p_back"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
            with c2:
                if st.button("주문하러 가기 ➡", key="next_btn_shop"):
                    if total > 0: st.session_state.step = 4; st.rerun()
                    else: st.warning("물건을 최소 1개 이상 담아주세요.")

        # --- [스마트폰 앱 - 은행 송금 기능] ---
        elif biz == "은행":
            st.markdown('<div class="guide-box">🏦 [모바일 송금]<br>돈을 보낼 계좌 정보를 가상으로 선택하고 채워줍니다.</div>', unsafe_allow_html=True)
            st.selectbox("1. 어디 은행으로 보낼까요?", ["농협은행", "국민은행", "신한은행", "우리은행", "우체국"])
            st.text_input("2. 상대방 계좌번호를 확인하세요", "302-1234-5678-90")
            st.text_input("3. 얼마를 보낼까요?", "50,000원")
            c1, c2 = st.columns(2)
            with c1: if st.button("⬅ 이전으로", key="b_p_back"): st.session_state.step = 2; st.rerun()
            with c2: if st.button("송금 확인하기 ➡", key="next_btn_bank"): st.session_state.step = 4; st.rerun()

        # --- [스마트폰 앱 - 고속버스 예약 기능 대폭 확장] ---
        elif biz == "버스":
            st.markdown('<div class="guide-box">🚍 [1단계: 터미널 및 시간 선택]<br>원하시는 여정과 시간을 넓은 선택지에서 골라보세요.</div>', unsafe_allow_html=True)
            
            # 출발지 목록 확대
            st.write("📍 **1. 출발 터미널을 고르세요**")
            from_list = ["서울경부", "동서울", "인천", "대전복합", "광주종합"]
            c_f = st.columns(len(from_list))
            for idx, f_name in enumerate(from_list):
                if c_f[idx].button(f_name, key=f"f_{f_name}"): st.session_state.bus_from = f_name; st.rerun()
            
            # 도착지 목록 확대
            st.write("📍 **2. 도착 터미널을 고르세요**")
            to_list = ["부산종합", "대구한진", "울산", "전주", "강릉"]
            c_t = st.columns(len(to_list))
            for idx, t_name in enumerate(to_list):
                if c_t[idx].button(t_name, key=f"t_{t_name}"): st.session_state.bus_to = t_name; st.rerun()

            # 여정 안내창
            st.info(f"👉 나의 선택: [ {st.session_state.bus_from if st.session_state.bus_from else '...'} ] 에서 출발  ➡  [ {st.session_state.bus_to if st.session_state.bus_to else '...'} ] 도착")

            if st.session_state.bus_from and st.session_state.bus_to:
                st.write("⏰ **3. 버스 출발 시간을 고르세요**")
                time_list = ["07:00 (오전)", "09:00 (오전)", "13:00 (오후)", "16:00 (오후)", "20:00 (야간)"]
                c_time = st.columns(3)
                for idx, t_val in enumerate(time_list):
                    if c_time[idx%3].button(t_val, key=f"time_{idx}"): st.session_state.bus_time = t_val; st.rerun()
                
                if st.session_state.bus_time:
                    st.success(f"정해진 여정: {st.session_state.bus_from} ➡ {st.session_state.bus_to} ({st.session_state.bus_time} 출발)")
                    if st.button("인원 및 좌석 선택하러 가기 ➡", key="next_btn_bus_s1"): st.session_state.step = 10; st.rerun() # 10번 전용 인원창으로 이동

            if st.button("🔄 처음부터 다시 고르기", key="bus_reset_all"): reset_state(); st.session_state.selected_biz="버스"; st.rerun()

    # --- [버스 전용 추가 단계: 인원수 및 연령별 상세 설정] ---
    elif st.session_state.step == 10:
        st.markdown('<div class="guide-box">🚍 [2단계: 탑승 인원수 설정]<br>총 몇 명이 타는지 연령별로 인원수를 더해 주세요.</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**어른 (성인)**")
            if st.button("➕ 어른 추가", key="pa_up"): st.session_state.bus_p_adult += 1; st.rerun()
            if st.button("➖ 어른 감소", key="pa_dn"): st.session_state.bus_p_adult = max(0, st.session_state.bus_p_adult - 1); st.rerun()
        with col2:
            st.markdown("**청소년 (학생)**")
            if st.button("➕ 청소년 추가", key="pt_up"): st.session_state.bus_p_teen += 1; st.rerun()
            if st.button("➖ 청소년 감소", key="pt_dn"): st.session_state.bus_p_teen = max(0, st.session_state.bus_p_teen - 1); st.rerun()
        with col3:
            st.markdown("**어린이 (아동)**")
            if st.button("➕ 아동 추가", key="pc_up"): st.session_state.bus_p_child += 1; st.rerun()
            if st.button("➖ 아동 감소", key="pc_dn"): st.session_state.bus_p_child = max(0, st.session_state.bus_p_child - 1); st.rerun()
        with col4:
            st.markdown("**어르신 (경로)**")
            if st.button("➕ 어르신 추가", key="ps_up"): st.session_state.bus_p_senior += 1; st.rerun()
            if st.button("➖ 어르신 감소", key="ps_dn"): st.session_state.bus_p_senior = max(0, st.session_state.bus_p_senior - 1); st.rerun()

        # 인원 요약
        total_p = st.session_state.bus_p_adult + st.session_state.bus_p_teen + st.session_state.bus_p_child + st.session_state.bus_p_senior
        st.markdown(f"""
        <div class='info-card' style='text-align:center;'>
            선택된 총 인원: <span style='color:#4C51BF; font-size:26px;'>{total_p}명</span><br>
            (어른 {st.session_state.bus_p_adult}명 / 청소년 {st.session_state.bus_p_teen}명 / 아동 {st.session_state.bus_p_child}명 / 어르신 {st.session_state.bus_p_senior}명)
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 노선 다시 고르기", key="b_to_s3"): st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("좌석 직접 고르러 가기 ➡", key="next_btn_bus_seat"):
                if total_p > 0: st.session_state.step = 11; st.rerun()
                else: st.warning("최소 1명 이상 인원을 추가하셔야 합니다!")

    # --- [버스 전용 추가 단계: 28석 대형 좌석표 선택] ---
    elif st.session_state.step == 11:
        total_need = st.session_state.bus_p_adult + st.session_state.bus_p_teen + st.session_state.bus_p_child + st.session_state.bus_p_senior
        st.markdown(f'<div class="guide-box">🚍 [3단계: 좌석 번호 직접 고르기]<br>빈 좌석을 누르세요. 총 {total_need}석을 선택하셔야 합니다.<br>(선택됨: {len(st.session_state.bus_selected_seats)} / {total_need}석)</div>', unsafe_allow_html=True)
        
        # 가상의 우등버스 28인승 좌석 배치도 만들기
        st.write("🚍 버스 앞쪽 (운전석)")
        sold_seats = [3, 7, 12, 18, 22] # 가상 매진 좌석
        
        for row in range(1, 10): # 9줄 배치
            cols = st.columns(4) # 왼쪽 2자리, 통로, 오른쪽 1자리 구조 시뮬레이션
            
            # 좌석 1 (창가)
            s1 = (row - 1) * 3 + 1
            if s1 <= 28:
                if s1 in sold_seats: cols[0].button(f"❌ {s1:02d}", key=f"s_{s1}", disabled=True)
                elif s1 in st.session_state.bus_selected_seats:
                    if cols[0].button(f"⭐ {s1:02d}", key=f"s_{s1}"): st.session_state.bus_selected_seats.remove(s1); st.rerun()
                else:
                    if cols[0].button(f"💺 {s1:02d}", key=f"s_{s1}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s1); st.rerun()
                        else: st.warning("이미 설정한 인원수만큼 좌석을 다 고르셨습니다.")
                        
            # 좌석 2 (복도석)
            s2 = (row - 1) * 3 + 2
            if s2 <= 28:
                if s2 in sold_seats: cols[1].button(f"❌ {s2:02d}", key=f"s_{s2}", disabled=True)
                elif s2 in st.session_state.bus_selected_seats:
                    if cols[1].button(f"⭐ {s2:02d}", key=f"s_{s2}"): st.session_state.bus_selected_seats.remove(s2); st.rerun()
                else:
                    if cols[1].button(f"💺 {s2:02d}", key=f"s_{s2}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s2); st.rerun()
                        else: st.warning("이미 설정한 인원수만큼 좌석을 다 고르셨습니다.")
            
            # 중간 통로 표현 공백
            cols[2].write("")
            
            # 좌석 3 (우측 1인 단독석)
            s3 = (row - 1) * 3 + 3
            if s3 <= 28:
                if s3 in sold_seats: cols[3].button(f"❌ {s3:02d}", key=f"s_{s3}", disabled=True)
                elif s3 in st.session_state.bus_selected_seats:
                    if cols[3].button(f"⭐ {s3:02d}", key=f"s_{s3}"): st.session_state.bus_selected_seats.remove(s3); st.rerun()
                else:
                    if cols[3].button(f"💺 {s3:02d}", key=f"s_{s3}"):
                        if len(st.session_state.bus_selected_seats) < total_need: st.session_state.bus_selected_seats.append(s3); st.rerun()
                        else: st.warning("이미 설정한 인원수만큼 좌석을 다 고르셨습니다.")

        st.markdown(f"<div class='price-box'>💵 자동 계산된 총 버스 요금: {get_total_price():,}원</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 인원수 다시 변경", key="b_to_s10"): st.session_state.bus_selected_seats=[]; st.session_state.step = 10; st.rerun()
        with c2:
            if st.button("예약 확인창으로 ➡", key="next_btn_bus_done"):
                if len(st.session_state.bus_selected_seats) == total_need: st.session_state.step = 4; st.rerun()
                else: st.error(f"인원수에 맞게 좌석을 {total_need}개 전부 선택해 주세요.")

    # --- [스마트폰 앱 공통 - 4단계: 최종 신청 내용 최종 확인] ---
    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 신청한 예약/주문 내용이 전부 맞는지 확인하세요.</div>', unsafe_allow_html=True)
        
        if st.session_state.selected_biz == "버스":
            st.markdown(f"""
            <div class='info-card'>
                🚌 고속버스 승차권 정보<br><br>
                • <b>구간:</b> {st.session_state.bus_from} 출발 ➡ {st.session_state.bus_to} 도착<br>
                • <b>시간:</b> {st.session_state.bus_time}<br>
                • <b>선택 좌석:</b> {", ".join([f"{x}번" for x in st.session_state.bus_selected_seats])}<br>
                • <b>인원:</b> 어른{st.session_state.bus_p_adult} / 청소년{st.session_state.bus_p_teen} / 아동{st.session_state.bus_p_child} / 경로{st.session_state.bus_p_senior}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.selected_biz == "쇼핑":
            for name, qty in st.session_state.cart.items():
                st.markdown(f'<div class="info-card"><span>● {name} — {qty}개 ({SHOP_DATA[name]*qty:,}원)</span></div>', unsafe_allow_html=True)
        elif st.session_state.selected_biz == "은행":
            st.markdown('<div class="info-card">🏦 모바일 송금 내용<br><br>• 받는 계좌: 농협은행 302-1234-5678-90<br>• 송금 금액: 50,000원</div>', unsafe_allow_html=True)

        total = get_total_price()
        st.markdown(f'<div class="price-box">💰 최종 결제/송금 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("⬅ 처음부터 다시 고르기", key="a_b4_back"): reset_state(); st.session_state.selected_biz=st.session_state.selected_biz; st.session_state.step = 3; st.rerun()
        with c2:
            if st.session_state.selected_biz == "은행":
                if st.button("비밀번호 입력하기 🔑", key="next_btn_pass"): st.session_state.step = 8; st.rerun()
            else:
                if st.button("결제 단계로 가기 ➡", key="pay_btn_app4"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">온라인 결제 방법을 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("🏦 통장 계좌이체 결제", key="a_pay_bank"): st.session_state.pay_method = "계좌이체"; st.session_state.step = 9; st.rerun()
        if st.button("💳 신용/체크카드 번호 적기 결제", key="a_pay_card"): st.session_state.pay_method = "카드"; st.session_state.step = 6; st.rerun()
        if st.button("⬅ 이전으로", key="a_b5_back"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        st.markdown('<div class="guide-box">💳 [카드 번호 입력]<br>카드 번호와 비밀번호를 가상으로 채워줍니다.</div>', unsafe_allow_html=True)
        st.text_input("카드번호 16자리 예시", "9411 - **** - **** - ****")
        st.text_input("비밀번호 앞 2자리 입력", type="password")
        if st.button("안전하게 결제 확인 승인 🔒", key="complete_btn_app_card"): st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="a_b6_back"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 미션 성공! 완벽하게 마쳤습니다.")
        total = get_total_price()
        st.markdown(f'<div class="guide-box" style="background-color:#EBF8FF !important; border: 2px solid #63B3ED;">참 잘하셨습니다 어르신!<br>모든 스마트폰 미션이 성공적으로 처리되었습니다.<br>🧾 처리 총액: {total:,}원</div>', unsafe_allow_html=True)
        if st.button("🏠 처음 화면으로 이동하기", key="a_fin_btn_home"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 8:
        st.markdown('<div class="guide-box">🔑 [비밀번호 입력]<br>송금을 완료하기 위해 비밀번호 숫자 6자리를 누르세요.</div>', unsafe_allow_html=True)
        stars = " ".join(["★" for _ in st.session_state.bank_pass]) + " " + " ".join(["☆" for _ in range(6 - len(st.session_state.bank_pass))])
        st.markdown(f"<h1 style='text-align:center; color:#4C51BF;'>{stars}</h1>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i in range(1, 10):
            if cols[(i-1)%3].button(str(i), key=f"num_{i}"): st.session_state.bank_pass += str(i); st.rerun()
        if st.columns(3)[1].button("0", key="num_0"): st.session_state.bank_pass += "0"; st.rerun()
        
        if len(st.session_state.bank_pass) >= 6: st.session_state.pay_method = "은행"; st.session_state.step = 7; st.rerun()
        if st.button("❌ 처음부터 다시 누르기", key="num_clear"): st.session_state.bank_pass = ""; st.rerun()

    elif st.session_state.step == 9:
        st.markdown('<div class="guide-box">내 계좌정보가 맞는지 확인해 주세요.</div>', unsafe_allow_html=True)
        st.selectbox("내 통장 은행", ["농협은행", "국민은행", "우체국"])
        st.text_input("내 계좌번호 예시", "110-***-******")
        if st.button("안전하게 송금/결제 이체 승인 🔒", key="complete_btn_app_tr"): st.session_state.step = 7; st.rerun()
        if st.button("⬅ 이전으로", key="a_b9_back"): st.session_state.step = 5; st.rerun()


# --- 모든 화면 하단 안심 가이드 고정 배치 ---
st.markdown('<div class="footer-notice">⚠️ 이 앱은 실제 돈이 나가지 않는 교육용 연습 앱입니다. 안심하고 마음껏 누르셔도 됩니다!</div>', unsafe_allow_html=True)

# --- 자동 음성 가이드 시스템 ---
if st.session_state.step > 1:
    if st.session_state.mode == "APP" and st.session_state.step == 10: speak("탑승하실 인원을 어른, 청소년, 아동, 어르신 항목별로 더해 주세요.")
    elif st.session_state.mode == "APP" and st.session_state.step == 11: speak("원하시는 버스 좌석 번호를 인원수만큼 직접 눌러서 선택하세요.")
