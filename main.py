import random
import matplotlib.pyplot as plt
import streamlit as st

# 세션 상태 초기화
if "money" not in st.session_state:
    st.session_state.money = 30000
    st.session_state.success_rate = round(random.uniform(0.05, 0.10), 2)
    st.session_state.initial_success_rate = st.session_state.success_rate
    st.session_state.success_increase = round(random.uniform(0.03, 0.05), 2)
    st.session_state.success_count = 0
    st.session_state.fail_count = 0
    st.session_state.balance_history = [st.session_state.money]
    st.session_state.round_num = 1
    st.session_state.auto_mode = False
    st.session_state.game_over = False

def reset_game(starting_money, auto_mode):
    st.session_state.money = starting_money
    st.session_state.success_rate = round(random.uniform(0.05, 0.10), 2)
    st.session_state.initial_success_rate = st.session_state.success_rate
    st.session_state.success_increase = round(random.uniform(0.03, 0.05), 2)
    st.session_state.success_count = 0
    st.session_state.fail_count = 0
    st.session_state.balance_history = [starting_money]
    st.session_state.round_num = 1
    st.session_state.auto_mode = auto_mode
    st.session_state.game_over = False

# 게임 제목 및 모드 선택
st.title("🎰 도박 시뮬레이터")

starting_money = st.slider("💰 시작 자금 설정", 30000, 50000, 30000, step=1000)
mode = st.radio("🎮 게임 모드 선택", ["자동 모드", "수동 모드"])

if st.button("🔄 게임 초기화"):
    reset_game(starting_money, auto_mode=(mode == "자동 모드"))

if st.session_state.money <= 0:
    st.session_state.game_over = True
    st.warning("💸 자금이 모두 소진되었습니다. 게임을 초기화해주세요.")

# 수동 모드
if not st.session_state.auto_mode and not st.session_state.game_over:
    st.write(f"### 🎲 {st.session_state.round_num}번째 도박")
    st.write(f"현재 잔액: {st.session_state.money}원")
    st.write(f"현재 성공 확률: {round(st.session_state.success_rate*100, 2)}%")
    st.write(f"성공: {st.session_state.success_count}회, 실패: {st.session_state.fail_count}회")

    bet = st.number_input("💸 베팅 금액을 입력하세요", min_value=1, max_value=st.session_state.money, step=1000)

    if st.button("🎯 도박 시작!"):
        multiplier = max(1.2, round(2.0 - st.session_state.success_rate * 2, 2))
        outcome = random.random()

        if outcome < st.session_state.success_rate:
            gain = int(bet * multiplier)
            st.session_state.money += gain
            st.session_state.success_count += 1
            st.session_state.success_rate = st.session_state.initial_success_rate
            st.success(f"✅ 성공! {gain}원 획득! (배율: {multiplier})")
        else:
            st.session_state.money -= bet
            st.session_state.fail_count += 1
            st.session_state.success_rate = min(
                st.session_state.success_rate + st.session_state.success_increase, 0.5
            )
            st.error(f"❌ 실패... {bet}원 잃음.")

        st.session_state.balance_history.append(st.session_state.money)
        st.session_state.round_num += 1

# 자동 모드
elif st.session_state.auto_mode and not st.session_state.game_over:
    st.write("### 🤖 자동 도박 시작!")
    while st.session_state.money > 0:
        bet = min(3000, st.session_state.money)
        multiplier = max(1.2, round(2.0 - st.session_state.success_rate * 2, 2))
        outcome = random.random()

        if outcome < st.session_state.success_rate:
            gain = int(bet * multiplier)
            st.session_state.money += gain
            st.session_state.success_count += 1
            st.session_state.success_rate = st.session_state.initial_success_rate
        else:
            st.session_state.money -= bet
            st.session_state.fail_count += 1
            st.session_state.success_rate = min(
                st.session_state.success_rate + st.session_state.success_increase, 0.5
            )

        st.session_state.balance_history.append(st.session_state.money)
        st.session_state.round_num += 1

    st.session_state.game_over = True
    st.success("✅ 자동 도박 종료!")

# 그래프
if st.session_state.round_num > 1:
    st.write("### 📈 잔액 변화 그래프")
    fig1, ax1 = plt.subplots()
    ax1.plot(st.session_state.balance_history, marker='o')
    ax1.set_title('잔액 변화')
    ax1.set_xlabel('도박 횟수')
    ax1.set_ylabel('잔액 (원)')
    ax1.grid(True)
    st.pyplot(fig1)

    st.write("### 🥧 성공 vs 실패 비율")
    fig2, ax2 = plt.subplots()
    ax2.pie(
        [st.session_state.success_count, st.session_state.fail_count],
        labels=['성공', '실패'],
        autopct='%1.1f%%',
        startangle=90
    )
    ax2.set_title('도박 성공률')
    st.pyplot(fig2)
