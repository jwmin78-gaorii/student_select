import streamlit as st
import pandas as pd
import random
import time

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
    
    # [1단계] 초고속 회전 (1초간)
    for _ in range(30):
        slot_placeholder.markdown(render_slots([random.choice(chars) for _ in range(3)], rolling_indices=[0,1,2]), unsafe_allow_html=True)
        time.sleep(0.02)
        
    # [2단계] 서서히 감속 (가속도 적용)
    # 점점 느려지는 속도 배열
    deceleration = [0.05, 0.08, 0.12, 0.18, 0.25]
    for d in deceleration:
        slot_placeholder.markdown(render_slots([random.choice(chars) for _ in range(3)], rolling_indices=[0,1,2]), unsafe_allow_html=True)
        time.sleep(d)

    # [3단계] 순차 정지 (멈칫+결정)
    current_display = ["?", "?", "?"]
    fixed_indices = []
    
    for i in range(3):
        idx = stop_order[i]
        
        # 멈추기 직전 멈칫 (한두번 살짝 굴러감)
        bounce_speeds = [0.3, 0.5] 
        for b in bounce_speeds:
            temp = current_display[:]
            temp[idx] = random.choice(chars)
            slot_placeholder.markdown(render_slots(temp, rolling_indices=[j for j in range(3) if j not in fixed_indices], fixed_indices=fixed_indices), unsafe_allow_html=True)
            time.sleep(b)
        
        # 글자 확정 (탁!)
        current_display[idx] = w_list[idx]
        fixed_indices.append(idx)
        slot_placeholder.markdown(render_slots(current_display, rolling_indices=[j for j in range(3) if j not in fixed_indices], fixed_indices=fixed_indices), unsafe_allow_html=True)
        
        if i < 2: time.sleep(0.5)

    st.balloons()
    st.success(f"🎊 당첨자: {winner} !! 🎊")