import streamlit as st
import pandas as pd
import random
import time

# ... (CSS 및 초기화 설정은 이전과 동일) ...

if st.button("🎲 학생 뽑기 시작!"):
    winner = random.choice(st.session_state.students)
    w_list = list(winner)
    stop_order = random.sample([0, 1, 2], 3)
    
    # 1. 전체 회전
    for _ in range(15):
        slot_placeholder.markdown(render_slots([random.choice(unique_chars) for _ in range(3)], rolling_indices=[0,1,2]))
        time.sleep(0.05)

    # 2. 하나씩 멈춤 (데이터와 일치시키기)
    current_display = ["?", "?", "?"]
    fixed_indices = []
    
    for i in range(3):
        target_idx = stop_order[i]
        
        # 감속 구간 (데이터는 건드리지 않고 시각만 랜덤으로 굴림)
        for slow_down in [0.1, 0.25, 0.5]:
            temp = current_display[:]
            # 멈춰야 할 타겟 인덱스에만 랜덤 글자 표시 (데이터는 ??? 상태 유지)
            temp[target_idx] = random.choice(unique_chars) 
            rolling = [j for j in range(3) if j not in fixed_indices and j != target_idx]
            render_slots(temp, rolling_indices=rolling + [target_idx], fixed_indices=fixed_indices)
            time.sleep(slow_down)
        
        # ★핵심 수정: 여기서 타겟 인덱스를 확정된 글자로 '강제' 고정
        current_display[target_idx] = w_list[target_idx] 
        fixed_indices.append(target_idx)
        
        # 멈춘 후 대기 (데이터 고정 확인)
        if i < 2:
            start_wait = time.time()
            while time.time() - start_wait < 1.0:
                temp = current_display[:]
                for j in range(3):
                    if j not in fixed_indices:
                        temp[j] = random.choice(unique_chars)
                render_slots(temp, rolling_indices=[j for j in range(3) if j not in fixed_indices], fixed_indices=fixed_indices)
                time.sleep(0.1)
        else:
            # 마지막까지 다 멈추면 최종 결과 렌더링
            render_slots(current_display, fixed_indices=fixed_indices)

    st.balloons()
    st.success(f"🎊 당첨자: {winner} !! 🎊")