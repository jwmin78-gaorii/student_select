import streamlit as st
import pandas as pd
import random
import time

# 구글 시트 설정
SHEET_ID = "1la5w_VJ96KPik7hcATR76RNflM-7EOF2vL87jBsXUVM"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

# 페이지 설정
st.set_page_config(page_title="강의실 슬롯머신", layout="centered")

# CSS 디자인 (게임기 느낌)
st.markdown("""
    <style>
    .slot-box { 
        background-color: #262730; border: 5px solid #FFD700; border-radius: 15px; 
        font-size: 50px; font-weight: bold; text-align: center; padding: 20px; 
        margin: 5px; color: #FFFFFF; height: 120px; display: flex; 
        justify-content: center; align-items: center; 
    }
    .slot-fixed { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# 데이터 가져오기
def get_student_list():
    try:
        df = pd.read_csv(URL)
        return [n for n in df['회원이름'].dropna().tolist() if len(str(n)) == 3]
    except:
        return []

if 'students' not in st.session_state:
    st.session_state.students = get_student_list()

st.title("🎰 강의실 슬롯머신")

# 슬롯 영역 생성
c1, c2, c3 = st.columns(3)
slots = [c1.empty(), c2.empty(), c3.empty()]

# 초기 상태 표시
for s in slots:
    s.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)

if st.button("🔄 명단 새로고침"):
    st.session_state.students = get_student_list()
    st.success(f"3글자 학생 {len(st.session_state.students)}명 로드 완료!")

# 추첨 버튼
if st.button("🎲 두근두근 학생 뽑기 시작!", use_container_width=True):
    if st.session_state.students:
        winner = random.choice(st.session_state.students)
        w_list = list(winner)
        
        # 전체 휠이 굴러가는 연출
        for _ in range(10):
            for s in slots:
                s.markdown(f'<div class="slot-box">{random.choice("가나다라마바사아자차")}</div>', unsafe_allow_html=True)
            time.sleep(0.05)
            
        # 순차적으로 정지
        for i in range(3):
            # 나머지 돌아가는 애들은 계속 랜덤값 출력
            for j in range(i, 3):
                slots[j].markdown(f'<div class="slot-box">{random.choice("가나다라마바사아자차")}</div>', unsafe_allow_html=True)
            
            # i번째 멈춤
            slots[i].markdown(f'<div class="slot-box slot-fixed">{w_list[i]}</div>', unsafe_allow_html=True)
            time.sleep(0.5) # 멈추는 간격 (쫄깃함 추가)
            
        st.success(f"🎊 오늘의 당첨자: {winner} 🎊")
        st.balloons()
    else:
        st.error("명단에 3글자 이름이 없습니다.")