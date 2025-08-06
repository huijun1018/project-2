import random
import matplotlib.pyplot as plt
import streamlit as st

def gambling_game(auto_mode=True, starting_money=30000):
    money = starting_money
    initial_success_rate = round(random.uniform(0.05, 0.10), 2)
    success_rate = initial_success_rate
    max_success_rate = 0.5
    success_increase = round(random.uniform(0.03, 0.05), 2)

    balance_history = [money]
    round_num = 1
    success_count = 0
    fail_count = 0

    st.markdown("## 🎯 도박 시뮬레이션 시작!")
    st.write(f"초기 자금: {money}원")
    st.write(f"초기 성공 확률: {success_rate * 100}%")

    while money > 0:
        st.write(f"### 🎲 {round_num}번째 도박")
        st.write(f"현재 잔액: {money}원")
        st.write(f"현재 성공 확률: {round(success_rate * 100, 2)}%")

        if auto_mode:
            bet = min(3000, money)
            st.write(f"자동 모드: {bet}원 베팅")
        else:
            bet = min(money, 3000)  # 수동 모드라도 streamlit에서는 자동 설정 (수동 구현 복잡함)

        multiplier = max(1.2, round(2.0 - success_rate * 2, 2))
        outcome = random.random()

        if outcome < success_rate:
            gain = int(bet * multiplier)
            money += gain
            success_count += 1
            st.success(f"✅ 성공! {gain}원 획득! (배율: {multiplier})")
            success_rate = initial_success_rate
        else:
            money -= bet
            fail_count += 1
            st.error(f"❌ 실패... {bet}원 잃음.")
            success_rate = min(success_rate + success_increase, max_success_rate)

        balance_history.append(money)
        round_num += 1

        if auto_mode and round_num > 100:
            st.warning("100회를 초과하여 자동 모드 종료합니다.")
            break

    st.markdown("## 🎉 게임 종료!")
    st.write(f"최종 잔액: {money}원")
    st.write(f"총 도박 횟수: {round_num - 1}회")
    st.write(f"성공 횟수: {success_count}회")
    st.write(f"실패 횟수: {fail_count}회")

    # 잔액 변화 그래프
    st.subheader("📈 잔액 변화 그래프")
    fig1, ax1 = plt.subplots()
    ax1.plot(balance_history, marker='o')
    ax1.set_title("Balance Change Graph")
    ax1.set_xlabel("the number of gambling")
    ax1.set_ylabel("Balance (KRW)")
    ax1.grid(True)
    st.pyplot(fig1)

    # 성공/실패 비율 파이차트
    st.subheader("🥧 성공 vs 실패 비율")
    fig2, ax2 = plt.subplots()
    ax2.pie([success_count, fail_count], labels=['success', 'fail'], autopct='%1.1f%%', startangle=90)
    ax2.set_title("success vs fail percentage")
    st.pyplot(fig2)

# Streamlit UI
st.title("💸 도박 시뮬레이션 게임")

starting_money = st.slider("🎯 시작 자금 설정 (30,000 ~ 50,000원)", min_value=30000, max_value=50000, step=1000)

mode = st.radio("게임 모드 선택", ["자동 모드 (3,000원 고정 베팅)", "수동 모드 (현재는 자동과 동일하게 처리됨)"])

if st.button("게임 시작"):
    auto_mode = True if mode == "자동 모드 (3,000원 고정 베팅)" else False
    gambling_game(auto_mode=auto_mode, starting_money=starting_money)
