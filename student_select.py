import streamlit as st
import pandas as pd
import random
import time

# 구글 시트 ID 설정
SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
# csv 형태로 가져오는 URL 구성
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

st.title("🎰 강의실 학생 선발기")

def get_student_list():
    try:
        df = pd.read_csv(URL)
        # C열에 있는 '회원이름' 컬럼 사용
        return df['회원이름'].dropna().tolist()
    except Exception as e:
        st.error(f"데이터를 불러올 수 없습니다: {e}")
        return []

# 학생 명단 로드
if 'students' not in st.session_state:
    st.session_state.students = get_student_list()

if st.button("🔄 명단 새로고침"):
    st.session_state.students = get_student_list()
    st.success("최신 명단을 불러왔습니다!")

slot_area = st.empty()
slot_area.markdown(f"## 🏆 준비 완료! 버튼을 눌러주세요.")

if st.button("🎲 학생 뽑기 시작!", use_container_width=True):
    if st.session_state.students:
        # 슬롯머신 돌아가는 연출
        for i in range(20):
            pick = random.choice(st.session_state.students)
            slot_area.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>🌀 {pick}...</h1>", unsafe_allow_html=True)
            time.sleep(0.06)
        
        # 최종 당첨자
        winner = random.choice(st.session_state.students)
        slot_area.markdown(f"<h1 style='text-align: center; color: #00CC66;'>🎊 당첨자: {winner} !! 🎊</h1>", unsafe_allow_html=True)
        st.balloons()
    else:
        st.warning("선택할 학생이 없습니다.")