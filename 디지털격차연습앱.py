import streamlit as st

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(page_title="디지털 친구 - 키오스크 연습 앱", layout="centered")

st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
    }
    
    .stButton>button {
        width: 100%;
        height: 70px;
        font-size: 24px !important;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #CBD5E1;
        background-color: #F8FAFC;
        color: #1E293B;
    }
    
    /* 강조 버튼 스타일 지정 */
    div.stButton>button[key*="start"], div.stButton>button[key*="next"], div.stButton>button[key*="pay"] {
        background-color: #6366F1 !important;
        color: white !important;
        border: none !important;
        height: 80px;
        font-size: 26px !important;
    }
    
    .guide-box {
        font-size: 28px;
        font-weight: bold;
        color: #1E293B;
        text-align: center;
        background-color: #F1F5F9;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        border-bottom: 4px solid #CBD5E1;
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

# 2. 상태 관리 및 업종별 메뉴 데이터 정의
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_biz' not in st.session_state: st.session_state.selected_biz = ""
if 'cart' not in st.session_state: st.session_state.cart = {}

# 전 업종 메뉴판 데이터 (기획안 연동 가격 구성)
BIZ_MENUS = {
    "패스트푸드": {
        "햄버거": 5000,
        "치즈버거": 6000,
        "감자튀김": 2000,
        "콜라": 1500,
        "치킨너겟": 3000
    },
    "카페": {
        "아메리카노": 3000,
        "카페라떼": 3500,
        "바닐라라떼": 4000,
        "단팥빵": 2500,
        "조각케이크": 5000
    },
    "병원 / 약국": {
        "진료비 수납": 4500,
        "처방전 발행": 0,
        "영양제 구입": 15000,
        "마스크(5매)": 3000
    }
}

# 에러 원인이었던 총금액 계산 함수 완벽 수정
def get_total_price():
    biz = st.session_state.selected_biz
    if not biz or biz not in BIZ_MENUS:
        return 0
    total = 0
    for item_name, qty in st.session_state.cart.items():
        price = BIZ_MENUS[biz].get(item_name, 0)
        total += price * qty
    return total

def speak(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'ko-KR';
    msg.rate = 0.85; 
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)


# --- 7단계 실전 흐름 구현 ---

# [1단계: 시작 화면]
if st.session_state.step == 1:
    st.markdown('<div class="guide-box">안녕하세요!<br>키오스크 연습을 시작해 볼까요?</div>', unsafe_allow_html=True)
    
    # 어르신 일러스트 느낌의 밝고 친근한 만화풍 이미지로 교체
    st.image("https://img.freepik.com/free-vector/happy-grandparents-concept-illustration_114360-6644.jpg?w=500", use_container_width=True)
    
    if st.button("연습 시작하기", key="btn_start"):
        st.session_state.step = 2
        st.rerun()
    if st.button("사용 방법 보기", key="btn_howto"):
        st.info("키오스크 주문 순서를 그림과 음성으로 차근차근 배우는 체험형 앱입니다.")

# [2단계: 업종 선택]
elif st.session_state.step == 2:
    st.markdown('<div class="guide-box">연습할 업종을 선택하세요</div>', unsafe_allow_html=True)
    
    if st.button("🍔 패스트푸드", key="biz_fast"):
        st.session_state.selected_biz = "패스트푸드"
        st.session_state.cart = {}
        st.session_state.step = 3
        st.rerun()
        
    if st.button("☕ 카페", key="biz_cafe"):
        st.session_state.selected_biz = "카페"
        st.session_state.cart = {}
        st.session_state.step = 3
        st.rerun()
        
    if st.button("🏥 병원 / 약국", key="biz_hosp"):
        st.session_state.selected_biz = "병원 / 약국"
        st.session_state.cart = {}
        st.session_state.step = 3
        st.rerun()
        
    st.markdown("---")
    if st.button("🏠 처음으로", key="back_to_1"):
        st.session_state.step = 1
        st.rerun()

# [3단계: 메뉴 선택]
elif st.session_state.step == 3:
    biz = st.session_state.selected_biz
    st.markdown(f'<div class="guide-box">[{biz}] 메뉴를 선택하세요</div>', unsafe_allow_html=True)
    
    # 선택된 업종의 메뉴 리스트 유연하게 출력
    current_menu = BIZ_MENUS[biz]
    for menu_name, price in current_menu.items():
        col_txt, col_btn = st.columns([3, 1])
        with col_txt:
            price_display = f"{price:,}원" if price > 0 else "무료 가이드"
            st.markdown(f"**{menu_name}** ({price_display})")
        with col_btn:
            if st.button("담기", key=f"add_{menu_name}"):
                st.session_state.cart[menu_name] = st.session_state.cart.get(menu_name, 0) + 1
                speak(f"{menu_name}을 담았습니다.")
                st.rerun()
                
    total = get_total_price()
    st.markdown(f'<div class="price-box">주문 금액: {total:,}원</div>', unsafe_allow_html=True)
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("이전", key="prev_to_2"):
            st.session_state.step = 2
            st.rerun()
    with col_next:
        if st.button("다음", key="next_to_4"):
            if len(st.session_state.cart) > 0:
                st.session_state.step = 4
                st.rerun()
            else:
                st.warning("메뉴를 하나 이상 골라주세요!")

# [4단계: 주문 확인]
elif st.session_state.step == 4:
    st.markdown('<div class="guide-box">주문 내역을 확인하세요</div>', unsafe_allow_html=True)
    
    biz = st.session_state.selected_biz
    st.markdown("| 선택한 항목 | 수량 | 금액 |")
    st.markdown("| :--- | :---: | :---: |")
    for name, qty in st.session_state.cart.items():
        item_total = BIZ_MENUS[biz][name] * qty
        st.markdown(f"| {name} | {qty} 개 | {item_total:,}원 |")
        
    total = get_total_price()
    st.markdown(f'<div class="price-box">총 주문 금액: {total:,}원</div>', unsafe_allow_html=True)
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("이전", key="prev_to_3"):
            st.session_state.step = 3
            st.rerun()
    with col_next:
        if st.button("결제하기", key="next_to_5"):
            st.session_state.step = 5
            st.rerun()

# [5단계: 결제 방법 선택]
elif st.session_state.step == 5:
    st.markdown('<div class="guide-box">결제 방법을 선택하세요</div>', unsafe_allow_html=True)
    
    if st.button("💳 카드 결제", key="pay_card"):
        st.session_state.step = 6
        st.rerun()
    if st.button("📱 간편결제 (삼성페이 등)", key="pay_easy"):
        st.info("[카드 결제] 버튼을 눌러 결제 연습을 계속 진행해 보세요!")
    if st.button("💵 현금 결제", key="pay_cash"):
        st.info("이 기오스크는 카드 전용입니다. [카드 결제]를 눌러주세요!")
        
    st.markdown("---")
    if st.button("이전", key="prev_to_4"):
        st.session_state.step = 4
        st.rerun()

# [6단계: 카드 투입 안내]
elif st.session_state.step == 6:
    st.markdown('<div class="guide-box">카드를 넣어주세요</div>', unsafe_allow_html=True)
    
    # 깔끔한 일러스트 카드 투입 이미지 적용
    st.image("https://img.freepik.com/free-vector/pos-terminal-inserted-credit-card-hand-holding-smartphone-with-nfc-payment-isolated-cartoon-illustration_107791-3860.jpg?w=500", use_container_width=True)
    st.caption("※ 실제 결제는 진행되지 않는 모의 교육용 화면입니다.")
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("이전", key="prev_to_5"):
            st.session_state.step = 5
            st.rerun()
    with col_next:
        if st.button("카드 넣기 완료 💳", key="pay_complete"):
            st.session_state.step = 7
            st.rerun()

# [7단계: 결제 및 연습 완료]
elif st.session_state.step == 7:
    st.success("주문이 완료되었습니다! 🎉")
    st.markdown('<div class="guide-box">주문이 성공적으로 끝났습니다!</div>', unsafe_allow_html=True)
    
    total = get_total_price()
    st.markdown(f'<div class="price-box" style="background-color:#DCFCE7; color:#16A34A;">총 결제 금액: {total:,}원</div>', unsafe_allow_html=True)
    st.write("참 잘하셨습니다! 이제 실제 매장에서도 두려움 없이 주문하실 수 있습니다.")
    
    if st.button("처음으로 돌아가기", key="restart_app"):
        st.session_state.cart = {}
        st.session_state.selected_biz = ""
        st.session_state.step = 1
        st.rerun()


# --- 음성 안내 연동 로직 ---
if st.session_state.step == 2:
    speak("연습할 업종을 선택하세요.")
elif st.session_state.step == 3:
    speak("원하는 메뉴를 담고 다음 버튼을 누르세요.")
elif st.session_state.step == 4:
    speak("주문 내역을 확인하신 후 결제하기를 누르세요.")
elif st.session_state.step == 5:
    speak("결제 방법을 선택하세요.")
elif st.session_state.step == 6:
    speak("카드를 카드 투입구에 넣어주세요.")
elif st.session_state.step == 7:
    speak("축하합니다! 주문이 완료되었습니다. 처음부터 다시 연습할 수 있습니다.")
