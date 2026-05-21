import streamlit as st

# 1. 페이지 기본 설정 (큰 폰트와 깔끔한 레이아웃)
st.set_page_config(page_title="디지털 친구 - 키오스크 연습", layout="centered")

# CSS를 사용하여 어르신 맞춤형 스타일 적용 (큰 버튼, 큰 글씨)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 120px;
        font-size: 30px !important;
        font-weight: bold;
        border-radius: 20px;
        background-color: #F59E0B;
        color: white;
        margin-bottom: 20px;
    }
    .stButton>button:hover {
        background-color: #D97706;
        border: 2px solid #FFF;
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        color: #1E293B;
        text-align: center;
        margin-bottom: 30px;
    }
    .guide-text {
        font-size: 28px;
        color: #475569;
        text-align: center;
        background-color: #FEF3C7;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #F59E0B;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 상태 관리 (현재 어느 단계인지 추적)
if 'step' not in st.session_state:
    st.session_state.step = "HOME"
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 3. 음성 안내 함수 (브라우저의 TTS 사용)
def speak(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'ko-KR';
    msg.rate = 0.8; 
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 화면 구성 시작 ---

if st.session_state.step == "HOME":
    st.markdown('<div class="main-title">안녕하세요! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="guide-text">원하시는 장소를 눌러보세요.<br>실제 돈은 나가지 않으니 안심하세요!</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☕ 카페 (커피)"):
            st.session_state.step = "CAFE_MENU"
            st.rerun()
    with col2:
        if st.button("🍔 식당 (버거)"):
            st.info("준비 중인 시나리오입니다.")

elif st.session_state.step == "CAFE_MENU":
    st.markdown('<div class="main-title">무엇을 마실까요? ☕</div>', unsafe_allow_html=True)
    st.markdown('<div class="guide-text">드시고 싶은 음료를 하나 골라주세요.</div>', unsafe_allow_html=True)
    
    menu = {
        "따뜻한 아메리카노": "3,000원",
        "시원한 아메리카노": "3,500원",
        "달콤한 카페라떼": "4,000원",
        "건강한 대추차": "4,500원"
    }
    
    for name, price in menu.items():
        if st.button(f"{name} ({price})"):
            st.session_state.cart.append(name)
            st.session_state.step = "CONFIRM"
            st.rerun()
    
    if st.button("⬅️ 처음으로 돌아가기"):
        st.session_state.step = "HOME"
        st.rerun()

elif st.session_state.step == "CONFIRM":
    st.markdown('<div class="main-title">주문을 확인해요 ✅</div>', unsafe_allow_html=True)
    item = st.session_state.cart[-1]
    st.markdown(f'<div class="guide-text">선택하신 음료: <b>{item}</b><br>주문하시겠습니까?</div>', unsafe_allow_html=True)
    
    if st.button("✅ 네, 주문할게요"):
        st.session_state.step = "PAYMENT"
        st.rerun()
    
    if st.button("❌ 아니오, 다시 고를래요"):
        st.session_state.cart = []
        st.session_state.step = "CAFE_MENU"
        st.rerun()

elif st.session_state.step == "PAYMENT":
    st.markdown('<div class="main-title">결제 연습 💳</div>', unsafe_allow_html=True)
    st.markdown('<div class="guide-text">신용카드를 넣는 곳에 카드를 넣어주세요.<br>(연습이므로 아무 카드나 괜찮아요!)</div>', unsafe_allow_html=True)
    
    if st.button("💳 카드 넣기 완료"):
        st.session_state.step = "SUCCESS"
        st.rerun()

elif st.session_state.step == "SUCCESS":
    st.balloons()
    st.markdown('<div class="main-title">주문 성공! 🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="guide-text">축하합니다! 주문을 완료하셨어요.<br>이제 실제 카페에서도 자신 있게 주문해 보세요!</div>', unsafe_allow_html=True)
    
    if st.button("🏠 처음으로 돌아가기"):
        st.session_state.step = "HOME"
        st.session_state.cart = []
        st.rerun()

# 단계별 음성 안내 자동 실행 (페이지 렌더링 시)
if st.session_state.step == "HOME": speak("안녕하세요. 원하시는 장소를 눌러보세요.")
elif st.session_state.step == "CAFE_MENU": speak("무엇을 마실까요? 드시고 싶은 음료를 하나 골라주세요.")
elif st.session_state.step == "CONFIRM": speak("주문 내용을 확인해 주세요. 맞으면 네, 틀리면 아니오를 누르세요.")
elif st.session_state.step == "PAYMENT": speak("결제 연습입니다. 카드를 넣어주세요.")
elif st.session_state.step == "SUCCESS": speak("축하합니다! 주문에 성공하셨습니다.")
