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
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(CSV_URL)
        return [str(n) for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except: return []

if 'students' not in st.session_state: st.session_state.students = get_student_list()

st.markdown("<div class='header-box'><h1>🎰 강의실 행운의 슬롯</h1></div>", unsafe_allow_html=True)

def render_slots(display_list, fixed_indices=None):
    fixed = fixed_indices if fixed_indices else []
    html = '<div class="slot-container">'
    for i in range(3):
        cls = "slot-box" + (" slot-fixed" if i in fixed else "")
        html += f'<div class="{cls}">{display_list[i]}</div>'
    html += '</div>'
    slot_placeholder.markdown(html, unsafe_allow_html=True)

slot_placeholder = st.empty()
slot_placeholder.markdown(render_slots(["?", "?", "?"]), unsafe_allow_html=True)

chars = "김이박최정강조윤장임한오서신권황안송전홍박배백문허유남류심양"

if st.button("🎲 학생 뽑기 시작!"):
    winner = random.choice(st.session_state.students)
    w_list = list(winner)
    stop_order = random.sample([0, 1, 2], 3)
    
    # 1. 속도가 점점 줄어드는 물리적 감속 (80단계로 대폭 확장)
    for i in range(80):
        # 0.02초에서 시작해 0.4초까지 서서히 느려지는 곡선
        delay = 0.02 + (i / 80) ** 2 * 0.4
        render_slots([random.choice(chars) for _ in range(3)])
        time.sleep(delay)

    # 2. 하나씩 멈추며 긴장감 조성 (개별 글자 확인 시간 1.5초씩)
    current_display = ["?", "?", "?"]
    fixed_indices = []
    
    for i in range(3):
        idx = stop_order[i]
        
        # 멈추기 전 살짝 뜸들이기
        time.sleep(0.5) 
        
        # 글자 확정 (탁!)
        current_display[idx] = w_list[idx]
        fixed_indices.append(idx)
        render_slots(current_display, fixed_indices)
        
        # [긴장감 포인트] 글자 하나가 확정되면 나머지 글자들은 계속 돌아감
        # 멈춘 글자를 본 후 다음 글자가 멈추기까지 1.5초간 쫄깃한 시간
        if i < 2:
            start_wait = time.time()
            while time.time() - start_wait < 1.5:
                temp = current_display[:]
                for j in range(3):
                    if j not in fixed_indices:
                        temp[j] = random.choice(chars)
                render_slots(temp, fixed_indices)
                time.sleep(0.08)

    st.balloons()
    st.success(f"🎊 당첨자: {winner} !! 🎊")