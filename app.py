import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="취향 테스트 | 당신의 취향은?",
    page_icon="🎯",
    layout="centered"
)

# Initialize session state variables
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"감성": 0, "로컬": 0, "낭만": 0, "힐링": 0}
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'test_completed' not in st.session_state:
    st.session_state.test_completed = False

# Check for result in URL parameters
params = st.query_params
if 'result' in params and not st.session_state.test_completed:
    try:
        result_data = params['result']
        result_pairs = result_data.split('&')
        
        for pair in result_pairs:
            key, value = pair.split('=')
            st.session_state.scores[key] = int(value)
        
        st.session_state.test_completed = True
    except:
        pass  # If there's any error parsing the URL parameters, just ignore

# Define quiz questions
questions = [
    {
        "text": "Q1. 혼자만의 시간이 주어진다면, 당신은 어디로 가고 싶나요?",
        "choices": {
            "A": "햇살 들어오는 카페에서 조용히 책 읽기",
            "B": "지역 특색 있는 골목을 산책하며 가게 구경하기",
            "C": "은은한 조명의 바에서 잔잔한 음악 들으며 잔을 기울이기",
            "D": "아무 계획 없이 자연이나 공원에서 멍 때리기"
        },
        "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
    },
    {
        "text": "Q2. 당신이 공간을 선택할 때 가장 먼저 반응하는 요소는?",
        "choices": {
            "A": "조명이나 색감 같은 분위기",
            "B": "장소가 가진 이야기나 지역성",
            "C": "대화가 자연스레 이어질 수 있는 온기 있는 자리인지",
            "D": "조용하고 편안한 동선이나 구조"
        },
        "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
    },
    {
        "text": "Q3. SNS에서 끌리는 피드 스타일은?",
        "choices": {
            "A": "감성 일상 브이로그",
            "B": "숨은 동네 핫플 소개",
            "C": "잔잔한 대화와 웃음이 흐르는 모임 사진이나 술자리 브이로그",
            "D": "바다·산·자연 속 힐링 영상"
        },
        "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
    },
    {
        "text": "Q4. 다음 중 가장 '끌리는' 카페의 느낌은?",
        "choices": {
            "A": "낮은 조도, LP 음악, 따뜻한 조명",
            "B": "오래된 골목 안, 간판 없는 로컬 카페",
            "C": "밤에도 오래 머무를 수 있고, 대화하기 좋은 아늑한 공간",
            "D": "나무 냄새 나는 테라스와 여백 많은 좌석"
        },
        "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
    },
    {
        "text": "Q5. 지금 당장 '회복'이 필요할 때 떠오르는 장소는?",
        "choices": {
            "A": "감정 정돈되는 분위기 있는 카페",
            "B": "동네 오래된 식당이나 골목길 산책",
            "C": "나를 잘 아는 친구와 마주 앉아 진심 나눌 수 있는 공간",
            "D": "조용하고 푸른 공간, 아무도 없는 벤치"
        },
        "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
    }
]

# Function to reset the quiz
def reset_quiz():
    st.session_state.current_question = 0
    st.session_state.scores = {"감성": 0, "로컬": 0, "낭만": 0, "힐링": 0}
    st.session_state.answers = []
    st.session_state.test_completed = False
    st.rerun()

# Function to process answer and move to next question
def process_answer(answer, question_idx):
    if answer:
        category = questions[question_idx]["categories"][answer]
        st.session_state.scores[category] += 1
        st.session_state.answers.append(answer)
        
        if question_idx < len(questions) - 1:
            st.session_state.current_question += 1
        else:
            st.session_state.test_completed = True
        st.rerun()

