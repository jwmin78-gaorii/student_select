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
                justify-content: center; align-items: center; box-shadow: 0 0 15px #333; }
    .slot-fixed { color: #FFD700 !important; border-color: #FF4500; background-color: #333; }
    .footer-box { text-align: center; color: #888; font-size: 14px; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(CSV_URL)
        return [str(n) for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except: return []

if 'students' not in st.session_state: st.session_state.students = get_student_list()

# 화면 상단 고정 헤더
st.markdown("<div class='header-box'><h1>🎰 강의실 행운의 슬롯</h1></div>", unsafe_allow_html=True)

# 슬롯 영역 컨테이너 (여기는 항상 존재)
slot_placeholder = st.empty()

def render_slots(current_display, fixed_indices=None):
    fixed = fixed_indices if fixed_indices else []
    html = '<div class="slot-container">'
    for i in range(3):
        cls = "slot-box" + (" slot-fixed" if i in fixed else "")
        html += f'<div class="{cls}">{current_display[i]}</div>'
    html += '</div>'
    slot_placeholder.markdown(html, unsafe_allow_html=True)

# 초기화면
render_slots(["?", "?", "?"])

# 버튼 영역 (슬롯 아래 배치)
if st.button("🎲 학생 뽑기 시작!"):
    winner = random.choice(st.session_state.students)
    w_list = list(winner)
    stop_order = random.sample([0, 1, 2], 3)
    
    chars = "김이박최정강조윤장임한오서신권황안송전홍박배백문허유남류심양"
    
    # 1. 감속 회전 (전체 회전)
    for delay in [0.03, 0.05, 0.08, 0.12, 0.18]:
        render_slots([random.choice(chars) for _ in range(3)])
        time.sleep(delay)

    # 2. 순차 정지
    current_display = ["?", "?", "?"]
    fixed_indices = []
    for i in range(3):
        idx = stop_order[i]
        for d in [0.2, 0.3, 0.4, 0.5]:
            temp = current_display[:]
            temp[idx] = random.choice(chars)
            render_slots(temp, fixed_indices)
            time.sleep(d)
        
        current_display[idx] = w_list[idx]
        fixed_indices.append(idx)
        render_slots(current_display, fixed_indices)
        
        if i < 2: time.sleep(0.8)

    st.balloons()
    st.success(f"🎊 당첨자: {winner} !! 🎊")

# 하단 정보 항상 표시
st.markdown("<div class='footer-box'>오늘의 주인공은 누구일까요? 긴장하세요!</div>", unsafe_allow_html=True)