import streamlit as st

# 1. 페이지 기본 설정 및 디자인 (에러 수정 및 UI 고급화)
st.set_page_config(page_title="디지털 친구 - 키오스크 연습 앱", layout="centered")

# CSS 스타일 정의 (버튼 크기 키우기, 글씨 확대, 기획안 색상 반영)
st.markdown("""
    <style>
    /* 전체 글꼴 크기 상향 */
    html, body, [data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
    }
    
    /* 일반 버튼 스타일 (이전, 홈으로 등) */
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
    
    /* 1단계: 메인 보라색 버튼 (연습 시작하기) */
    div[data-testid="stHorizontalBlock"] + div .stButton>button,
    .stButton>button[key*="start"], .stButton>button[key*="next"], .stButton>button[key*="pay"] {
        background-color: #6366F1 !important;
        color: white !important;
        border: none !important;
        height: 80px;
        font-size: 26px !important;
    }
    
    /* 상단 안내 문구 상자 */
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
    
    /* 메뉴판 안의 개별 아이템 카드 가로 정렬용 */
    .menu-card {
        background-color: white;
        border: 2px solid #E2E8F0;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* 주문 금액 표시 상자 */
    .price-box {
        background-color: #FEE2E2;
        color: #EF4444;
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 상태 관리 (기획안의 1~7단계 흐름 제어)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# 기획안 일치 메뉴판 데이터 (패스트푸드 기준)
MENU_DATA = {
    "햄버거": 5000,
    "치즈버거": 6000,
    "감자튀김": 2000,
    "콜라": 1500,
    "치킨너겟": 3000
}

# 총 주문 금액 계산 함수
def get_total_price():
    return sum(name * price for name, price in st.session_state.cart.items())

# 3. 음성 안내 함수 (스마트폰 브라우저 지원 TTS)
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


# --- 단계별 화면 구현 (기획안 100% 매칭) ---

# [1단계: 시작 화면]
if st.session_state.step == 1:
    st.markdown('<div class="guide-box">안녕하세요!<br>키오스크 연습을 시작해 볼까요?</div>', unsafe_allow_html=True)
    
    # 기획안 어르신 일러스트 영역 대체 이미지
    st.image("https://images.unsplash.com/photo-1581579438747-1dc8d17bbce4?w=500", use_container_width=True)
    
    if st.button("연습 시작하기", key="btn_start"):
        st.session_state.step = 2
        st.rerun()
    if st.button("사용 방법 보기", key="btn_howto"):
        st.info("키오스크 주문 순서를 그림과 음성으로 배우는 앱입니다.")

# [2단계: 업종 선택]
elif st.session_state.step == 2:
    st.markdown('<div class="guide-box">연습할 업종을 선택하세요</div>', unsafe_allow_html=True)
    
    if st.button("🍔 패스트푸드", key="biz_fastfood"):
        st.session_state.step = 3
        st.rerun()
    if st.button("☕ 카페", key="biz_cafe"):
        st.info("준비 중인 업종입니다. 패스트푸드를 먼저 연습해 보세요!")
    if st.button("🛒 마트", key="biz_mart"):
        st.info("준비 중인 업종입니다.")
    if st.button("🏥 병원 / 약국", key="biz_hospital"):
        st.info("준비 중인 업종입니다.")
        
    st.markdown("---")
    if st.button("🏠 홈으로", key="back_to_1"):
        st.session_state.step = 1
        st.rerun()

# [3단계: 메뉴 선택 (장바구니 담기)]
elif st.session_state.step == 3:
    st.markdown('<div class="guide-box">메뉴를 선택하세요</div>', unsafe_allow_html=True)
    
    # 기획안과 똑같은 메뉴 타일 배열 구성
    for menu_name, price in MENU_DATA.items():
        col_img, col_txt, col_btn = st.columns([1, 2, 1])
        with col_txt:
            st.markdown(f"**{menu_name}** \n{price:,}원")
        with col_btn:
            if st.button("담기", key=f"add_{menu_name}"):
                st.session_state.cart[menu_name] = st.session_state.cart.get(menu_name, 0) + 1
                speak(f"{menu_name}을 담았습니다.")
                st.rerun()
                
    # 주문 금액 실시간 표시
    total = get_total_price()
    st.markdown(f'<div class="price-box">주문 금액: {total:,}원</div>', unsafe_allow_html=True)
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("이전", key="prev_to_2"):
            st.session_state.cart = {}
            st.session_state.step = 2
            st.rerun()
    with col_next:
        if st.button("다음", key="next_to_4"):
            if total > 0:
                st.session_state.step = 4
                st.rerun()
            else:
                st.warning("메뉴를 최소 하나 이상 담아주세요!")

# [4단계: 주문 확인]
elif st.session_state.step == 4:
    st.markdown('<div class="guide-box">주문 내역을 확인하세요</div>', unsafe_allow_html=True)
    
    # 장바구니 리스트 영수증 형태로 표기
    st.markdown("| 메뉴 | 수량 | 금액 |")
    st.markdown("| :--- | :---: | :---: |")
    for name, qty in st.session_state.cart.items():
        item_total = MENU_DATA[name] * qty
        st.markdown(f"| {name} | {qty} | {item_total:,}원 |")
        
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
    if st.button("📱 간편결제 (삼성페이 등)", key="pay_samsung"):
        st.info("연습을 위해 [카드 결제]를 눌러보세요!")
    if st.button("💵 현금 결제", key="pay_cash"):
        st.info("이 키오스크는 카드 전용입니다. [카드 결제]를 선택해 주세요!")
        
    st.markdown("---")
    if st.button("이전", key="prev_to_4"):
        st.session_state.step = 4
        st.rerun()

# [6단계: 결제 방법 선택 (예시: 카드 투입 안내)]
elif st.session_state.step == 6:
    st.markdown('<div class="guide-box">카드를 넣어주세요</div>', unsafe_allow_html=True)
    
    # 카드 투입구 지시 이미지 영역 대체
    st.image("https://images.unsplash.com/photo-1563013544-824ae1d704d3?w=500", use_container_width=True)
    st.caption("※ 실제 결제는 되지 않습니다. 안심하고 연습하세요.")
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("이전", key="prev_to_5"):
            st.session_state.step = 5
            st.rerun()
    with col_next:
        if st.button("카드 넣기 완료 💳", key="pay_complete"):
            st.session_state.step = 7
            st.rerun()

# [7단계: 결제 완료 (연습 결과)]
elif st.session_state.step == 7:
    st.success("주문이 완료되었습니다! 🎉")
    st.markdown('<div class="guide-box">주문이 완료되었습니다!</div>', unsafe_allow_html=True)
    
    total = get_total_price()
    st.markdown(f'<div class="price-box" style="background-color:#DCFCE7; color:#16A34A;">주문 금액: {total:,}원</div>', unsafe_allow_html=True)
    st.write("※ 실제 결제는 되지 않았습니다. 연습이 완료되었습니다.")
    
    if st.button("처음으로 돌아가기", key="restart_app"):
        st.session_state.cart = {}
        st.session_state.step = 1
        st.rerun()


# --- 모바일 보안 정책 대응 단계별 자동 음성 안내 ---
if st.session_state.step == 2:
    speak("연습할 업종을 선택하세요.")
elif st.session_state.step == 3:
    speak("메뉴를 선택하세요. 다 고르셨으면 다음을 누르세요.")
elif st.session_state.step == 4:
    speak("주문 내역을 확인하세요. 맞으면 결제하기를 누르세요.")
elif st.session_state.step == 5:
    speak("결제 방법을 선택하세요. 카드 결제를 추천합니다.")
elif st.session_state.step == 6:
    speak("카드를 아래 투입구에 넣어주세요.")
elif st.session_state.step == 7:
    speak("축하합니다! 주문이 성공적으로 완료되었습니다.")