# Function to create result visualization
def create_result_chart():
    # Convert scores to percentages
    total = sum(st.session_state.scores.values())
    percentages = {k: (v / total) * 100 for k, v in st.session_state.scores.items()}
    
    # Create DataFrame
    df = pd.DataFrame({
        'Category': list(percentages.keys()),
        'Percentage': list(percentages.values())
    })
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(
        df['Category'], 
        df['Percentage'],
        color=['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB']
    )
    
    # Add percentage labels
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height + 1,
            f'{height:.0f}%',
            ha='center', 
            va='bottom',
            fontsize=12
        )
    
    ax.set_ylim(0, 100)
    ax.set_title('취향 테스트 결과', fontsize=16)
    ax.set_ylabel('퍼센트 (%)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Convert plot to image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

# Function to create shareable image
def create_shareable_image():
    # Convert scores to percentages
    total = sum(st.session_state.scores.values())
    percentages = {k: (v / total) * 100 for k, v in st.session_state.scores.items()}
    
    # Create figure with subplot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Add title and subtitle
    ax.text(0.5, 0.95, '나의 취향 테스트 결과', horizontalalignment='center', fontsize=20, fontweight='bold')
    
    # Add result bars
    categories = list(percentages.keys())
    values = list(percentages.values())
    colors = ['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB']
    
    y_pos = [0.7, 0.55, 0.4, 0.25]
    
    for i, (cat, val, color) in enumerate(zip(categories, values, colors)):
        ax.barh(y_pos[i], val, height=0.1, color=color)
        ax.text(val + 2, y_pos[i], f'{cat}: {val:.0f}%', va='center', fontsize=14)
    
    # Add footer
    ax.text(0.5, 0.1, 'www.tastetest.com에서 테스트 해보세요!', 
            horizontalalignment='center', fontsize=12, alpha=0.7)
    
    # Remove axes
    ax.axis('off')
    
    # Convert plot to image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

# Function for getting shareable image as base64
def get_image_base64(buf):
    img_str = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Main application layout
st.title("🎯 취향 테스트")
st.markdown("### 당신의 취향을 탐색해보세요!")

if not st.session_state.test_completed:
    # Display progress bar
    progress = (st.session_state.current_question) / len(questions) * 100
    st.progress(progress/100)
    st.markdown(f"### {st.session_state.current_question + 1}/{len(questions)}")
    
    # Display current question
    current_q = questions[st.session_state.current_question]
    st.markdown(f"## {current_q['text']}")
    
    # Display answer choices
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"A. {current_q['choices']['A']}", key="A", use_container_width=True):
            process_answer("A", st.session_state.current_question)
        if st.button(f"C. {current_q['choices']['C']}", key="C", use_container_width=True):
            process_answer("C", st.session_state.current_question)
    
    with col2:
        if st.button(f"B. {current_q['choices']['B']}", key="B", use_container_width=True):
            process_answer("B", st.session_state.current_question)
        if st.button(f"D. {current_q['choices']['D']}", key="D", use_container_width=True):
            process_answer("D", st.session_state.current_question)

else:
    # Display results
    st.markdown("## ✨ 당신의 취향 결과입니다")
    
    # Calculate percentages
    total = sum(st.session_state.scores.values())
    percentages = {k: (v / total) * 100 for k, v in st.session_state.scores.items()}
    
    # Sort categories by percentage
    sorted_percentages = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    
    # Display detailed percentage results with comments
    st.markdown("### 테스트 결과")
    
    # Create result summary text
    result_categories = []
    for category, percent in sorted_percentages:
        if percent > 0:
            result_categories.append(f"{category} {percent:.0f}%")
    
    result_text = ", ".join(result_categories)
    st.markdown(f"#### 당신은 {result_text}로 구성된 사람입니다!")
    
    # Display metrics for each category
    for cat, percent in sorted_percentages:
        if percent > 0:
            st.metric(cat, f"{percent:.0f}%")
    
    # Result descriptions
    category_descriptions = {
        "감성": "분위기와 감성을 중요시하며, 조명과 색감에 민감하게 반응하는 편입니다.",
        "로컬": "장소가 가진 이야기와 지역성을 중요시하며, 오래된 골목길이나 지역의 특색있는 공간을 선호합니다.",
        "낭만": "온기있고 대화가 자연스럽게 이어지는 공간을 좋아하며, 은은한 조명 아래 진솔한 이야기를 나눌 수 있는 공간을 선호합니다.",
        "힐링": "여백이 있고 편안함을 주는 공간을 좋아하며, 자연 속에서 멍때리거나 조용한 곳을 선호합니다."
    }
    
    # Show descriptions for categories with non-zero percentages
    st.markdown("#### 당신의 취향 설명")
    for category, percent in sorted_percentages:
        if percent > 0:
            st.markdown(f"**{category}**: {category_descriptions[category]}")
    
    # Just add restart button
    if st.button("테스트 다시하기", use_container_width=True):
        reset_quiz()
            
    # Add Gongridan-gil recommendation first
if st.session_state.test_completed:
    st.markdown("---")
    st.subheader("당신을 위한 추천")
    
    # Gongridan-gil recommendation
    st.markdown("### 공리단길에서 당신의 취향에 맞는 코스를 찾아보세요!")
    gongridan_link = "https://www.notion.so/88e346b3954242d3803d36af70912859?pvs=4"
    st.markdown(f"[공리단길 코스 추천 보러가기]({gongridan_link})")
    st.markdown("당신의 취향에 맞게 특별하게 큐레이션된 코스를 확인해보세요.")
    
    # Add test link sharing option second
    st.markdown("---")
    st.markdown("### 테스트 링크 공유하기")
    share_link = "https://tastetest.replit.app"
    st.code(share_link, language=None)
    st.markdown("위 링크를 복사해서 친구들과 공유해보세요!")

# Footer
st.markdown("---")
st.markdown("© 2025 취향테스트 | 당신의 취향은 무엇인가요?")
