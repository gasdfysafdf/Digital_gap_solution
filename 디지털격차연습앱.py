import streamlit as st

# 1. 페이지 기본 설정 및 스타일 정의
st.set_page_config(page_title="디지털 친구 - 어르신 스마트폰 & 키오스크 교육 앱", layout="centered")

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
    
    /* 좌석 선택용 특수 버튼 스타일 */
    div.stButton>button[key*="seat_"] {
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
if 'mode' not in st.session_state: st.session_state.mode = "MAIN" # MAIN, KIOSK, APP
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_biz' not in st.session_state: st.session_state.selected_biz = ""
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'pay_method' not in st.session_state: st.session_state.pay_method = ""

# 데이터 세팅
KIOSK_DATA = {
    "패스트푸드": {"햄버거": 5000, "치즈버거": 6000, "감자튀김": 2000, "콜라": 1500, "치킨너겟": 3000},
    "카페": {"아메리카노": 3000, "카페라떼": 3500, "바닐라라떼": 4000, "단팥빵": 2500, "조각케이크": 5000},
    "병원 / 약국": {"일반 진료비": 4500, "처방전 발행": 0, "영양제 수납": 15000, "보호 마스크": 3000}
}

def get_total_price():
    if st.session_state.mode == "APP":
        if st.session_state.selected_biz == "쇼핑": return 35000
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
# 🛑 [분기 1] 매장 키오스크 연습 모드
# ==========================================
elif st.session_state.mode == "KIOSK":
    
    # [1단계: 안내 및 시작]
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">실제 매장처럼 연습하고 실수해도 돈이 안 나가는<br>안전한 키오스크 연습 공간입니다!</div>', unsafe_allow_html=True)
        if st.button("키오스크 연습 시작하기 🏁", key="k_start"):
            st.session_state.step = 2
            st.rerun()
        if st.button("🏠 메인 화면으로 돌아가기", key="k_home"):
            st.session_state.mode = "MAIN"
            st.rerun()

    # [2단계: 업종 선택]
    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">연습하고 싶으신 장소를 눌러주세요.</div>', unsafe_allow_html=True)
        for biz in KIOSK_DATA.keys():
            if st.button(biz, key=f"k_biz_{biz}"):
                st.session_state.selected_biz = biz
                st.session_state.step = 3
                st.rerun()
        if st.button("⬅️ 뒤로가기", key="k_b2_1"): st.session_state.step = 1; st.rerun()

    # [3단계: 메뉴 고르기]
    elif st.session_state.step == 3:
        biz = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{biz}] 드실 메뉴판입니다.<br>원하는 음식을 누르고 [다음]을 누르세요.</div>', unsafe_allow_html=True)
        
        for name, price in KIOSK_DATA[biz].items():
            col_txt, col_btn = st.columns([3, 1])
            with col_txt: st.markdown(f"**{name}** ({price:,}원)")
            with col_btn:
                if st.button("담기", key=f"k_add_{name}"):
                    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
                    speak(f"{name} 장바구니 추가.")
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

    # [4단계: 주문 확인]
    elif st.session_state.step == 4:
        st.markdown('<div class="guide-box">내가 고른 메뉴가 맞는지 확인해 보세요.</div>', unsafe_allow_html=True)
        for name, qty in st.session_state.cart.items():
            st.markdown(f"■ **{name}** : {qty}개 — {KIOSK_DATA[st.session_state.selected_biz][name]*qty:,}원")
        
        total = get_total_price()
        st.markdown(f'<div class="price-box">최종 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
        
        col_p, col_n = st.columns(2)
        with col_p: id = st.button("이전", key="k_b4_3"); st.session_state.step=3 if id else st.session_state.step
        with col_n: 
            if st.button("결제하기", key="k_n4_5"): st.session_state.step = 5; st.rerun()

    # [5단계: 결제 방법 선택 (★ 분기 처리)]
    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">어떻게 결제하시겠습니까?<br>연습하고 싶은 방식을 선택하세요!</div>', unsafe_allow_html=True)
        
        if st.button("💵 현금 결제 (지폐/동전 넣기)", key="k_pay_cash"):
            st.session_state.pay_method = "현금"
            st.session_state.step = 7 # 현금은 투입 가이드 없이 바로 완료로 패스
            speak("현금 결제가 선택되었습니다.")
            st.rerun()
            
        if st.button("💳 신용카드 결제", key="k_pay_card"):
            st.session_state.pay_method = "카드"
            st.session_state.step = 6
            st.rerun()
            
        if st.button("📱 간편결제 (삼성페이 / 카카오페이)", key="k_pay_nfc"):
            st.session_state.pay_method = "간편결제"
            st.session_state.step = 6
            st.rerun()
            
        if st.button("이전으로", key="k_b5_4"): st.session_state.step = 4; st.rerun()

    # [6단계: 결제 진행 세부 가이드 (카드 vs 간편결제)]
    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">IC칩이 위로 향하게 카드를 끝까지 넣어주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-hand-holding-smartphone-with-nfc-payment-isolated-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
            if st.button("카드 넣기 완료 💳", key="k_card_complete"): st.session_state.step = 7; st.rerun()
            
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">스마트폰 뒷면을 키오스크 기계의<br>[NFC 마크/리더기] 부위에 가까이 대어 주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("스마트폰 인식 완료 📱", key="k_nfc_complete"): st.session_state.step = 7; st.rerun()
            
        if st.button("이전으로", key="k_b6_5"): st.session_state.step = 5; st.rerun()

    # [7단계: 주문 성공 완료]
    elif st.session_state.step == 7:
        st.success("🎉 키오스크 주문 성공!")
        total = get_total_price()
        if st.session_state.pay_method == "현금":
            st.markdown(f'<div class="guide-box" style="background-color:#E0F2FE;">현금 결제가 완료되었습니다!<br>지출 금액: {total:,}원</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="guide-box" style="background-color:#DCFCE7;">주문이 정상적으로 끝났습니다!<br>총 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
            
        st.write("훌륭합니다! 매장 키오스크 훈련 과정을 마스터하셨습니다.")
        if st.button("메인 화면으로 가기 🏠", key="k_finish"):
            st.session_state.mode = "MAIN"
            st.rerun()


# ==========================================
# 🛑 [분기 2] 스마트폰 필수 앱 연습 모드 (신규 대형 기능)
# ==========================================
elif st.session_state.mode == "APP":
    
    # [1단계: 안내 및 시작]
    if st.session_state.step == 1:
        st.markdown('<div class="guide-box">스마트폰으로 물건을 사고, 돈을 보내고,<br>차표를 예약하는 복잡한 과정을 쉽게 연습하는 곳입니다!</div>', unsafe_allow_html=True)
        if st.button("스마트폰 앱 연습 시작하기 🏁", key="a_start"):
            st.session_state.step = 2
            st.rerun()
        if st.button("🏠 메인 화면으로 돌아가기", key="a_home"):
            st.session_state.mode = "MAIN"
            st.rerun()

    # [2단계: 앱 종류 선택]
    elif st.session_state.step == 2:
        st.markdown('<div class="guide-box">어떤 스마트폰 기능을 연습해 볼까요?</div>', unsafe_allow_html=True)
        
        if st.button("🛍️ 1. 인터넷 쇼핑 (쿠팡처럼 물건 사기)", key="a_biz_shop"):
            st.session_state.selected_biz = "쇼핑"; st.session_state.step = 3; st.rerun()
        if st.button("🏦 2. 은행 앱 (자녀에게 계좌 송금하기)", key="a_biz_bank"):
            st.session_state.selected_biz = "은행(송금)"; st.session_state.step = 3; st.rerun()
        if st.button("📅 3. 버스 예매 (고속버스 좌석 지정 예약을 똑같이)", key="a_biz_bus"):
            st.session_state.selected_biz = "고속버스 예매"; st.session_state.step = 3; st.rerun()
            
        st.markdown("---")
        if st.button("⬅   뒤로가기", key="a_b2_1"): st.session_state.step = 1; st.rerun()

    # [3단계: 각 앱별 전용 실전 입력 단계]
    elif st.session_state.step == 3:
        app_type = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">[{app_type} 단계] 실제 화면처럼 빈칸을 누르거나 채워보세요.</div>', unsafe_allow_html=True)
        
        if app_type == "쇼핑":
            st.image("https://img.freepik.com/free-vector/order-delivery-concept-illustration_114360-1231.jpg?w=300", use_container_width=True)
            st.markdown("🛒 **추천 상품: 시골 국산 유기농 쌀 10kg**\n\n가격: 35,000원")
            st.text_input("🏠 받으실 주소 입력 예시", "서울특별시 종로구 세종대로 1번지 경로당 앞")
            if st.button("🛒 장바구니 담고 바로 구매하기", key="app_shop_next"): st.session_state.step = 4; st.rerun()
            
        elif app_type == "은행(송금)":
            st.image("https://img.freepik.com/free-vector/transfer-money-concept-illustration_114360-3762.jpg?w=300", use_container_width=True)
            st.selectbox("🏦 보낼 은행 선택", ["국민은행", "농협은행", "신한은행", "카카오뱅크"])
            st.text_input("🔢 상대방 계좌번호 입력", "302-1234-5678-90")
            st.text_input("💵 보낼 금액", "50,000 원 (용돈)")
            if st.button("보내기 확인 단계로", key="app_bank_next"): st.session_state.step = 4; st.rerun()
            
        elif app_type == "고속버스 예매":
            st.markdown("🚍 **여정: 서울경부 ➡️ 부산종합버스터미널**")
            st.markdown("💡 **비어있는 원하는 좌석 번호를 누르세요 (예: 11번, 12번)**")
            
            # 좌석 배열 시뮬레이션
            c1, c2, c3 = st.columns(3)
            with c1: st.button("💺 09 (예약됨)", disabled=True)
            with c2: st.button("💺 10 (예약됨)", disabled=True)
            with c3: 
                if st.button("💺 11 (선택 가능)", key="seat_11"): speak("11번 좌석이 선택되었습니다."); st.session_state.step = 4; st.rerun()
            
            if st.button("💺 12 (선택 가능)", key="seat_12"): speak("12번 좌석이 선택되었습니다."); st.session_state.step = 4; st.rerun()

        if st.button("⬅   이전단계로", key="a_b3_2"): st.session_state.step = 2; st.rerun()

    # [4단계: 스마트폰 앱용 최종 확인창]
    elif st.session_state.step == 4:
        app_type = st.session_state.selected_biz
        st.markdown(f'<div class="guide-box">마지막으로 정보가 맞는지 검토하세요.</div>', unsafe_allow_html=True)
        
        total = get_total_price()
        if app_type == "쇼핑": st.write(f"■ 결제 상품 : 국산 유기농 쌀 10kg\n\n■ 결제 예정 금액 : {total:,}원")
        elif app_type == "은행(송금)": st.write(f"■ 송금 대상 : 지정 계좌번호\n\n■ 송금 금액 : {total:,}원")
        elif app_type == "고속버스 예매": st.write(f"■ 예약 내역 : 서울발 부산행 고속버스 1석\n\n■ 결제 금액 : {total:,}원")
            
        col_p, col_n = st.columns(2)
        with col_p: 
            if st.button("이전으로", key="a_b4_3"): st.session_state.step = 3; st.rerun()
        with col_n:
            if st.button("다음 (결제/인증)", key="a_n4_5"): st.session_state.step = 5; st.rerun()

    # [5단계: 스마트폰용 결제 수단 분기 처리 (★ 현금/간편결제 동일 로직 연동)]
    elif st.session_state.step == 5:
        st.markdown('<div class="guide-box">스마트폰 앱에서 결제할 수단을 골라주세요.</div>', unsafe_allow_html=True)
        
        if st.button("💵 무통장 입금 (현금 결제 방식)", key="a_pay_cash"):
            st.session_state.pay_method = "현금"
            st.session_state.step = 7 # 즉시 완료로 패스
            speak("무통장 입금 방식이 확인되었습니다.")
            st.rerun()
            
        if st.button("💳 등록된 신용카드 결제", key="a_pay_card"):
            st.session_state.pay_method = "카드"
            st.session_state.step = 6
            st.rerun()
            
        if st.button("📱 스마트폰 페이 간편결제", key="a_pay_nfc"):
            st.session_state.pay_method = "간편결제"
            st.session_state.step = 6
            st.rerun()
            
        if st.button("이전으로", key="a_b5_4"): st.session_state.step = 4; st.rerun()

    # [6단계: 스마트폰 세부 결제 액션]
    elif st.session_state.step == 6:
        if st.session_state.pay_method == "카드":
            st.markdown('<div class="guide-box">스마트폰 뒤에 실물카드를 터치하거나<br>카드 비밀번호 앞 2자리를 입력하는 단계입니다.</div>', unsafe_allow_html=True)
            st.text_input("🔒 카드 비밀번호 앞 2자리 입력 연습", value="", type="password", placeholder="**")
            if st.button("결제 인증 완료 💳", key="a_card_complete"): st.session_state.step = 7; st.rerun()
            
        elif st.session_state.pay_method == "간편결제":
            st.markdown('<div class="guide-box">스마트폰 NFC 결제 신호 송출 중...<br>핸드폰 뒷면을 카드 단말기에 가져다 대거나<br>지문 인증을 진행해 주세요.</div>', unsafe_allow_html=True)
            st.image("https://img.freepik.com/free-vector/contactless-payment-concept-illustration_114360-6395.jpg?w=500", use_container_width=True)
            if st.button("간편 지문/NFC 인식 완료 📱", key="a_nfc_complete"): st.session_state.step = 7; st.rerun()
            
        if st.button("이전으로", key="a_b6_5"): st.session_state.step = 5; st.rerun()

    # [7단계: 앱 시나리오 최종 완료]
    elif st.session_state.step == 7:
        st.success("🎉 스마트폰 미션 최종 성공!")
        total = get_total_price()
        app_type = st.session_state.selected_biz
        
        if st.session_state.pay_method == "현금":
            st.markdown(f'<div class="guide-box" style="background-color:#E0F2FE;">[{app_type}] 무통장 현금 입금 예약이 완료되었습니다.<br>입금 총액: {total:,}원</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="guide-box" style="background-color:#DCFCE7;">[{app_type}] 결제 및 처리가 정상 완료되었습니다!<br>이용 금액: {total:,}원</div>', unsafe_allow_html=True)
            
        st.write("처음에는 낯설지만 매일 한 번씩 연습하면 스마트폰 달인이 될 수 있습니다!")
        if st.button("대메뉴 초기화면으로 이동 🏠", key="a_finish"):
            st.session_state.mode = "MAIN"
            st.rerun()


# --- 전 단계 모바일 타겟 보이스 세팅 ---
if st.session_state.mode == "KIOSK":
    if st.session_state.step == 2: speak("연습하고 싶으신 장소를 눌러주세요.")
    elif st.session_state.step == 3: speak("원하는 음식을 누르고 아래의 다음 버튼을 누르세요.")
    elif st.session_state.step == 4: speak("내가 고른 메뉴가 맞는지 확인해 보세요.")
    elif st.session_state.step == 5: speak("결제 방법을 선택하세요.")
    elif st.session_state.step == 7: speak("축하합니다! 키오스크 주문에 성공하셨습니다.")
elif st.session_state.mode == "APP":
    if st.session_state.step == 2: speak("어떤 스마트폰 기능을 연습해 볼까요?")
    elif st.session_state.step == 3: speak("실제 스마트폰 화면처럼 빈칸을 채우거나 선택해 보세요.")
    elif st.session_state.step == 4: speak("마지막으로 입력한 정보가 맞는지 검토하세요.")
    elif st.session_state.step == 5: speak("스마트폰에서 결제할 수단을 골라주세요.")
    elif st.session_state.step == 7: speak("축하합니다! 스마트폰 미션을 완벽하게 성공하셨습니다.")
