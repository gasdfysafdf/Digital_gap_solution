# 디지털격차연습앱.py (최종 업그레이드 버전)
import streamlit as st

# 1. 페이지 기본 설정 및 디자인 (완전 업그레이드)
st.set_page_config(page_title="디지털 친구 v2 - 실전 연습", layout="centered")

# CSS를 사용하여 실제 키오스크 같은 이미지 타일 UI 구현
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 15px;
        font-weight: bold;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(0,0,0,0.15);
    }
    /* 메인 큰 버튼 (시작하기, 완료 등) */
    .start-btn {
        width: 100% !important;
        height: 120px !important;
        font-size: 30px !important;
        background-color: #F59E0B !important;
        color: white !important;
        margin-top: 20px !important;
    }
    /* 메뉴 타일 버튼 (이미지 + 텍스트) */
    .menu-btn {
        width: 100% !important;
        height: auto !important;
        min-height: 220px !important;
        font-size: 22px !important;
        background-color: white !important;
        color: #1E293B !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        padding: 20px !important;
    }
    /* 선택 완료/장바구니 확인 버튼 */
    .cart-btn {
        width: 100% !important;
        height: 70px !important;
        font-size: 24px !important;
        background-color: #1E293B !important;
        color: white !important;
        margin-top: 20px !important;
    }
    .main-title {
        font-size: 45px;
        font-weight: bold;
        color: #1E293B;
        text-align: center;
        margin-bottom: 25px;
    }
    .guide-text {
        font-size: 26px;
        color: #475569;
        text-align: center;
        background-color: #FEF3C7;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #F59E0B;
        margin-bottom: 40px;
        line-height: 1.4;
    }
    /* 메뉴 이미지 스타일 */
    .menu-img {
        width: 100%;
        max-width: 180px;
        height: 120px;
        object-fit: contain;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 상태 관리 및 메뉴 데이터
if 'step' not in st.session_state: st.session_state.step = "HOME"
if 'cart' not in st.session_state: st.session_state.cart = []
if 'total_price' not in st.session_state: st.session_state.total_price = 0

# 이미지 URL 데이터 (사용자 구상안에 맞춘 실제 이미지)
IMG_URLS = {
    "버거": "http://googleusercontent.com/image_collection/image_retrieval/1066491796677931008",
    "커피": "http://googleusercontent.com/image_collection/image_retrieval/11417890954816535125",
    "아메리카노": "http://googleusercontent.com/image_collection/image_retrieval/11417890954816535125",
    "카페라떼": "http://googleusercontent.com/image_collection/image_retrieval/11417890954816535125",
    "대추차": "http://googleusercontent.com/image_collection/image_retrieval/11417890954816535125",
    "치즈버거": "http://googleusercontent.com/image_collection/image_retrieval/1066491796677931008",
    "새우버거": "http://googleusercontent.com/image_collection/image_retrieval/1066491796677931008",
    "치킨버거": "http://googleusercontent.com/image_collection/image_retrieval/1066491796677931008",
    "감자튀김": "http://googleusercontent.com/image_collection/image_retrieval/1206129321743048704",
    "콜라": "http://googleusercontent.com/image_collection/image_retrieval/1206129321743048704",
    "신용카드": "http://googleusercontent.com/image_collection/image_retrieval/4988231667140896185",
    "성공": "http://googleusercontent.com/image_collection/image_retrieval/3456165767797042465"
}

# 3. 음성 안내 함수 (수정 없음)
def speak(text):
    js_code = f"<script>var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'ko-KR'; msg.rate = 0.8; window.speechSynthesis.speak(msg);</script>"
    st.components.v1.html(js_code, height=0)

# 4. 공통 함수: 메뉴 타일 버튼 생성
def menu_tile_button(col, label, price_raw, key):
    with col:
        price_str = f"{price_raw:,}원" if price_raw > 0 else ""
        button_label = f"| <img src='{IMG_URLS.get(label, '')}' class='menu-img'> | <br>**{label}** | <br>{price_str}"
        if st.button(button_label, key=key, type="menu"):
            st.session_state.cart.append({"name": label, "price": price_raw})
            st.session_state.total_price += price_raw
            speak(f"{label}이 장바구니에 담겼습니다.")
            st.rerun()

# --- 화면 구성 시작 (v2 완전 업그레이드) ---

if st.session_state.step == "HOME":
    st.markdown('<div class="main-title">디지털 격차 해소</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">키오스크 연습 앱</div>', unsafe_allow_html=True)
    st.markdown('<div class="guide-text">원하시는 메뉴를 직접 사진으로 보며<br>편안하게 연습해 보세요.</div>', unsafe_allow_html=True)
    
    if st.button("연습 시작하기 👋", key="start_btn", type="start"):
        st.session_state.step = "PLACE_SELECT"
        st.rerun()

elif st.session_state.step == "PLACE_SELECT":
    st.markdown('<div class="main-title">장소 선택 🏬</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    # 더 진짜 같은 이미지 타일로 변경
    menu_tile_button(col1, "버거", 0, "select_burger")
    menu_tile_button(col2, "커피", 0, "select_cafe")
    
    if st.session_state.cart:
        if st.button("처음으로 돌아가기", key="back_home", type="cart"):
             st.session_state.cart = []; st.session_state.total_price = 0; st.session_state.step = "HOME"; st.rerun()

    # 분기 처리
    if any(item['name'] == '버거' for item in st.session_state.cart): st.session_state.step = "BURGER_MENU"; st.session_state.cart = []; st.session_state.total_price = 0; st.rerun()
    elif any(item['name'] == '커피' for item in st.session_state.cart): st.session_state.step = "CAFE_MENU"; st.session_state.cart = []; st.session_state.total_price = 0; st.rerun()

# --- 버거 메뉴 구현부 (신규) ---
elif st.session_state.step == "BURGER_MENU":
    st.markdown('<div class="main-title">맛있는 버거 고르기 🍔</div>', unsafe_allow_html=True)
    st.markdown('<div class="guide-text">드시고 싶은 버거를 하나 선택해 주세요.<br>(사이드 메뉴는 다음 단계에서 나옵니다.)</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    menu_tile_button(col1, "치즈버거", 5500, "menu_cheese")
    menu_tile_button(col2, "새우버거", 6000, "menu_shrimp")
    menu_tile_button(col3, "치킨버거", 6500, "menu_chicken")

    if st.session_state.cart:
        if st.button(f"장바구니 확인 ({st.session_state.total_price:,}원)", key="go_cart", type="cart"):
            st.session_state.step = "CONFIRM"
            st.rerun()
    if st.button("⬅️ 뒤로가기", key="back_place", type="cart"): st.session_state.step = "PLACE_SELECT"; st.session_state.cart = []; st.session_state.total_price = 0; st.rerun()

# --- 장바구니 확인 및 주문 완료까지 (v2 스타일 적용) ---
elif st.session_state.step == "CONFIRM":
    st.markdown('<div class="main-title">주문 확인해요 ✅</div>', unsafe_allow_html=True)
    
    # 장바구니 목록을 좀 더 진짜처럼 표시
    st.markdown('<div class="guide-text">이대로 주문하시겠습니까?</div>', unsafe_allow_html=True)
    for i, item in enumerate(st.session_state.cart, 1):
        st.write(f"**{i}. {item['name']}** - {item['price']:,}원")
    st.markdown("---")
    st.write(f"### 총 금액: **{st.session_state.total_price:,}원**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 네, 주문할게요", key="confirm_yes", type="start"):
            st.session_state.step = "PAYMENT"; st.rerun()
    with col2:
        if st.button("❌ 다시 고를래요", key="confirm_no", type="cart"):
            st.session_state.cart = []; st.session_state.total_price = 0; st.session_state.step = "BURGER_MENU"; st.rerun()

elif st.session_state.step == "PAYMENT":
    st.markdown('<div class="main-title">결제 연습 💳</div>', unsafe_allow_html=True)
    st.image(IMG_URLS["신용카드"], use_column_width=True)
    st.markdown('<div class="guide-text">신용카드를 넣는 곳에 카드를 넣어주세요.<br>(연습이므로 아무 카드나 괜찮아요!)</div>', unsafe_allow_html=True)
    
    if st.button("💳 카드 넣기 완료", key="pay_done", type="start"):
        st.session_state.step = "SUCCESS"; st.rerun()

elif st.session_state.step == "SUCCESS":
    st.balloons()
    st.markdown('<div class="main-title">주문 성공! 🎉</div>', unsafe_allow_html=True)
    st.image(IMG_URLS["성공"], use_column_width=True)
    st.markdown('<div class="guide-text">축하합니다! 주문을 완료하셨어요.<br>실제 매장에서도 자신 있게 도전해 보세요!</div>', unsafe_allow_html=True)
    
    if st.button("🏠 처음으로 돌아가기", key="final_home", type="start"):
        st.session_state.step = "HOME"; st.session_state.cart = []; st.session_state.total_price = 0; st.rerun()

# 5. 단계별 음성 안내 자동 실행 (수정 없음, 모바일 보안 정책 고려)
if st.session_state.step == "HOME": pass # 시작 버튼 누르며 음성 시작 유도
elif st.session_state.step == "PLACE_SELECT": speak("안녕하세요! 원하시는 장소를 직접 사진으로 보고 눌러보세요.")
elif st.session_state.step == "BURGER_MENU": speak("맛있는 버거를 골라주세요. 다 고르셨으면 아래 장바구니 확인 버튼을 누르세요.")
elif st.session_state.step == "CONFIRM": speak("주문 내용을 확인해 주세요. 이대로 주문하시겠습니까?")
elif st.session_state.step == "PAYMENT": speak("결제 연습입니다. 카드를 넣어주세요.")
elif st.session_state.step == "SUCCESS": speak("축하합니다! 주문에 성공하셨습니다.")
