import streamlit as st
import pandas as pd
import random
import time

# 구글 시트 설정 (사용자님의 정보 그대로 사용)
SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

st.set_page_config(page_title="학생 선발 슬롯머신", layout="centered")

# CSS로 슬롯 스타일 꾸미기 (더 게임기처럼 보이게)
st.markdown("""
    <style>
    .slot-box {
        background-color: #f0f2f6;
        border: 5px solid #333;
        border-radius: 15px;
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        margin: 10px;
        color: #005088;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .win-text {
        text-align: center;
        font-size: 80px;
        color: #00CC66;
        margin-top: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

def get_student_list():
    try:
        df = pd.read_csv(URL)
        names = df['회원이름'].dropna().tolist()
        # 이름이 3글자인 경우만 필터링 (슬롯이 3개이므로)
        return [name for name in names if len(name) == 3]
    except:
        return ["시트확인"]

st.title("🎰 강의실 학생 선발기 - 두근두근 슬롯")
st.write("구글 시트 명단 중 세 글자 이름 학생을 추첨합니다.")

if 'students' not in st.session_state:
    st.session_state.students = get_student_list()
if 'last_winner' not in st.session_state:
    st.session_state.last_winner = "???"

# 화면 연출 영역
c1, c2, c3 = st.columns(3)
slot1 = c1.empty()
slot2 = c2.empty()
slot3 = c3.empty()

# 초기 화면
slot1.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)
slot2.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)
slot3.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)

if st.button("🔄 명단 새로고침"):
    st.session_state.students = get_student_list()
    st.success(f"3글자 명단 {len(st.session_state.students)}명을 불러왔습니다!")

st.write("---")
if st.button("🎲 두근두근 학생 뽑기 시작!", use_container_width=True):
    if len(st.session_state.students) >= 1:
        # 최종 당첨자 선정
        winner = random.choice(st.session_state.students)
        w1, w2, w3 = list(winner)
        
        # --- 연출 시작 ---
        
        # 1. 전체 휠 돌기
        all_names = st.session_state.students
        for _ in range(10):
            p1, p2, p3 = random.choice(all_names), random.choice(all_names), random.choice(all_names)
            slot1.markdown(f'<div class="slot-box">🌀</div>', unsafe_allow_html=True)
            slot2.markdown(f'<div class="slot-box">🌀</div>', unsafe_allow_html=True)
            slot3.markdown(f'<div class="slot-box">🌀</div>', unsafe_allow_html=True)
            time.sleep(0.05)
            
        # 2. 첫 번째 글자 멈춤
        slot1.markdown(f'<div class="slot-box">{w1}</div>', unsafe_allow_html=True)
        time.sleep(0.5) # 0.5초 대기 (심장 쫄깃)
        
        # 3. 두 번째 글자 멈춤
        slot2.markdown(f'<div class="slot-box">{w2}</div>', unsafe_allow_html=True)
        time.sleep(0.8) # 0.8초 대기 (더 쫄깃)
        
        # 4. 세 번째 글자 멈춤 & 당첨!
        slot3.markdown(f'<div class="slot-box">{w3}</div>', unsafe_allow_html=True)
        
        # 결과 표시
        st.markdown(f'<div class="win-text">🎉 당첨: {winner} !! 🎉</div>', unsafe_allow_html=True)
        st.balloons()
        
    else:
        st.warning("추첨할 3글자 이름 학생이 명단에 없습니다.")

st.write("이전 당첨자:", st.session_state.last_winner)
if st.button("기록 저장"):
    # 이번 당첨자를 DB 시트에 '당첨기록' 탭에 적는 기능은 추후 추가 가능
    st.info("기록 저장 기능은 앱스 스크립트 연동이 필요합니다.")