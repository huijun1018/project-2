import streamlit as st
import random
import matplotlib.pyplot as plt

# 상태 저장
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.money = 0
    st.session_state.success_rate = 0.0
    st.session_state.initial_success_rate = 0.0
    st.session_state.success_increase = 0.0
    st.session_state.max_success_rate = 0.5
    st.session_state.balance_history = []
    st.session_state.round_num = 1
    st.session_state.success_count = 0
    st.session_state.fail_count = 0
    st.session_state.mode = 'auto'
    st.session_state.game_over = False

def reset_game(starting_money, mode):
    st.session_state.money = starting_money
    st.session_state.initial_success_rate = round(random.uniform(0.05, 0.10), 2)
    st.session_state.success_rate = st.session_state.initial_success_rate
    st.session_state.success_increase = round(random.uniform(0.03, 0.05), 2)
    st.session_state.balance_history = [starting_money]
    st.session_state.round_num = 1
    st.session_state.success_count = 0
    st.session_state.fail_count = 0
    st.session_state.mode = mode
    st.session_state.game_over = False
    st.session_state.initialized = True

# 게임 초기 설정
st.title("💰 도박 시뮬레이션 게임 (Streamlit 버전)")

if not st.session_state.initialized:
    starting_money = st.number_input("시작 자금을 입력하세요 (30,000 ~ 50,000원)", min_value=30000, max_value=50000, step=1000)
    mode = st.radio("게임 모드 선택", ["자동", "수동"])

    if st.button("게임 시작"):
        reset_game(starting_money, "auto" if mode == "자동" else "manual")
        st.experimental_rerun()

# 게임 진행
if st.session_state.initialized and not st.session_state.game_over:
    st.subheader(f"🎲 {st.session_state.round_num}번째 도박")
    st.write(f"현재 잔액: {st.session_state.money}원")
    st.write(f"현재 성공 확률: {round(st.session_state.success_rate * 100, 2)}%")

    bet = 0
    if st.session_state.mode == "auto":
        bet = min(3000, st.session_state.money)
        if st.button("도박 진행 (자동 모드)"):
            pass  # 진행은 아래 로직에서 수행됨
        else:
            st.stop()
    else:
        bet = st.number_input("베팅 금액 입력 (0 입력 시 종료)", min_value=0, max_value=st.session_state.money, step=1000)
        if bet == 0:
            st.session_state.game_over = True
            st.success("게임을 종료합니다.")
            st.stop()
        if st.button("도박 진행 (수동 모드)"):
            pass
        else:
            st.stop()

    # 게임 로직
    multiplier = max(1.2, round(2.0 - st.session_state.success_rate * 2, 2))
    outcome = random.random()

    if outcome < st.session_state.success_rate:
        gain = int(bet * multiplier)
        st.session_state.money += gain
        st.session_state.success_count += 1
        st.success(f"✅ 성공! {gain}원 획득! (배율: {multiplier})")
        st.session_state.success_rate = st.session_state.initial_success_rate
    else:
        st.session_state.money -= bet
        st.session_state.fail_count += 1
        st.error(f"❌ 실패... {bet}원 잃음.")
        st.session_state.success_rate = min(
            st.session_state.success_rate + st.session_state.success_increase,
            st.session_state.max_success_rate
        )

    st.session_state.balance_history.append(st.session_state.money)
    st.session_state.round_num += 1

    if st.session_state.money <= 0:
        st.session_state.game_over = True
        st.warning("💸 자금이 모두 소진되었습니다. 게임 종료!")

# 게임 종료 시 결과 출력
if st.session_state.game_over:
    st.header("🎉 게임 종료!")
    st.write(f"최종 잔액: {st.session_state.money}원")
    st.write(f"총 도박 횟수: {st.session_state.round_num - 1}회")
    st.write(f"성공 횟수: {st.session_state.success_count}회")
    st.write(f"실패 횟수: {st.session_state.fail_count}회")

    # 잔액 변화 그래프
    fig, ax = plt.subplots()
    ax.plot(st.session_state.balance_history, marker='o')
    ax.set_title("잔액 변화 그래프")
    ax.set_xlabel("도박 횟수")
    ax.set_ylabel("잔액 (원)")
    st.pyplot(fig)

    # 성공/실패 비율 파이차트
    fig2, ax2 = plt.subplots()
    ax2.pie([st.session_state.success_count, st.session_state.fail_count],
            labels=['성공', '실패'],
            autopct='%1.1f%%', startangle=90)
    ax2.set_title("성공 vs 실패 비율")
    st.pyplot(fig2)

    if st.button("다시 시작"):
        st.session_state.initialized = False
        st.experimental_rerun()
