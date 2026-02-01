import streamlit as st

# ---------------------------------------------------------
# 1. 데이터 준비
# ---------------------------------------------------------
menu_data = {
    "식사류": {"순대국밥": 10000, "내장국밥": 10000, "얼큰국밥": 11000, "고기만": 10000},
    "안주류": {"모둠순대": 15000, "머리고기": 18000, "술국": 15000},
    "음료/주류": {"콜라": 2000, "사이다": 2000, "소주": 5000, "맥주": 5000}
}

# ---------------------------------------------------------
# 2. 기억 장치 (Session State)
# ---------------------------------------------------------
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# ---------------------------------------------------------
# 3. 화면 레이아웃
# ---------------------------------------------------------
st.set_page_config(layout="wide")
st.title("🍚 코딩국밥 키오스크 (수량 기능 추가)")

col_menu, col_cart = st.columns([0.7, 0.3])

# === [왼쪽 구역] 메뉴판 ===
with col_menu:
    tab1, tab2, tab3 = st.tabs(["🥘 식사류", "🍖 안주류", "🥤 음료/주류"])

    # 메뉴 버튼 함수 (여기가 변경되었습니다!)
    def show_menu_buttons(category_name):
        current_menu = menu_data[category_name]
        cols = st.columns(3)
        
        for i, (name, price) in enumerate(current_menu.items()):
            with cols[i % 3]: 
                st.markdown(f"### {name}")
                st.write(f"💰 {price:,}원")
                
                # [담기] 버튼 클릭 시 로직
                if st.button("담기", key=f"{category_name}_{name}"):
                    # 1. 장바구니에 이미 있는지 확인 (Flag 변수 사용)
                    found = False
                    for item in st.session_state['cart']:
                        if item['name'] == name:
                            item['quantity'] += 1 # 있으면 개수만 증가
                            found = True
                            break
                    
                    # 2. 없으면 새로 추가 (quantity: 1 로 시작)
                    if not found:
                        st.session_state['cart'].append({
                            "name": name, 
                            "price": price, 
                            "quantity": 1
                        })
                    
                    st.toast(f"✅ {name} 추가됨!")

    with tab1: show_menu_buttons("식사류")
    with tab2: show_menu_buttons("안주류")
    with tab3: show_menu_buttons("음료/주류")

# === [오른쪽 구역] 장바구니 & 영수증 ===
with col_cart:
    st.markdown("## 🛒 주문 내역")
    st.markdown("---")

    if len(st.session_state['cart']) == 0:
        st.info("메뉴를 담아주세요.")
    else:
        total_price = 0
        
        # 장바구니 출력 (여기도 변경되었습니다!)
        for index, item in enumerate(st.session_state['cart']):
            # 개별 합계 계산 (단가 x 수량)
            qty = item.get('quantity', 1) 
            sub_total = item['price'] * qty
            total_price += sub_total
            
            # 화면 표시: 이름 x 수량 (가격)
            st.write(f"{index+1}. **{item['name']}** x {item['quantity']}개")
            st.caption(f"└ {item['price']:,}원 x {item['quantity']} = {sub_total:,}원")
        
        st.markdown("---")
        st.metric(label="총 결제 금액", value=f"{total_price:,}원")
        
        # 버튼 영역
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💳 결제하기", type="primary"):
                st.balloons()
                st.success(f"{total_price:,}원 결제 완료!")
                st.session_state['cart'] = []
                st.rerun()
        with col_btn2:
            if st.button("🗑️ 전체 취소"):
                st.session_state['cart'] = []
                st.rerun()
