import streamlit as st

# 1. 페이지 기본 설정 및 스타일 정의
st.set_page_config(page_title="디지털 친구 - 어르신 종합 디지털 교육 앱 v4", layout="centered")

st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
    }
    
    .stButton>button {
        width: 100%;
        height: 75px;
        font-size: 24px !important;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #CBD5E1;
        background-color: #F8FAFC;
        color: #1E293B;
        margin-bottom: 10px;
    }
    
    /* 강조/시작/다음 버튼 전용 스타일 */
    div.stButton>button[key*="start"], div.stButton>button[key*="next"], div.stButton>button[key*="pay"], div.stButton>button[key*="complete"] {
        background-color: #6366F1 !important;
        color: white !important;
        border: none !important;
        height: 85px;
        font-size: 26px !important;
    }
    
    /* 기능별 세부 선택 작은 버튼 스타일 */
    div.stButton>button[key*="seat_"], div.stButton>button[key*="loc_"], div.stButton>button[key*="time_"] {
        height: 60px !important;
        font-size: 20px !important;
    }
    
    .guide-box {
        font-size: 26px;
        font-weight: bold;
        color: #1E293B;
        text-align: center;
        background-color: #F1F5F9;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        border-bottom: 4px solid #CBD5E1;
        line-height: 1.5;
    }
    
    .price-box {
        background-color: #FEE2E2;
        color: #EF4444;
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 전역 상태 관리 변수 초기화
if 'mode' not in st.session_state: st.session_state.mode = "MAIN" 
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_biz' not in st.session_state: st.session_state.selected_biz = ""
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'pay_method' not in st.session_state: st.session_state.pay_method = ""

# 고속버스 전용 상태 변수
if 'bus_from' not in st.session_state: st.session_state.bus_from = ""
if 'bus_to' not in st.session_state: st.session_state.bus_to = ""
if 'bus_time' not in st.session_state: st.session_state.bus_time = ""

# 데이터 세팅
KIOSK_DATA = {
    "패스트푸드": {"햄버거": 5000, "치즈버거": 6000, "감자튀김": 2000, "콜라": 1500, "치킨너겟": 3000},
    "카페": {"아메리카노": 3000, "카페라떼": 3500, "바닐라라떼": 4000, "단팥빵": 2500, "조각케이크": 5000},
    "병원 / 약국": {"일반 진료비": 4500, "처방전 발행": 0, "영양제 수납": 15000, "보호 마스크": 3000}
}

SHOP_DATA = {
    "국산 유기농 쌀 10kg": 35000,
    "완도 카네이션 전복 세트": 45000,
    "가정용 꿀 고구마 5kg": 18000
}

def get_total_price():
    if st.session_state.mode == "APP":
        if st.session_state.selected_biz == "쇼핑":
            return sum(SHOP_DATA.get(name, 0) * qty for name, qty in st.session_state.cart.items())
        if st.session_state.selected_biz == "은행(송금)": return 50000
        if st.session_state.selected_biz == "고속버스 예매": return 23000
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
    st.session_state.bus_from = ""
    st.session_state.bus_to = ""
    st.session_state.bus_time = ""


# --- [대분류 메인 화면] ---
if st.session_state.mode == "MAIN":
    st.markdown('<div class="guide-box">👵 어르신 디지털 세상 똑똑하게 배우기 👴<br>공부하고 싶은 분야를 선택해 주세요.</div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/happy-grandparents-concept-illustration_114360-6644.jpg?w=500", use_container_width=True)
    
    if st.button("🏪 1. 매장 키오스크 연습하기 (식당/카페/병원)", key="main_kiosk"):
        st.session_state.mode = "KIOSK"
        reset_state()
        st.rerun()
        
    if st.button("📱 2. 스마트폰 앱 연습하기 (쇼핑/은행/예약)", key="main_app"):
        st.session_state.mode = "APP"
        reset_state()
        st.rerun()


# ==========================================
# 🛑 [분기 1] 매장 키오스크 연습 모드 (결제 NFC 유지)
# ==========================================
elif st.session_state.mode == "KIOSK":
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">실제 매장처럼 연습하고 실수해도 결제되지 않는<br>안전한 키오스크 연습 공간입니다!</div>', unsafe_allow_html=True)
        if st.button("키오스크 연습 시작하기 🏁", key="k_start"):
            st.session_state.step = 2
            st.rerun()
        if st.button("🏠 메인 화면으로 돌아가기", key="k_home"):
            st.session_state.mode = "MAIN"
            st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습하고 싶으신 장소를 눌러주세요.</div>', unsafe_allow_html=True)
        for biz in KIOSK_DATA.keys():
            if st.button(biz, key=f"k_biz_{biz}"):
                st.session_state.selected_biz = biz
                st.session_state.step = 3
                st.rerun()
        if st.button("⬅️ 뒤로가기", key="k_b2_1"): st.session_state.step = 1; st.rerun()

    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{biz}] 드실 메뉴판입니다.<br>원하는 음식을 누르고 [다음]을 누르세요.</div>', unsafe_allow_html=True)
        
        for name, price in KIOSK_DATA[biz].items():
            col_txt, col_btn = st.columns([3, 1])
            with col_txt: st.markdown(f"**{name}** ({price:,}원)")
            with col_btn:
                if st.button("담기", key=f"k_add_{name}"):
                    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
                    speak(f"{name} 추가")
                    st.rerun()
                    
        total = get_total_price()
        st.markdown(f'<div class="price-box">현재 주문 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        col_p, col_n = st.columns(2)
        with col_p: 
            if st.button("이전", key="k_b3_2"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
        with col_n:
            if st.button("다음", key="k_n3_4"):
                if total > 0: st.session_state.step = 4; st.rerun()
                else: st.warning("메뉴를 하나 이상 골라주세요!")

    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 고른 메뉴가 맞는지 확인해 보세요.</div>', unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            st.markdown(f"■ **{name}** : {qty}개 — {KIOSK_DATA[st.session_state.selected_biz][name]*qty:,}원")
        
        total = get_total_price()
        st.markdown(f'<div class="price-box">최종 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        col_p, col_n = st.columns(2)
        with col_p: 
            if st.button("이전", key="k_b4_3"): st.session_state.step = 3; st.rerun()
        with col_n: 
            if st.button("결제하기", key="k_n4_5"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">어떻게 결제하시겠습니까? (오프라인 매장 전용)</div>', unsafe_allow_html=True)
        
        if st.button("💵 현금 결제 (지폐 투입)", key="k_pay_cash"):
            st.session_state.pay_method = "현금"
            st.session_state.step = 7 
            speak("현금 결제가 완료되었습니다.")
            st.rerun()
            
        if st.button("💳 신용카드 결제 (카드 삽입)", key="k_pay_card"):
            st.session_state.pay_method = "카드"
            st.session_state.step = 6
            st.rerun()
            
        if st.button("📱 스마트폰 NFC 태그 결제 (삼성페이 등)", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"
            st.session_state.step = 6
            st.rerun()
            
        if st.button("이전으로", key="k_b5_4"): st.session_state.step = 4; st.rerun()

    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">IC칩이 위로 향하게 카드를 끝까지 넣어주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-hand-holding-smartphone-with-nfc-payment-isolated-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
            if st.button("카드 넣기 완료 💳", key="k_card_complete"): st.session_state.step = 7; st.rerun()
            
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">스마트폰 뒷면을 기계 하단의 리더기에 대어 주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("스마트폰 태그 완료 📱", key="k_nfc_complete"): st.session_state.step = 7; st.rerun()
            
        if st.button("이전으로", key="k_b6_5"): st.session_state.step = 5; st.rerun()

    elif st.session_state.step == 7:
        st.success("🎉 키오스크 주문 성공!")
        total = get_total_price()
        st.markdown(f'<div class="guide-box" style="background-color:#DCFCE7;">주문이 정상적으로 끝났습니다!<br>총 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
        if st.button("메인 화면으로 가기 🏠", key="k_finish"): st.session_state.mode = "MAIN"; st.rerun()


# ==========================================
# 🛑 [분기 2] 스마트폰 필수 앱 연습 모드 (대폭 수정)
# ==========================================
elif st.session_state.mode == "APP":
    
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">스마트폰으로 물건을 사고, 돈을 보내고, 차표를 예약하는<br>과정을 하나씩 마스터해 봅시다!</div>', unsafe_allow_html=True)
        if st.button("스마트폰 앱 연습 시작하기 🏁", key="a_start"): st.session_state.step = 2; st.rerun()
        if st.button("🏠 메인 화면으로 돌아가기", key="a_home"): st.session_state.mode = "MAIN"; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">원하시는 스마트폰 기능을 터치하세요.</div>', unsafe_allow_html=True)
        if st.button("🛍️ 1. 장보기 쇼핑몰 (여러 상품 골라 담기)", key="a_biz_shop"):
            st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; st.rerun()
        if st.button("🏦 2. 모바일 뱅킹 (계좌이체 송금)", key="a_biz_bank"):
            st.session_state.selected_biz = "은행(송금)"; st.session_state.step = 3; st.rerun()
        if st.button("📅 3. 고속버스 예매 (노선 및 시간 지정)", key="a_biz_bus"):
            st.session_state.selected_biz = "고속버스 예매"; st.session_state.step = 3; st.rerun()
        st.markdown("---")
        if st.button("⬅ 뒤로가기", key="a_b2_1"): st.session_state.step = 1; st.rerun()

    # [3단계: 각 앱별 고유 입력 프로세스]
    elif st.session_state.step == 3:
        app_type = st.session_state.selected_biz
        
        # --- 인터넷 쇼핑몰 (상품 다변화 + 키오스크식 담기 구조) ---
        if app_type == "쇼핑":
            st.markdown('<div class="guide-box">🛒 [디지털 마켓]<br>원하는 농산물을 골라 장바구니에 담아보세요!</div>', unsafe_allow_html=True)
            for prod_name, price in SHOP_DATA.items():
                col_txt, col_btn = st.columns([3, 1])
                with col_txt: st.markdown(f"**{prod_name}** — {price:,}원")
                with col_btn:
                    if st.button("담기", key=f"shop_add_{prod_name}"):
                        st.session_state.cart[prod_name] = st.session_state.cart.get(prod_name, 0) + 1
                        speak(f"{prod_name} 장바구니 추가")
                        st.rerun()
            
            total = get_total_price()
            st.markdown(f'<div class="price-box">장바구니 총 금액: {total:,}원</div>', unsafe_allow_html=True)
            
            col_p, col_n = st.columns(2)
            with col_p: 
                if st.button("이전으로", key="shop_prev"): st.session_state.step = 2; st.session_state.cart={}; st.rerun()
            with col_n:
                if st.button("주문 결제하기", key="shop_next"):
                    if total > 0: st.session_state.step = 4; st.rerun()
                    else: st.warning("상품을 담아주세요!")
            
        # --- 모바일 뱅킹 송금 ---
        elif app_type == "은행(송금)":
            st.markdown('<div class="guide-box">🏦 [스마트 뱅킹]<br>자녀에게 보낼 은행과 정보를 확인하세요.</div>', unsafe_allow_html=True)
            st.selectbox("받는 사람 은행 선택", ["농협은행", "국민은행", "신한은행", "우리은행"])
            st.text_input("받는 사람 계좌번호", "302-1234-5678-90")
            st.text_index = st.text_input("보낼 금액 (원)", "50,000")
            
            col_p, col_n = st.columns(2)
            with col_p: 
                if st.button("이전으로", key="bank_prev"): st.session_state.step = 2; st.rerun()
            with col_n:
                if st.button("송금 정보 확인", key="bank_next"): st.session_state.step = 4; st.rerun()
                
        # --- 고속버스 예매 (출발지 -> 도착지 -> 시간 -> 좌석 순서대로 전면 개편) ---
        elif app_type == "고속버스 예매":
            st.markdown('<div class="guide-box">🚍 [고속버스 예매 티켓]</div>', unsafe_allow_html=True)
            
            # 1. 출발지 선택
            st.write("📍 **1. 출발지를 고르세요**")
            c1, c2, c3 = st.columns(3)
            with c1: 
                if st.button("🏠 서울경부", key="loc_seoul"): st.session_state.bus_from = "서울경부"; st.rerun()
            with c2: 
                if st.button("🏢 인천터미널", key="loc_incheon"): st.session_state.bus_from = "인천"; st.rerun()
            with c3: 
                if st.button("🏙️ 대전복합", key="loc_daejeon"): st.session_state.bus_from = "대전"; st.rerun()
            st.info(f"선택된 출발지: **{st.session_state.bus_from if st.session_state.bus_from else '없음'}**")
            
            # 2. 도착지 선택
            if st.session_state.bus_from:
                st.write("🏁 **2. 도착지를 고르세요**")
                c4, c5, c6 = st.columns(3)
                with c4: 
                    if st.button("🌊 부산종합", key="loc_busan"): st.session_state.bus_to = "부산"; st.rerun()
                with c5: 
                    if st.button("🍎 동대구", key="loc_daegu"): st.session_state.bus_to = "대구"; st.rerun()
                with c6: 
                    if st.button("🍉 광주유스퀘어", key="loc_gwangju"): st.session_state.bus_to = "광주"; st.rerun()
                st.info(f"선택된 도착지: **{st.session_state.bus_to if st.session_state.bus_to else '없음'}**")
                
            # 3. 시간 선택
            if st.session_state.bus_to:
                st.write("⏰ **3. 출발 시간을 고르세요**")
                c7, c8, c9 = st.columns(3)
                with c7: 
                    if st.button("☀️ 아침 09:00", key="time_09"): st.session_state.bus_time = "09:00"; st.rerun()
                with c8: 
                    if st.button("🌤️ 낮 13:00", key="time_13"): st.session_state.bus_time = "13:00"; st.rerun()
                with c9: 
                    if st.button("🌙 저녁 18:00", key="time_18"): st.session_state.bus_time = "18:00"; st.rerun()
                st.info(f"선택된 출발시간: **{st.session_state.bus_time if st.session_state.bus_time else '없음'}**")

            # 모든 정보 입력 완료 후 좌석 선택 활성화
            if st.session_state.bus_from and st.session_state.bus_to and st.session_state.bus_time:
                st.write("💺 **4. 비어있는 좌석을 선택하세요**")
                cx, cy = st.columns(2)
                with cx: st.button("💺 05번 (예약 완료)", disabled=True)
                with cy: 
                    if st.button("💺 06번 (예약 가능)", key="seat_06"):
                        speak("06번 좌석 선택 완료")
                        st.session_state.step = 4
                        st.rerun()
                        
            st.markdown("---")
            if st.button("⬅ 처음부터 다시 입력", key="bus_reset"): reset_state(); st.session_state.selected_biz="고속버스 예매"; st.session_state.step=3; st.rerun()

    # [4단계: 스마트폰 앱용 최종 내역 검토창]
    elif st.session_state.step == 4:
        app_type = st.session_state.selected_biz
        st.markdown('<div class="guide-box">화면에 적힌 입력 내용이 전부 맞는지 확인하세요.</div>', unsafe_allow_html=True)
        
        total = get_total_price()
        if app_type == "쇼핑":
            for name, qty in st.session_state.cart.items():
                st.write(f"· {name} : {qty}개")
            st.markdown(f"### 총 결제 금액 : **{total:,}원**")
        elif app_type == "은행(송금)":
            st.write(f"· 자녀에게 보내는 계좌이체 금액 : **{total:,}원**")
        elif app_type == "고속버스 예매":
            st.write(f"· 노선 : {st.session_state.bus_from} ➡️ {st.session_state.bus_to}")
            st.write(f"· 시간 및 좌석 : {st.session_state.bus_time} 출발 / 06번 좌석")
            st.markdown(f"### 버스 승차권 금액 : **{total:,}원**")
            
        col_p, col_n = st.columns(2)
        with col_p: 
            if st.button("이전으로", key="app_b4_3"): st.session_state.step = 3; st.rerun()
        with col_n:
            if st.button("다음 단계 (결제하기)", key="app_n4_5"): st.session_state.step = 5; st.rerun()

    # [5단계: 온라인 전용 결제 방식 선택 (NFC 스마트페이/무통장 전면 제외)]
    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">스마트폰 안에서 안전하게 결제할 수단을 골라주세요.</div>', unsafe_allow_html=True)
        
        if st.button("🏦 실시간 계좌이체 (통장에서 바로 송금)", key="a_pay_bank_transfer"):
            st.session_state.pay_method = "계좌이체"
            st.session_state.step = 7 # 계좌이체 승인은 별도 단말 태그 없이 완료창 이동
            speak("계좌이체 승인 완료")
            st.rerun()
            
        if st.button("💳 신용/체크카드 결제 (카드번호 입력)", key="a_pay_card_online"):
            st.session_state.pay_method = "온라인카드"
            st.session_state.step = 6
            st.rerun()
            
        if st.button("이전으로", key="app_b5_4"): st.session_state.step = 4; st.rerun()

    # [6단계: 온라인 전용 결제 세부 액션]
    elif st.session_state.step == 6:
        st.markdown('<div class="guide-box">💳 [카드 정보 입력]<br>스마트폰 화면에 카드 번호와 비밀번호를 적는 칸입니다.</div>', unsafe_allow_html=True)
        st.text_input("1. 카드 번호 16자리 예시 입력", "4571 - 1234 - **** - ****")
        st.text_input("2. 비밀번호 앞 2자리 입력", type="password", placeholder="**")
        
        col_p, col_n = st.columns(2)
        with col_p: 
            if st.button("이전으로", key="app_b6_5"): st.session_state.step = 5; st.rerun()
        with col_n:
            if st.button("온라인 결제 승인 완료 🔒", key="app_online_complete"): st.session_state.step = 7; st.rerun()

    # [7단계: 모바일 앱 시나리오 최종 완료]
    elif st.session_state.step == 7:
        st.success("🎉 스마트폰 미션 최종 성공!")
        total = get_total_price()
        app_type = st.session_state.selected_biz
        
        if st.session_state.pay_method == "계좌이체":
            st.markdown(f'<div class="guide-box" style="background-color:#E0F2FE;">[{app_type}] 등록된 본인 계좌에서 이체가 안전하게 완료되었습니다.<br>이체 총액: {total:,}원</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="guide-box" style="background-color:#DCFCE7;">[{app_type}] 온라인 카드 승인이 완료되었습니다!<br>이용 총액: {total:,}원</div>', unsafe_allow_html=True)
            
        st.write("인터넷 쇼핑과 버스 예약도 이제 폰으로 척척 하실 수 있습니다!")
        if st.button("대메뉴 초기화면으로 이동 🏠", key="app_finish"): st.session_state.mode = "MAIN"; st.rerun()


# --- 전 단계 음성 안내 연동 로직 ---
if st.session_state.mode == "KIOSK":
    if st.session_state.step == 2: speak("연습하고 싶으신 장소를 눌러주세요.")
    elif st.session_state.step == 3: speak("음식을 누르고 아래 다음 버튼을 누르세요.")
    elif st.session_state.step == 5: speak("현금, 카드, 삼성페이 중 결제 방식을 고르세요.")
elif st.session_state.mode == "APP":
    if st.session_state.step == 2: speak("연습하고 싶으신 스마트폰 기능을 터치하세요.")
    elif st.session_state.step == 3:
        if st.session_state.selected_biz == "고속버스 예매": speak("출발지와 도착지, 시간을 차례대로 선택해 주세요.")
        else: speak("실제 스마트폰 화면처럼 정보를 입력해 보세요.")
    elif st.session_state.step == 5: speak("계좌이체와 신용카드 중 결제 방식을 선택하세요.")
    elif st.session_state.step == 7: speak("스마트폰 미션을 성공적으로 마쳤습니다. 축하합니다.")
