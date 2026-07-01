import streamlit as st
import pandas as pd
import random
import time

SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

st.set_page_config(page_title="강의실 슬롯머신", layout="centered")

st.markdown("""
    <style>
    .slot-box { background-color: #262730; border: 5px solid #FFD700; border-radius: 15px; 
                font-size: 50px; font-weight: bold; text-align: center; padding: 20px; 
                margin: 5px; color: #FFFFFF; height: 120px; display: flex; 
                justify-content: center; align-items: center; }
    .slot-fixed { color: #FFD700 !important; border-color: #FF4500; transform: scale(1.05); transition: 0.3s; }
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(CSV_URL)
        return [str(n) for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except: return []

if 'students' not in st.session_state: st.session_state.students = get_student_list()

st.title("🎰 두근두근 극적 슬롯머신")

c1, c2, c3 = st.columns(3)
slots = [c1.empty(), c2.empty(), c3.empty()]
for s in slots: s.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)

if st.button("🎲 학생 뽑기 시작!"):
    if st.session_state.students:
        winner = random.choice(st.session_state.students)
        w_list = list(winner)
        # 랜덤 멈춤 순서 결정 (예: [2, 0, 1])
        stop_order = random.sample([0, 1, 2], 3)
        
        # 1. 초반 전체 회전
        for _ in range(15):
            for s in slots:
                s.markdown(f'<div class="slot-box">{random.choice("가나다라마바사아자차")}</div>', unsafe_allow_html=True)
            time.sleep(0.06)

        # 2. 순서대로 하나씩 멈춤
        for i in range(3):
            target_idx = stop_order[i]
            
            # 극적 연출: 멈추기 직전 3번 정도 헛도는 듯한 효과
            for _ in range(3):
                slots[target_idx].markdown(f'<div class="slot-box">{random.choice("가나다라마바사아자차")}</div>', unsafe_allow_html=True)
                time.sleep(0.15)
            
            # 확정
            slots[target_idx].markdown(f'<div class="slot-box slot-fixed">{w_list[target_idx]}</div>', unsafe_allow_html=True)
            
            # 나머지 계속 돌아가는 연출
            if i < 2:
                time.sleep(1.0) # 멈춘 뒤 대기시간
                # 나머지 자리들 계속 회전
                for _ in range(10):
                    for j in range(3):
                        if j not in stop_order[:i+1]:
                            slots[j].markdown(f'<div class="slot-box">{random.choice("가나다라마바사아자차")}</div>', unsafe_allow_html=True)
                    time.sleep(0.05)
        
        st.success(f"🎊 오늘의 주인공: {winner} 🎊")
        st.balloons()
    else: st.error("명단이 비어있습니다.")