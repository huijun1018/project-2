# streamlit_app.py
import streamlit as st
import random
import matplotlib.pyplot as plt

def gambling_game(auto_mode=True):
    # 세션 상태 초기화
    if 'money' not in st.session_state:
        st.session_state.money = 30000
        st.session_state.success_rate = round(random.uniform(0.05, 0.10), 2)
        st.session_state.initial_success_rate = st.session_state.success_rate
        st.session_state.success_increase = round(random.uniform(0.03, 0.05), 2)
        st.session_state.max_success_rate = 0.5
        st.session_state.round_num = 1
        st.session_state.balance_history = [st.session_state.money]
        st.session_state.success_count = 0
        st.session_state.fail_count = 0
        st.session_state.game_over = False

    st.write(f"🎯 도박 시뮬레이션")
    st.write(f"초기 자금: 30000원")
    st.write(f"초기 성공 확률: {round(st.session_state.initial_success_rate * 100, 2)}%")

    if st.session_state.money <= 0:
        st.session_state.game_over = True

    if not st.session_state.game_over:
        st.write(f"🎲 {st.session_state.round_num}번째 도박")
        st.write(f"현재 잔액: {st.session_state.money}원")
        st.write(f"현재 성공 확률: {round(st.session_state.success_rate * 100, 2)}%")

        if auto_mode:
            bet = min(3000, st.session_state.money)
            st.write(f"자동 모드: {bet}원 베팅")
        else:
            bet = st.number_input("베팅할 금액을 입력하세요", min_value=1, max_value=st.session_state.money, step=100, key=f"bet_input_{st.session_state.round_num}")

        if st.button("도박 시작" if auto_mode else "도박하기", key=f"button_{st.session_state.round_num}"):
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

    else:
        st.header("🎉 게임 종료!")
        st.write(f"최종 잔액: {st.session_state.money}원")
        st.write(f"총 도박 횟수: {st.session_state.round_num - 1}회")
        st.write(f"성공 횟수: {st.session_state.success_count}회")
        st.write(f"실패 횟수: {st.session_state.fail_count}회")

        # 그래프: 잔액 변화
        fig1, ax1 = plt.subplots()
        ax1.plot(st.session_state.balance_history, marker='o')
        ax1.set_title('Balance Change Graph')
        ax1.set_xlabel('number of gambling')
        ax1.set_ylabel('Balance (KRW)')
        ax1.grid(True)
        st.pyplot(fig1)

        # 그래프: 성공/실패 비율
        fig2, ax2 = plt.subplots()
        ax2.pie([st.session_state.success_count, st.session_state.fail_count],
                labels=['success', 'fail'],
                autopct='%1.1f%%',
                startangle=90)
        ax2.set_title('success vs fail proportion')
        st.pyplot(fig2)

        # 초기화 버튼
        if st.button("다시 시작하기"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()


# Streamlit 앱 시작점
st.title("💸 도박 시뮬레이션 게임")

mode = st.radio("모드를 선택하세요", options=["자동 모드", "수동 모드"])
gambling_game(auto_mode=(mode == "자동 모드"))
