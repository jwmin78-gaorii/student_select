import streamlit as st
import pandas as pd
import random
import time
import math

SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

st.set_page_config(page_title="강의실 리얼 슬롯", layout="centered")

st.markdown("""
    <style>
    .header-box { text-align: center; color: #FFD700; margin-bottom: 20px; }
    .slot-container { display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; }
    .slot-box { background-color: #1a1a1a; border: 5px solid #FFD700; border-radius: 15px; 
                font-size: 60px; font-weight: bold; text-align: center; padding: 20px; 
                color: #FFFFFF; height: 150px; width: 120px; display: flex; 
                justify-content: center; align-items: center; box-shadow: 0 0 15px #333; overflow: hidden; }
    .slot-fixed { color: #FFD700 !important; border-color: #FF4500; background-color: #333; animation: popIn 0.3s ease; }
    .slot-rolling { animation: slideDown 0.05s linear infinite; }
    @keyframes slideDown { 0% { transform: translateY(-50%); opacity: 0; } 50% { transform: translateY(0%); opacity: 1; } 100% { transform: translateY(50%); opacity: 0; } }
    @keyframes popIn { 0% { transform: scale(0.9); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(CSV_URL)
        return [str(n) for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except: return []

if 'students' not in st.session_state: st.session_state.students = get_student_list()

st.markdown("<div class='header-box'><h1>🎰 강의실 행운의 슬롯</h1></div>", unsafe_allow_html=True)

def render_slots(display_list, rolling_indices=None, fixed_indices=None):
    rolling = rolling_indices if rolling_indices else []
    fixed = fixed_indices if fixed_indices else []
    html = '<div class="slot-container">'
    for i in range(3):
        cls = "slot-box"
        if i in fixed: cls += " slot-fixed"
        elif i in rolling: cls += " slot-rolling"
        html += f'<div class="{cls}">{display_list[i]}</div>'
    html += '</div>'
    return html

slot_placeholder = st.empty()
slot_placeholder.markdown(render_slots(["?", "?", "?"]), unsafe_allow_html=True)

chars = "김이박최정강조윤장임한오서신권황안송전홍박배백문허유남류심양"

if st.button("🎲 학생 뽑기 시작!"):
    winner = random.choice(st.session_state.students)
    w_list = list(winner)
    stop_order = random.sample([0, 1, 2], 3)
    
    # [가속도 곡선]
    # 총 40번 회전하며 속도를 0.02초에서 0.5초까지 서서히 늘림
    for i in range(40):
        # 사인 함수를 이용해 회전 속도가 서서히 줄어드는 곡선을 만듭니다.
        progress = i / 40
        delay = 0.02 + (progress ** 2) * 0.5 
        
        slot_placeholder.markdown(render_slots([random.choice(chars) for _ in range(3)], rolling_indices=[0,1,2]), unsafe_allow_html=True)
        time.sleep(delay)

    # [멈춤 단계]
    current_display = ["?", "?", "?"]
    fixed_indices = []
    
    for i in range(3):
        idx = stop_order[i]
        
        # 마지막 정지 시 덜컹거림
        temp = current_display[:]
        temp[idx] = w_list[idx]
        slot_placeholder.markdown(render_slots(temp, rolling_indices=[j for j in range(3) if j not in fixed_indices and j != idx], fixed_indices=fixed_indices), unsafe_allow_html=True)
        time.sleep(0.6) # 탁! 하고 멈추는 쾌감
        
        fixed_indices.append(idx)
        current_display[idx] = w_list[idx]
        
        if i < 2: time.sleep(0.4)

    st.balloons()
    st.success(f"🎊 당첨자: {winner} !! 🎊")