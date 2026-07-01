import streamlit as st
import pandas as pd
import random
import time

# 구글 시트 설정
SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
URL = f"https://spreadsheets.google.com/feeds/cells/{SHEET_ID}/1/public/full?alt=json"
# URL을 CSV 호출 방식으로 변경하여 더 안정적으로 작동하도록 수정
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

st.set_page_config(page_title="강의실 슬롯머신", layout="centered")

st.markdown("""
    <style>
    .slot-box { 
        background-color: #262730; border: 5px solid #FFD700; border-radius: 15px; 
        font-size: 50px; font-weight: bold; text-align: center; padding: 20px; 
        margin: 5px; color: #FFFFFF; height: 120px; display: flex; 
        justify-content: center; align-items: center; 
    }
    .slot-fixed { color: #FFD700 !important; border-color: #FF4500; }
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(CSV_URL)
        return [str(n) for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except:
        return []

if 'students' not in st.session_state:
    st.session_state.students = get_student_list()

st.title("🎰 두근두근 슬롯머신")

c1, c2, c3 = st.columns(3)
slots = [c1.empty(), c2.empty(), c3.empty()]

for s in slots:
    s.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)

if st.button("🎲 학생 뽑기 시작!"):
    if st.session_state.students:
        winner = random.choice(st.session_state.students)
        w_list = list(winner)
        
        # 전체가 격렬하게 돌아가는 시간 (약 1초)
        start_time = time.time()
        while time.time() - start_time < 1.0:
            for s in slots:
                s.markdown(f'<div class="slot-box">{random.choice("가나다라마바사아자차")}</div>', unsafe_allow_html=True)
            time.sleep(0.05)
            
        # 순차적으로 하나씩 정지
        for i in range(3):
            # i번째 정지 (결과 확정)
            slots[i].markdown(f'<div class="slot-box slot-fixed">{w_list[i]}</div>', unsafe_allow_html=True)
            
            # 다음 정지 전까지 나머지 칸들은 계속 돌기
            if i < 2:
                for _ in range(10): # 0.5초 동안 나머지 칸들 회전
                    for j in range(i + 1, 3):
                        slots[j].markdown(f'<div class="slot-box">{random.choice("가나다라마바사아자차")}</div>', unsafe_allow_html=True)
                    time.sleep(0.05)
        
        st.success(f"🎊 당첨자: {winner} !! 🎊")
        st.balloons()
    else:
        st.error("명단이 비어있습니다.")