import streamlit as st
import pandas as pd
import random
import time

SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

st.set_page_config(page_title="강의실 리얼 슬롯", layout="centered")

st.markdown("""
    <style>
    .slot-container { display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; }
    .slot-box { background-color: #1a1a1a; border: 5px solid #FFD700; border-radius: 15px; 
                font-size: 60px; font-weight: bold; text-align: center; padding: 20px; 
                color: #FFFFFF; height: 150px; width: 120px; display: flex; 
                justify-content: center; align-items: center; box-shadow: 0 0 15px #333; overflow: hidden; }
    .slot-fixed { color: #FFD700 !important; border-color: #FF4500; background-color: #333; }
    .slot-rolling { animation: slideDown 0.05s linear infinite; }
    @keyframes slideDown { 0% { transform: translateY(-50%); opacity: 0; } 50% { transform: translateY(0%); opacity: 1; } 100% { transform: translateY(50%); opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(CSV_URL)
        return [str(n) for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except: return []

if 'students' not in st.session_state: st.session_state.students = get_student_list()

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎰 강의실 행운의 슬롯</h1>", unsafe_allow_html=True)
slot_placeholder = st.empty()

def render_slots(current_display, rolling_indices=None, fixed_indices=None):
    rolling = rolling_indices if rolling_indices else []
    fixed = fixed_indices if fixed_indices else []
    html = '<div class="slot-container">'
    for i in range(3):
        cls = "slot-box"
        if i in fixed: cls += " slot-fixed"
        elif i in rolling: cls += " slot-rolling"
        html += f'<div class="{cls}">{current_display[i]}</div>'
    html += '</div>'
    slot_placeholder.markdown(html, unsafe_allow_html=True)

render_slots(["?", "?", "?"], rolling_indices=[])
chars = "김이박최정강조윤장임한오서신권황안송전홍박배백문허유남류심양"

if st.button("🎲 학생 뽑기 시작!"):
    winner = random.choice(st.session_state.students)
    w_list = list(winner)
    stop_order = random.sample([0, 1, 2], 3)
    
    # [1단계] 감속 구간 (80단계, 속도가 점진적으로 느려짐)
    for i in range(80):
        delay = 0.02 + (i / 80) ** 2 * 0.4
        render_slots([random.choice(chars) for _ in range(3)], rolling_indices=[0,1,2])
        time.sleep(delay)

    # [2단계] 하나씩 멈춤 (개별 쫄깃한 시간 1.5초)
    current_display = ["?", "?", "?"]
    fixed_indices = []
    
    for i in range(3):
        idx = stop_order[i]
        
        # 글자 확정 및 고정
        current_display[idx] = w_list[idx]
        fixed_indices.append(idx)
        
        # 다음 글자 멈추기 전까지 나머지 칸들은 애니메이션 유지
        start_wait = time.time()
        while time.time() - start_wait < 1.5:
            temp = current_display[:]
            for j in range(3):
                if j not in fixed_indices:
                    temp[j] = random.choice(chars)
            render_slots(temp, rolling_indices=[j for j in range(3) if j not in fixed_indices], fixed_indices=fixed_indices)
            time.sleep(0.08)

    st.balloons()
    st.success(f"🎊 당첨자: {winner} !! 🎊")