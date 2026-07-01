import streamlit as st
import pandas as pd
import random
import time

SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

st.set_page_config(page_title="강의실 리얼 슬롯", layout="centered")

# 핵심: CSS 애니메이션 정의 (위에서 아래로 흐르는 효과)
st.markdown("""
    <style>
    /* 슬롯머신 전체 컨테이너 스타일 */
    .slot-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 30px;
    }

    /* 각 슬롯 박스 기본 스타일 */
    .slot-box {
        background-color: #1a1a1a;
        border: 5px solid #FFD700;
        border-radius: 15px;
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        color: #FFFFFF;
        height: 150px;
        width: 120px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: inset 0 0 20px #000;
        overflow: hidden; /* 애니메이션이 박스 밖으로 안나가게 */
        position: relative;
    }

    /* 확정된 글자 스타일 (황금색 + 약간 확대) */
    .slot-fixed {
        color: #FFD700 !important;
        border-color: #FF4500;
        background-color: #333;
        animation: popIn 0.3s ease; /* 멈출 때 톡 튀어나오는 효과 */
    }
    
    /* 돌아가는 중인 글자 스타일 (약간 흐릿하게) */
    .slot-rolling {
        animation: slideDown 0.05s linear infinite; /* 위에서 아래로 흐르는 애니메이션 */
    }

    /* 위에서 아래로 흐르는 키프레임 정의 */
    @keyframes slideDown {
        0% { transform: translateY(-100%); opacity: 0; }
        50% { transform: translateY(0%); opacity: 1; }
        100% { transform: translateY(100%); opacity: 0; }
    }
    
    /* 멈출 때 톡 튀는 효과 */
    @keyframes popIn {
        0% { transform: scale(0.8); }
        70% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }

    /* 버튼 스타일 */
    .stButton>button {
        background-color: #FFD700; color: #1a1a1a; font-size: 20px; font-weight: bold;
        border: none; border-radius: 10px; padding: 15px 32px;
        width: 100%; box-shadow: 0 4px #b89a00;
    }
    .stButton>button:active { box-shadow: 0 2px #b89a00; transform: translateY(2px); }
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(CSV_URL)
        return [str(n) for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except: return []

if 'students' not in st.session_state: st.session_state.students = get_student_list()
if 'winner_display' not in st.session_state: st.session_state.winner_display = ["?", "?", "?"]

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎰 두근두근 리얼 롤링 슬롯</h1>", unsafe_allow_html=True)

# 슬롯 영역을 HTML div로 구성
slot_container = st.empty()

def render_slots(current_display, rolling_indices=None, fixed_indices=None):
    if rolling_indices is None: rolling_indices = []
    if fixed_indices is None: fixed_indices = []
    
    html_content = '<div class="slot-container">'
    for i in range(3):
        char = current_display[i]
        cls = "slot-box"
        if i in fixed_indices:
            cls += " slot-fixed"
        elif i in rolling_indices:
            cls += " slot-rolling"
        
        # 각 칸의 HTML 구성
        html_content += f'<div class="{cls}">{char}</div>'
    html_content += '</div>'
    slot_container.markdown(html_content, unsafe_allow_html=True)

# 초기 화면 렌더링
render_slots(st.session_state.winner_display)

chars = "김이박최정강조윤장임한오서신권황안송전홍박배백문허유남류심양" # 이름용 글자풀

if st.button("🎲 학생 뽑기 시작!"):
    if st.session_state.students:
        winner = random.choice(st.session_state.students)
        w_list = list(winner)
        stop_order = random.sample([0, 1, 2], 3)
        
        # 1. 초반 전체 회전 (속도감 극대화)
        start_time = time.time()
        while time.time() - start_time < 1.5:
            render_slots([random.choice(chars) for _ in range(3)], rolling_indices=[0,1,2])
            time.sleep(0.01) # 이 값을 줄일수록 더 빨라집니다

        # 2. 하나씩 순차적으로 멈춤
        current_display = ["?", "?", "?"]
        fixed_indices = []
        
        for i in range(3):
            target_idx = stop_order[i]
            rolling_others = [idx for idx in range(3) if idx not in fixed_indices and idx != target_idx]
            
            # 멈추기 전 '드르륵' 하는 오버슈팅 (3번 굴림)
            for _ in range(5):
                temp_display = current_display[:]
                temp_display[target_idx] = random.choice(chars)
                render_slots(temp_display, rolling_indices=[target_idx] + rolling_others, fixed_indices=fixed_indices)
                time.sleep(0.06)
            
            # 확정
            current_display[target_idx] = w_list[target_idx]
            fixed_indices.append(target_idx)
            render_slots(current_display, rolling_indices=rolling_others, fixed_indices=fixed_indices)
            
            # 멈춘 뒤 대기시간 (긴장감 조성)
            if i < 2:
                time.sleep(0.8)
        
        st.balloons()
        st.markdown(f"<h2 style='text-align: center; color: #00CC66;'>🎊 당첨자: {winner} !! 🎊</h2>", unsafe_allow_html=True)
    else: st.error("명단이 비어있습니다.")