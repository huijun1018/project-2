import random
import matplotlib.pyplot as plt
import streamlit as st

def gambling_game(auto_mode=True, starting_money=30000, manual_bets=None):
    money = starting_money
    initial_success_rate = round(random.uniform(0.05, 0.10), 2)
    success_rate = initial_success_rate
    max_success_rate = 0.5
    success_increase = round(random.uniform(0.03, 0.05), 2)

    balance_history = [money]
    round_num = 1
    success_count = 0
    fail_count = 0

    st.write("### 🎯 도박 시뮬레이션 시작!")
    st.write(f"초기 자금: {money}원")
    st.write(f"초기 성공 확률: {success_rate*100}%")

    bet_index = 0

    while money > 0:
        st.write(f"#### 🎲 {round_num}번째 도박")
        st.write(f"현재 잔액: {money}원")
        st.write(f"현재 성공 확률: {round(success_rate*100, 2)}%")

        if auto_mode:
            bet = min(3000, money)
            st.write(f"자동 모드: {bet}원 베팅")
        else:
            if manual_bets and bet_index < len(manual_bets):
                bet = manual_bets[bet_index]
                bet_index += 1
                if bet > money:
                    st.write("❌ 베팅 금액이 보유 금액보다 많습니다. 건너뜁니다.")
                    round_num += 1
                    continue
            else:
                st.write("🛑 수동 입력이 부족하여 게임을 종료합니다.")
                break

        multiplier = max(1.2, round(2.0 - success_rate * 2, 2))
        outcome = random.random()

        if outcome < success_rate:
            gain = int(bet * multiplier)
            money += gain
            success_count += 1
            st.write(f"✅ 성공! {gain}원 획득! (배율: {multiplier})")
            success_rate = initial_success_rate
        else:
            money -= bet
            fail_count += 1
            st.write(f"❌ 실패... {bet}원 잃음.")
            success_rate = min(success_rate + success_increase, max_success_rate)

        balance_history.append(money)
        round_num += 1
        st.write("---")

    st.success("게임 종료!")
    st.write(f"최종 잔액: {money}원")
    st.write(f"총 도박 횟수: {round_num - 1}회")
    st.write(f"성공 횟수: {success_count}회")
    st.write(f"실패 횟수: {fail_count}회")

    # 잔액 변화 그래프
    st.write("### 📈 잔액 변화 그래프")
    fig1, ax1 = plt.subplots()
    ax1.plot(balance_history, marker='o')
    ax1.set_title('잔액 변화 그래프')
    ax1.set_xlabel('도박 횟수')
    ax1.set_ylabel('잔액 (원)')
    ax1.grid(True)
    st.pyplot(fig1)

    # 파이차트
    st.write("### 🥧 성공 vs 실패 비율")
    fig2, ax2 = plt.subplots()
    ax2.pie([success_count, fail_count], labels=['성공', '실패'], autopct='%1.1f%%', startangle=90)
    ax2.set_title('성공 vs 실패 비율')
    st.pyplot(fig2)

# Streamlit UI
st.title("🎰 도박 시뮬레이션 게임")
starting_money = st.slider("💰 시작 자금 설정", 30000, 50000, 30000, step=1000)

mode = st.radio("🎮 게임 모드 선택", ["자동 모드", "수동 모드"])

if mode == "수동 모드":
    manual_bet_input = st.text_input("💸 수동 베팅 금액들 (쉼표로 구분해서 입력, 예: 3000,2500,4000)")
    if manual_bet_input:
        try:
            manual_bets = [int(x.strip()) for x in manual_bet_input.split(',') if x.strip().isdigit()]
        except:
            st.warning("❌ 입력 형식이 올바르지 않습니다.")
        if st.button("게임 시작"):
            gambling_game(auto_mode=False, starting_money=starting_money, manual_bets=manual_bets)
else:
    if st.button("게임 시작"):
        gambling_game(auto_mode=True, starting_money=starting_money)
