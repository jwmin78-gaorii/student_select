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
    
    # [1단계] 감속 구간 (30번 반복하면서 속도가 서서히 줄어듦)
    for i in range(30):
        # 뒤의 1.5를 조절하면 멈추기 전 감속 체감이 더 커집니다.
        delay = 0.02 + (i / 30) ** 2 * 1.5 
        slot_placeholder.markdown(render_slots([random.choice(chars) for _ in range(3)], rolling_indices=[0,1,2]), unsafe_allow_html=True)
        time.sleep(delay)

    # [2단계] 하나씩 멈춤 (오버슈팅 + 최종 확정)
    current_display = ["?", "?", "?"]
    fixed_indices = []
    
    for i in range(3):
        idx = stop_order[i]
        
        # 멈추기 직전 낚시질 (0.3초간 랜덤 글자 노출)
        temp_fishing = current_display[:]
        temp_fishing[idx] = random.choice(chars)
        rolling_others = [j for j in range(3) if j not in fixed_indices and j != idx]
        slot_placeholder.markdown(render_slots(temp_fishing, rolling_indices=rolling_others + [idx], fixed_indices=fixed_indices), unsafe_allow_html=True)
        time.sleep(0.3)
        
        # 확정 (탁!)
        current_display[idx] = w_list[idx]
        fixed_indices.append(idx)
        slot_placeholder.markdown(render_slots(current_display, rolling_indices=rolling_others, fixed_indices=fixed_indices), unsafe_allow_html=True)
        
        if i < 2: time.sleep(0.6) # 다음 글자 넘어가기 전 대기

    st.balloons()
    st.success(f"🎊 당첨자: {winner} !! 🎊")