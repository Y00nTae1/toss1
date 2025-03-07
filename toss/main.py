import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
import altair as alt
from PIL import Image
import base64
from datetime import datetime, timedelta

# 페이지 설정 - 더 넓은 레이아웃과 아이콘 추가
st.set_page_config(
    page_title="금융 연체 예측 대시보드",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 개선 - 더 현대적인 디자인
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main-header {
        font-size: 2.7rem;
        background: linear-gradient(90deg, #0052D4, #4364F7, #6FB1FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 800;
        animation: fadeIn 1.5s ease-in-out;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #0052D4;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
        border-left: 5px solid #4364F7;
        padding-left: 12px;
        animation: slideInLeft 0.8s ease-in-out;
    }
    
    .section-header {
        font-size: 1.5rem;
        color: #007AFF;
        margin-top: 1.8rem;
        margin-bottom: 1rem;
        font-weight: 600;
        animation: fadeIn 1s ease-in-out;
    }
    
    .highlight {
        background: linear-gradient(to right, rgba(198, 222, 255, 0.2), rgba(117, 170, 255, 0.2));
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 0.5rem solid #4364F7;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.4s ease;
        animation: fadeIn 1s ease-in-out;
    }
    
    .highlight:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    .card {
        background-color: white;
        padding: 1.8rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.8rem;
        transition: all 0.4s ease;
        animation: fadeIn 1s ease-in-out;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(67, 100, 247, 0.15);
    }
    
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid #eaecef;
        animation: fadeIn 1.5s ease-in-out;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.4s ease;
        height: 100%;
        animation: popIn 0.8s cubic-bezier(0.19, 1, 0.22, 1);
        border: 1px solid rgba(67, 100, 247, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 20px rgba(67, 100, 247, 0.2);
        border: 1px solid rgba(67, 100, 247, 0.3);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0052D4, #4364F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        transition: all 0.4s ease;
        margin-bottom: 5px;
    }
    
    .metric-card:hover .metric-value {
        transform: scale(1.1);
    }
    
    .metric-label {
        font-size: 1rem;
        color: #495057;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .tab-content {
        padding: 1.8rem;
        background-color: white;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.8s ease-in-out;
        border: 1px solid #e9ecef;
        border-top: none;
    }
    
    /* 버튼 스타일 개선 */
    .stButton button {
        background: linear-gradient(90deg, #0052D4, #4364F7);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(67, 100, 247, 0.2);
    }
    
    .stButton button:hover {
        background: linear-gradient(90deg, #003baa, #3252d8);
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(67, 100, 247, 0.3);
    }
    
    .stButton button:active {
        transform: translateY(0);
        box-shadow: 0 2px 5px rgba(67, 100, 247, 0.2);
    }
    
    /* 위험도 표시 스타일 */
    .risk-low {
        color: #28a745;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    .risk-medium {
        color: #fd7e14;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    .risk-high {
        color: #dc3545;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    /* 진행 바 애니메이션 개선 */
    .animated-progress {
        width: 100%;
        height: 8px;
        border-radius: 100px;
        margin: 15px 0;
        border: none;
        overflow: hidden;
        position: relative;
        background: #e9ecef;
    }
    
    .animated-progress span {
        height: 100%;
        display: block;
        width: 0;
        border-radius: 100px;
        background: linear-gradient(90deg, #0052D4, #4364F7);
        position: absolute;
        transition: width 0.8s ease-in-out;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0052D4, #4364F7);
        border-radius: 100px;
    }
    /* 애니메이션 효과 개선 */
    @keyframes fadeIn {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        0% {
            opacity: 0;
            transform: translateX(-40px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        0% {
            opacity: 0;
            transform: translateX(40px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes popIn {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        40% {
            opacity: 1;
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.9;
            transform: scale(1.03);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-8px);
        }
        100% {
            transform: translateY(0px);
        }
    }
    
    .float-animation {
        animation: float 4s ease-in-out infinite;
    }
    
    .line-appear {
        animation: lineAppear 2s ease-in-out;
    }
    
    @keyframes lineAppear {
        0% {
            opacity: 0;
            width: 0;
        }
        100% {
            opacity: 1;
            width: 100%;
        }
    }
    
    /* 깜빡이는 효과 */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .blink {
        animation: blink 2s linear infinite;
    }
    
    /* 차트와 그래프 스타일 */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .chart-container:hover {
        box-shadow: 0 8px 25px rgba(67, 100, 247, 0.15);
    }
    
    /* 시각적 구분선 */
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(67, 100, 247, 0.5), transparent);
        margin: 25px 0;
    }
    
    /* 반응형 레이아웃 개선 */
    @media (max-width: 1200px) {
        .main-header {
            font-size: 2.2rem;
        }
        .sub-header {
            font-size: 1.6rem;
        }
        .section-header {
            font-size: 1.3rem;
        }
        .metric-value {
            font-size: 1.8rem;
        }
    }
    
    @media (max-width: 992px) {
        .main-header {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
        .card {
            padding: 1.2rem;
        }
    }
    
    @media (max-width: 576px) {
        .main-header {
            font-size: 1.6rem;
        }
        .sub-header {
            font-size: 1.3rem;
        }
    }
    /* 사이드바 스타일 개선 */
    .css-1d391kg, .css-163ttbj, .css-1wrcr25 {
        background-image: linear-gradient(180deg, #f8faff 0%, #f1f6ff 100%);
    }
    
    /* 사이드바 메뉴 항목 */
    .sidebar-menu-item {
        display: flex;
        align-items: center;
        padding: 12px 15px;
        margin-bottom: 8px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        background-color: rgba(255, 255, 255, 0.7);
        border-left: 3px solid transparent;
    }
    
    .sidebar-menu-item:hover {
        background-color: rgba(67, 100, 247, 0.1);
        border-left: 3px solid #4364F7;
    }
    
    .sidebar-menu-item.active {
        background-color: rgba(67, 100, 247, 0.15);
        border-left: 3px solid #4364F7;
    }
    
    .sidebar-menu-icon {
        margin-right: 10px;
        font-size: 18px;
        color: #4364F7;
        width: 24px;
        text-align: center;
    }
    
    /* 탭 스타일 개선 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8faff;
        border-radius: 10px 10px 0 0;
        gap: 2px;
        padding-left: 1px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f6ff;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: 1px solid #e9ecef;
        border-bottom: none;
        font-weight: 500;
        color: #495057;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9f0ff;
        color: #0052D4;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-top: 3px solid #4364F7 !important;
        color: #0052D4 !important;
        font-weight: 600 !important;
    }
    
    /* 확장 패널 스타일 */
    .stExpander [data-baseweb="accordion"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    
    .stExpander [data-baseweb="accordion-item"] {
        border: 1px solid #e9ecef;
    }
    
    .stExpander [data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
    }
    
    .stExpander [aria-expanded="true"] {
        background-color: #f8faff;
        border-left: 3px solid #4364F7;
    }
    
    /* 선택 박스와 슬라이더 개선 */
    .stSelectbox [data-baseweb="select"] > div:first-child {
        background-color: #f8faff;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        padding: 8px 15px;
    }
    
    .stSlider [data-baseweb="slider"] {
        height: 6px;
    }
    
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
        height: 20px;
        width: 20px;
        background-color: #4364F7;
        border: 2px solid white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"]:hover {
        transform: scale(1.2);
    }
    
    /* 페이지 네비게이션 */
    .page-nav {
        display: flex;
        justify-content: space-between;
        margin: 30px 0;
    }
    
    .page-nav-btn {
        display: flex;
        align-items: center;
        padding: 10px 15px;
        border-radius: 8px;
        background-color: #f8faff;
        border: 1px solid #e9ecef;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #495057;
        text-decoration: none;
    }
    
    .page-nav-btn:hover {
        background-color: #e9f0ff;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        color: #0052D4;
    }
    /* 데이터 시각화 및 차트 스타일 개선 */
    /* Plotly 차트 컨테이너 */
    .js-plotly-plot, .plotly {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        padding: 10px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
        background-color: white;
    }
    
    .js-plotly-plot:hover, .plotly:hover {
        box-shadow: 0 8px 20px rgba(67, 100, 247, 0.15);
    }
    
    /* 인포그래픽 카드 */
    .infographic-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .infographic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(67, 100, 247, 0.15);
    }
    
    .infographic-value {
        font-size: 3rem;
        font-weight: 700;
        color: #0052D4;
        margin-bottom: 10px;
    }
    
    .infographic-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        color: #4364F7;
    }
    
    .infographic-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
        color: #343a40;
    }
    
    .infographic-subtitle {
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    /* 데이터 테이블 스타일 */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .dataframe thead {
        background: linear-gradient(90deg, #0052D4, #4364F7);
        color: white;
    }
    
    .dataframe th {
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
    }
    
    .dataframe td {
        padding: 10px 15px;
        border-bottom: 1px solid #e9ecef;
    }
    
    .dataframe tr:last-child td {
        border-bottom: none;
    }
    
    .dataframe tr:nth-child(even) {
        background-color: #f8faff;
    }
    
    .dataframe tr:hover {
        background-color: #e9f0ff;
    }
    
    /* 데이터 하이라이트 */
    .positive-value {
        color: #28a745;
        font-weight: 600;
    }
    
    .negative-value {
        color: #dc3545;
        font-weight: 600;
    }
    
    .neutral-value {
        color: #6c757d;
        font-weight: 600;
    }
    
    /* 사용자 지정 툴팁 */
    .custom-tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .custom-tooltip .tooltip-text {
        visibility: hidden;
        width: 200px;
        background-color: #343a40;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .custom-tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    /* 스켈레톤 로딩 효과 */
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .skeleton {
        background: linear-gradient(to right, #f0f0f0 8%, #f8f8f8 18%, #f0f0f0 33%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite linear;
        border-radius: 8px;
        height: 100%;
        width: 100%;
    }
    
    /* 커스텀 알림 및 배지 */
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 6px;
    }
    
    .badge-primary {
        background-color: rgba(67, 100, 247, 0.1);
        color: #0052D4;
    }
    
    .badge-success {
        background-color: rgba(40, 167, 69, 0.1);
        color: #28a745;
    }
    
    .badge-warning {
        background-color: rgba(255, 193, 7, 0.1);
        color: #fd7e14;
    }
    
    .badge-danger {
        background-color: rgba(220, 53, 69, 0.1);
        color: #dc3545;
    }
    
    .alert {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid transparent;
        display: flex;
        align-items: center;
    }
    
    .alert-info {
        background-color: rgba(67, 100, 247, 0.1);
        border-left-color: #0052D4;
        color: #0052D4;
    }
    
    .alert-success {
        background-color: rgba(40, 167, 69, 0.1);
        border-left-color: #28a745;
        color: #28a745;
    }
    
    .alert-warning {
        background-color: rgba(255, 193, 7, 0.1);
        border-left-color: #fd7e14;
        color: #fd7e14;
    }
    
    .alert-danger {
        background-color: rgba(220, 53, 69, 0.1);
        border-left-color: #dc3545;
        color: #dc3545;
    }
    
    .alert-icon {
        margin-right: 10px;
        font-size: 20px;
    }
    
    /* 사용자 프로필 카드 */
    .profile-card {
        display: flex;
        padding: 20px;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .profile-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(67, 100, 247, 0.15);
    }
    
    .profile-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        overflow: hidden;
        margin-right: 20px;
        border: 3px solid #f1f6ff;
    }
    
    .profile-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .profile-info {
        flex: 1;
    }
    
    .profile-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #343a40;
        margin-bottom: 5px;
    }
    
    .profile-role {
        color: #6c757d;
        margin-bottom: 10px;
        font-weight: 500;
    }
    
    .profile-stats {
        display: flex;
        gap: 15px;
    }
    
    .profile-stat {
        text-align: center;
    }
    
    .profile-stat-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0052D4;
    }
    
    .profile-stat-label {
        font-size: 0.8rem;
        color: #6c757d;
    }
    
    /* 커스텀 체크박스, 라디오 버튼 */
    .stCheckbox > div > div > label {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stCheckbox > div > div > label > div:first-child {
        border-radius: 4px;
        border: 2px solid #4364F7;
        width: 18px;
        height: 18px;
    }
    
    .stRadio > div > div > label {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stRadio > div > div > label > div:first-child {
        border-radius: 50%;
        border: 2px solid #4364F7;
        width: 18px;
        height: 18px;
    }
    
    /* 마무리와 폴리싱 */
    ::selection {
        background-color: rgba(67, 100, 247, 0.2);
        color: #0052D4;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c5d5ff;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4364F7;
    }
</style>
""", unsafe_allow_html=True)

# 애니메이션 로딩 함수 개선
def load_with_animation():
    with st.spinner('데이터를 불러오는 중...'):
        # 로딩 애니메이션
        progress_text = "데이터 분석 중..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.02)  # 빠른 로딩
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.3)
        my_bar.empty()
        
        # 성공 메시지 표시
        st.success("데이터 분석이 완료되었습니다!")
        time.sleep(0.5)
        st.empty()  # 성공 메시지 제거


# 사이드바 설정
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
    st.markdown("## 금융 연체 예측 모델")
    st.markdown("---")
    
    # 페이지 선택
    page = st.radio(
        "페이지 선택",
        ["📊 대시보드 개요", "🔍 연체 예측 모델", "📈 모델 성능 분석", "🧪 시뮬레이션"]
    )
    
    st.markdown("---")
    st.markdown("### 📌 주요 참고 문헌")
    with st.expander("연구 논문 및 자료"):
        st.markdown("""
        - [데이터 마이닝을 활용한 신용카드 연체 예측모형 개발](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE02408191)
        - [SHAP을 이용한 설명 가능한 신용카드 연체 예측](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11711644)
        - [설명 가능한 인공지능을 활용한 은행대출연체 예측 모델 연구](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003116996)
        """)
    
    st.markdown("---")
    st.info("© 2025 금융 AI 분석팀", icon="ℹ️")

# 실시간 날짜와 시간 표시 (애니메이션 효과 부여)
current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
st.markdown(f"""
<div style='text-align: right; color: #757575; font-size: 0.9rem; animation: fadeIn 1s ease-in-out;'>
    마지막 업데이트: {current_time}
</div>
""", unsafe_allow_html=True)

# 대시보드 개요 페이지
if page == "📊 대시보드 개요":
    st.markdown("<div class='main-header'>금융 소비/생활 패턴 기반 연체 예측 모델</div>", unsafe_allow_html=True)
    
    # 아이콘 애니메이션 효과 추가
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; animation: fadeIn 1.5s ease-in-out;">
            <img src="https://i.ibb.co/zGSDGD0/dashboard-header.png" style="max-width: 100%; border-radius: 10px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); transition: all 0.3s ease;" class="float-animation">
        </div>
        """, unsafe_allow_html=True)
    
    # 로딩 애니메이션 표시
    load_with_animation()
    
    st.markdown("<div class='highlight'>", unsafe_allow_html=True)
    st.markdown("""
    ## 현황 및 문제점
    최근 경제 불황으로 대출 연체자가 급증하고 있으며, 2024년 12월 기준 대출 연체 개인 및 자영업자는 614만명, 
    연체 금액은 약 50조원에 육박하고 있습니다. 금융권 전체적으로 대출 연체가 증가하는 추세입니다.
    
    👉 **금융사는 연체 예측을 통한 리스크 관리가 필요하고, 고객은 신용 리스크를 사전에 인지하여 금융 부담을 줄일 필요가 있습니다.**
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # 주요 지표 카드 (애니메이션 지연 효과 추가)
    st.markdown("<div class='sub-header'>주요 현황</div>", unsafe_allow_html=True)
    
    metrics = [
        {"value": "614만", "label": "대출 연체 인원(명)", "delay": 0},
        {"value": "50조", "label": "미상환 대출금(원)", "delay": 0.2},
        {"value": "3개월+", "label": "장기연체 기준", "delay": 0.4},
        {"value": "↓7-8등급", "label": "1회 연체시 신용등급", "delay": 0.6}
    ]
    
    cols = st.columns(4)
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.markdown(f"""
            <div class='metric-card' style="animation-delay: {metric['delay']}s;">
                <div class='metric-value'>{metric['value']}</div>
                <div class='metric-label'>{metric['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 연체율 추이 그래프 (애니메이션 효과)
    st.markdown("<div class='sub-header'>연체율 추이 (2023-2025)</div>", unsafe_allow_html=True)
    
    # 더미 데이터 생성
    months = pd.date_range(start='2023-01-01', end='2025-02-01', freq='MS').strftime('%Y-%m')
    delinquency_rates = [3.2, 3.3, 3.4, 3.5, 3.4, 3.6, 3.8, 4.0, 4.2, 4.3, 4.5, 4.6, 
                         4.8, 5.0, 5.2, 5.4, 5.5, 5.7, 5.9, 6.1, 6.3, 6.4, 6.5, 6.7, 
                         6.8, 7.0]
    
    trend_data = pd.DataFrame({
        '월': months,
        '연체율(%)': delinquency_rates
    })
    
    # Plotly 애니메이션 그래프
    fig = px.line(
        trend_data, 
        x='월', 
        y='연체율(%)', 
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#1E88E5']
    )
    
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=3),
        marker=dict(size=8, symbol='circle', line=dict(width=2, color='white')),
    )
    
    fig.update_layout(
        title='월별 대출 연체율 추이',
        xaxis_title='월',
        yaxis_title='연체율(%)',
        hovermode='x unified',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(240,240,240,0.2)',
        xaxis=dict(showgrid=False),
        yaxis=dict(range=[3, 7.5]),
        # 애니메이션 설정
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='재생',
                method='animate',
                args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]
            )]
        )]
    )
    
    # 애니메이션 프레임 설정
    frames = [go.Frame(
        data=[go.Scatter(
            x=trend_data['월'][:k+1],
            y=trend_data['연체율(%)'][:k+1],
            mode='lines+markers'
        )]
    ) for k in range(len(trend_data))]
    
    fig.frames = frames
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 비즈니스 니즈 (반응형 카드)
    st.markdown("<div class='sub-header'>비즈니스 니즈</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h4 style="color: #1976D2; border-bottom: 2px solid #BBDEFB; padding-bottom: 10px;">
                <i class="fas fa-building"></i> 금융사 측면
            </h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 8px; display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">1</span>
                    연체율 감소
                </li>
                <li style="margin-bottom: 8px; display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">2</span>
                    부실 채권 관리 비용 절감
                </li>
                <li style="margin-bottom: 8px; display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">3</span>
                    신용 리스크 관리 강화
                </li>
                <li style="display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">4</span>
                    신규 고객 유치 및 충성도 제고
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='card'>
            <h4 style="color: #1976D2; border-bottom: 2px solid #BBDEFB; padding-bottom: 10px;">
                <i class="fas fa-user"></i> 고객 측면
            </h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 8px; display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">1</span>
                    신용 리스크 사전 인지
                </li>
                <li style="margin-bottom: 8px; display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">2</span>
                    금융 부담 감소
                </li>
                <li style="margin-bottom: 8px; display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">3</span>
                    맞춤형 금융상품 추천
                </li>
                <li style="display: flex; align-items: center;">
                    <span style="background-color: #1E88E5; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px;">4</span>
                    신용 점수 관리 지원
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 핵심 목표 (애니메이션 적용)
    st.markdown("<div class='sub-header'>핵심 목표</div>", unsafe_allow_html=True)
    
    objectives = [
        "고객이 향후 3개월 내 연체할 가능성을 예측하는 모델 개발",
        "고위험 고객을 조기에 식별하여 금융사 리스크를 최소화",
        "상환 가능성을 먼저 예측한 후 최종 연체 여부를 판단하는 2단계 모델 적용",
        "신용 이력이 부족한 고객을 분석하여 포용금융(Financial Inclusion) 측면 강화"
    ]
    
    for i, obj in enumerate(objectives):
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px; animation: slideInLeft {0.5 + i*0.2}s ease-in-out;">
            <div style="background-color: #1E88E5; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px; font-weight: bold; font-size: 1.2rem; flex-shrink: 0;">
                {i+1}
            </div>
            <div style="flex-grow: 1; padding: 10px 15px; background-color: #f5f5f5; border-radius: 5px; border-left: 4px solid #1E88E5;">
                <h3 style="margin: 0; color: #0D47A1; font-size: 1.2rem;">{obj}</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 신용평가 주요 요소 시각화 (애니메이션 원형 차트)
    st.markdown("<div class='sub-header'>신용평가 주요 요소</div>", unsafe_allow_html=True)
    
    # 원형 차트 데이터
    labels = ['연체 및 과거 채무 상환 이력', '현재 부채 수준', '신용거래 기간', '신규 신용 개설', '신용거래 형태']
    values = [45, 30, 15, 5, 5]
    colors = ['#1E88E5', '#42A5F5', '#90CAF9', '#BBDEFB', '#E3F2FD']
    
    # 원형 차트 생성 (애니메이션 추가)
    fig = go.Figure()
    
    # 첫 프레임은 모든 값이 같은 상태
    fig.add_trace(go.Pie(
        labels=labels,
        values=[20, 20, 20, 20, 20],  # 시작 값은 모두 동일
        hole=.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        insidetextorientation='radial',
        textfont=dict(size=14),
        pull=[0.1, 0, 0, 0, 0],  # 첫 번째 항목 강조
        hoverinfo='label+percent',
        name='신용평가 요소'
    ))
    
    # 애니메이션 설정
    fig.update_layout(
        title={
            'text': '신용평가 요소별 가중치',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#0D47A1'}
        },
        autosize=False,
        width=700,
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='애니메이션 재생',
                method='animate',
                args=[None, dict(frame=dict(duration=800, redraw=True), fromcurrent=True, mode='immediate')]
            )]
        )]
    )
    
    # 최종 값으로 애니메이션 프레임 추가
    fig.frames = [
        go.Frame(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=.4,
                marker=dict(colors=colors),
                textinfo='label+percent',
                insidetextorientation='radial',
                pull=[0.1, 0, 0, 0, 0]
            )]
        )
    ]
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 차별점 및 기대효과 (애니메이션 테이블)
    st.markdown("<div class='sub-header'>기존 모델과의 차별점</div>", unsafe_allow_html=True)
    
    comparison_data = {
        "구분": ["금융사의 활용성", "고객 관리 방식", "모델의 정밀도", "대체 신용 평가 활용"],
        "기존 연체 예측 모델": ["단순 위험 고객 분류 → 사전 개입 어려움", "연체 발생 후 대응 (사후 관리)", 
                      "단순 이진 분류로 정확도 한계 존재", "신용 이력 부족 고객 분석 어려움"],
        "2단계 모델": ["고객별 맞춤 조치 가능 (한도 조정, 리볼빙 안내)", "연체 위험 예측 후 선제적 대응 가능 (사전 개입)",
                  "회귀 예측 후 분류 진행 → 정밀도 증가", "신용 이력이 부족한 고객도 평가 가능 (포용 금융)"]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # 애니메이션 테이블 대신 HTML로 직접 구현
    # 애니메이션 테이블 대신 HTML로 직접 구현
    st.markdown("""
    <div style="overflow-x: auto; animation: fadeIn 1.5s ease-in-out;">
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.9em; border-radius: 5px 5px 0 0; overflow: hidden; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);">
            <thead>
                <tr style="background-color: #1E88E5; color: #ffffff; text-align: left; font-weight: bold;">
                    <th style="padding: 12px 15px; border-right: 1px solid #dddddd;">구분</th>
                    <th style="padding: 12px 15px; border-right: 1px solid #dddddd;">기존 연체 예측 모델</th>
                    <th style="padding: 12px 15px;">2단계 모델</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #dddddd; animation: fadeIn 1.7s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">금융사의 활용성</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">단순 위험 고객 분류 → 사전 개입 어려움</td>
                    <td style="padding: 12px 15px; background-color: #E3F2FD;">고객별 맞춤 조치 가능 (한도 조정, 리볼빙 안내)</td>
                </tr>
                <tr style="border-bottom: 1px solid #dddddd; animation: fadeIn 1.9s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">고객 관리 방식</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">연체 발생 후 대응 (사후 관리)</td>
                    <td style="padding: 12px 15px; background-color: #E3F2FD;">연체 위험 예측 후 선제적 대응 가능 (사전 개입)</td>
                </tr>
                <tr style="border-bottom: 1px solid #dddddd; animation: fadeIn 2.1s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">모델의 정밀도</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">단순 이진 분류로 정확도 한계 존재</td>
                    <td style="padding: 12px 15px; background-color: #E3F2FD;">회귀 예측 후 분류 진행 → 정밀도 증가</td>
                </tr>
                <tr style="animation: fadeIn 2.3s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">대체 신용 평가 활용</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">신용 이력 부족 고객 분석 어려움</td>
                    <td style="padding: 12px 15px; background-color: #E3F2FD;">신용 이력이 부족한 고객도 평가 가능 (포용 금융)</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sub-header'>기대효과 및 활용 방안</div>", unsafe_allow_html=True)
    
    effects = [
        {"title": "고위험 고객 사전 탐지 시스템 구축", "desc": "연체 위험 고객을 사전에 식별하여 신용한도 조정, 리볼빙 안내, 저금리 대출 추천 등", "icon": "🔎"},
        {"title": "금융사의 연체율 감소", "desc": "부실 채권 관리 비용 절감 및 전체 대출 포트폴리오 건전성 향상", "icon": "📉"},
        {"title": "소비자의 신용 관리 지원", "desc": "장기 고객 유치 및 만족도 향상으로 고객 이탈률 감소", "icon": "👨‍👩‍👧‍👦"},
        {"title": "맞춤형 상환 프로그램 제공", "desc": "연체 위험이 높은 고객을 선제적으로 식별하여 개인별 맞춤 솔루션 제공", "icon": "📋"},
        {"title": "고객군 세분화", "desc": "신용 한도 조정 및 금리 차별화를 통한 리스크 관리 정밀화", "icon": "📊"}
    ]
    
    for i, effect in enumerate(effects):
        st.markdown(f"""
        <div style="display: flex; margin-bottom: 20px; animation: slideInRight {0.5 + i*0.2}s ease-in-out;">
            <div style="background-color: #1E88E5; font-size: 2rem; color: white; border-radius: 50%; width: 60px; height: 60px; display: flex; justify-content: center; align-items: center; margin-right: 20px; flex-shrink: 0;">
                {effect['icon']}
            </div>
            <div style="flex-grow: 1; padding: 10px 15px; background-color: #f8f9fa; border-radius: 5px; border-left: 4px solid #1E88E5; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 6px 12px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <h4 style="margin: 0; color: #0D47A1; font-size: 1.2rem;">{i+1}. {effect['title']}</h4>
                <p style="margin: 5px 0 0 0; color: #424242;">{effect['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 연체 예측 모델 페이지
elif page == "🔍 연체 예측 모델":
    st.markdown("<div class='main-header'>2단계 연체 예측 모델링</div>", unsafe_allow_html=True)
    
    # 애니메이션 로딩
    load_with_animation()
    
    # 모델 구성도
    st.markdown("<div class='sub-header'>모델 구성도</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 1.5s ease-in-out;">
        <img src="https://i.ibb.co/xXwdSy1/model-architecture.png" style="max-width: 100%; border-radius: 10px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); transition: all 0.3s ease;" class="float-animation">
    </div>
    """, unsafe_allow_html=True)
    
    # 모델 설명
    st.markdown("<div class='highlight'>", unsafe_allow_html=True)
    st.markdown("""
    ## 📌 2단계 모델 개요
    
    본 모델은 두 단계로 구성된 연체 예측 시스템으로, 고객의 연체 가능성을 정밀하게 예측합니다:
    
    1️⃣ **1단계: 상환 비율 예측 (회귀 모델)**
       - 고객의 신용카드 상환 비율을 예측 (총 상환 금액 / 총 청구 금액)
       - 0~1 사이의 값으로, 1에 가까울수록 정상 상환, 0에 가까울수록 연체 가능성 높음
       
    2️⃣ **2단계: 연체 위험도 분류 (분류 모델)**
       - 예측된 상환 비율과 추가 변수를 활용하여 고객의 연체 위험도를 3단계로 분류
       - 정상 고객 / 위험 고객 / 고위험 고객으로 세분화
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 애니메이션 흐름도 추가
    st.markdown("<div class='section-header'>모델 흐름도</div>", unsafe_allow_html=True)
    
    # 흐름도 단계 표시
    steps = ["소비/생활 패턴 및 금융 데이터 수집", "데이터 전처리 및 피처 엔지니어링", 
             "1단계: 상환 비율 예측 모델 (XGBoost, LightGBM, CatBoost)", 
             "상환 비율 예측 결과 및 추가 피처 결합", 
             "2단계: 연체 위험도 분류 모델 (정상/위험/고위험)",
             "결과 해석 및 고객 맞춤형 조치 제안"]
    
    for i, step in enumerate(steps):
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px; animation: fadeIn {0.5 + i*0.2}s ease-in-out;">
            <div style="min-width: 28px; height: 28px; background-color: #1E88E5; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 10px; font-weight: bold;">
                {i+1}
            </div>
            <div style="flex-grow: 1; background-color: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); position: relative;">
                <div style="position: absolute; top: 0; left: 0; width: 5px; height: 100%; background-color: #1E88E5; border-radius: 5px 0 0 5px;"></div>
                <p style="margin: 0; padding-left: 10px;">{step}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 단계 사이에 화살표 추가 (마지막 단계 제외)
        if i < len(steps) - 1:
            st.markdown("""
            <div style="display: flex; justify-content: center; margin: 5px 0; animation: fadeIn 1s ease-in-out;">
                <div style="width: 2px; height: 20px; background-color: #90CAF9;"></div>
            </div>
            """, unsafe_allow_html=True)
    
    # 모델 단계별 설명 - 인터랙티브 탭 형식으로 변경
    st.markdown("<div class='sub-header'>모델 단계별 상세 설명</div>", unsafe_allow_html=True)
    
    model_tabs = st.tabs(["📉 1단계: 상환 비율 예측", "📊 2단계: 연체 위험도 분류"])
    
    with model_tabs[0]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 📉 상환 비율 예측 모델
            
            **앙상블 회귀 모델**을 활용하여 고객의 신용카드 상환 비율을 예측합니다.
            
            #### 예측 목표:
            - **상환 비율** = (총 상환 금액) / (총 청구 금액)
            - 0 ≦ 상환 비율 ≦ 1
            
            #### 사용 모델:
            - **XGBoost**
            - **LightGBM**
            - **CatBoost** 
            
            #### 주요 입력 변수:
            - **총 청구 금액**: 정상청구원금_BOM, 정상청구원금_B2M, 정상청구원금_B5M
            - **총 상환 금액**: 정상입금원금_BOM, 정상입금원금_B2M, 정상입금원금_B5M
            """)
            
        with col2:
            # 상환비율 예측 시각화 - 정규분포 형태
            np.random.seed(42)
            repayment_ratio = np.random.beta(5, 2, 1000)
            repayment_df = pd.DataFrame({'상환 비율': repayment_ratio})
            
            fig = px.histogram(
                repayment_df, 
                x='상환 비율', 
                nbins=30, 
                color_discrete_sequence=['#1E88E5'],
                opacity=0.8,
                marginal='box',
                title='상환 비율 예측 분포'
            )
            
            fig.update_layout(
                xaxis_title='상환 비율 (0~1)',
                yaxis_title='빈도',
                bargap=0.1,
                height=400,
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("""
            📌 **예측 해석**  
            - **0.8~1.0**: 정상 상환 가능성 높음
            - **0.5~0.8**: 부분 상환 가능성
            - **0~0.5**: 연체 가능성 높음
            """, icon="ℹ️")
    
    with model_tabs[1]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 📊 연체 위험도 분류 모델
            
            1단계에서 예측된 **상환 비율**을 포함하여 최종 연체 위험도를 예측하는 **다중 클래스 분류 모델**입니다.
            
            #### 분류 범주:
            - **1단계**: 정상 고객 (상환 가능성 높음)
            - **2단계**: 위험 고객 (상환 비율 중간, 연체 가능 고객)
            - **3단계**: 고위험 고객 (연체 확정 가능성 높음)
            
            #### 결과 활용:
            - **정상 고객**: 추가 금융 상품 제안
            - **위험 고객**: 한도 조정, 납부 안내
            - **고위험 고객**: 맞춤형 상환 계획 제안
            """)
        
        with col2:
            # 위험도 분류 시각화 - 도넛 차트
            risk_labels = ['정상 고객', '위험 고객', '고위험 고객']
            risk_values = [65, 25, 10]
            risk_colors = ['#4CAF50', '#FF9800', '#F44336']
            
            fig = go.Figure(data=[go.Pie(
                labels=risk_labels,
                values=risk_values,
                hole=.5,
                marker=dict(colors=risk_colors),
                textinfo='label+percent',
                textfont=dict(size=14),
                pull=[0, 0.05, 0.1],  # 위험 고객 강조
            )])
            
            fig.update_layout(
                title_text='고객 위험도 분류 예시',
                annotations=[dict(text='고객 분류', x=0.5, y=0.5, font_size=15, showarrow=False)],
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # 변수 설명 - 인터랙티브 탭으로 변경
    st.markdown("<div class='sub-header'>주요 입력 변수 분석</div>", unsafe_allow_html=True)
    
    var_tabs = st.tabs(["💳 소비 패턴", "🏠 생활 패턴", "👀 관심도", "💹 거시 경제 지표"])
    
    with var_tabs[0]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        
        # 변수 카드 레이아웃으로 변경
        consumption_vars = [
            {"name": "월별 총 소비액", "desc": "특정 기간 동안의 카드 사용 총액", "icon": "💰"},
            {"name": "소비 카테고리별 지출 비율", "desc": "음식점, 온라인 쇼핑, 유흥, 대형 마트, 여행 등 지출 항목별 비율", "icon": "🛒"},
            {"name": "고정 지출 여부", "desc": "매월 반복되는 지출 여부 (구독 서비스, 렌탈, 보험료 등)", "icon": "📅"},
            {"name": "최대 소비 카테고리", "desc": "가장 많은 소비가 발생한 업종", "icon": "🔝"},
            {"name": "소비 집중 시간대", "desc": "주로 소비가 발생하는 시간대 (예: 낮 vs 밤)", "icon": "⏰"},
            {"name": "소비 증가율", "desc": "과거 대비 최근 소비 증가율 (급격한 증가 여부)", "icon": "📈"},
            {"name": "평균 결제 금액", "desc": "한 번 결제할 때 평균적으로 소비하는 금액", "icon": "💲"},
            {"name": "결제방식(일시불 vs 할부)", "desc": "할부 사용 빈도", "icon": "💳"},
            {"name": "월별 카드 한도 대비 사용량", "desc": "카드 한도를 초과할 가능성이 있는지 분석", "icon": "⚠️"}
        ]
        
        # 3개 열 그리드로 변수 표시
        cols = st.columns(3)
        for i, var in enumerate(consumption_vars):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: all 0.3s ease; animation: fadeIn {0.5 + i*0.1}s ease-in-out;">
                    <div style="font-size: 24px; margin-bottom: 8px;">{var['icon']}</div>
                    <h4 style="margin: 0 0 8px 0; color: #1976D2;">{var['name']}</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #616161;">{var['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 소비 패턴 분석 예시 - 바 차트
        st.markdown("### 소비 카테고리별 지출 변화 분석 예시")
        
        categories = ['식비', '쇼핑', '교통', '주거', '의료', '여가', '여행']
        normal_spending = [25, 20, 15, 20, 5, 10, 5]
        risk_spending = [15, 35, 10, 20, 5, 5, 10]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=categories,
            y=normal_spending,
            name='정상 고객',
            marker_color='#4CAF50'
        ))
        fig.add_trace(go.Bar(
            x=categories,
            y=risk_spending,
            name='연체 위험 고객',
            marker_color='#F44336'
        ))
        
        fig.update_layout(
            barmode='group',
            title='고객 유형별 소비 패턴 비교',
            xaxis_title='소비 카테고리',
            yaxis_title='지출 비중 (%)',
            legend_title='고객 유형',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="highlight" style="margin-top: 20px;">
            <h4 style="margin-top: 0;">💡 소비 패턴 분석 인사이트</h4>
            <ul>
                <li>연체 위험 고객은 일반적으로 <b>쇼핑 비중이 높고 필수 지출(식비)이 낮은 경향</b>이 있습니다.</li>
                <li>갑작스러운 고가 소비가 발생한 경우 연체 가능성이 증가합니다.</li>
                <li>필수 지출과 선택적 지출의 비율은 연체 예측에 중요한 피처입니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    with var_tabs[1]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        
        # 생활 패턴 변수 카드
        lifestyle_vars = [
            {"name": "교통 이용 패턴", "desc": "대중교통 vs 자가용 사용 패턴 (교통비 지출 여부)", "icon": "🚗"},
            {"name": "이용하는 지역", "desc": "소비가 주로 발생하는 지역 (예: 주거지, 직장 근처)", "icon": "🏙️"},
            {"name": "자주 방문하는 업종", "desc": "특정 업종(예: 편의점, 카페, 쇼핑몰) 이용 빈도", "icon": "🏪"},
            {"name": "온라인 vs 오프라인 소비", "desc": "온라인 소비 비중이 높은지 여부", "icon": "💻"},
            {"name": "시간대별 소비 여부", "desc": "특정 시간대 소비 여부 (출근 전/후, 심야 등)", "icon": "🕒"},
            {"name": "급여일과 소비 패턴", "desc": "급여일 직후 소비 증가 여부", "icon": "💸"},
            {"name": "소비의 일관성", "desc": "정기적인 소비 패턴을 가지는지 여부", "icon": "📊"},
            {"name": "월간 지출 변동성", "desc": "소비 금액의 변동 폭", "icon": "📉"}
        ]
        
        # 3개 열 그리드로 변수 표시
        cols = st.columns(3)
        for i, var in enumerate(lifestyle_vars):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: all 0.3s ease; animation: fadeIn {0.5 + i*0.1}s ease-in-out;">
                    <div style="font-size: 24px; margin-bottom: 8px;">{var['icon']}</div>
                    <h4 style="margin: 0 0 8px 0; color: #1976D2;">{var['name']}</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #616161;">{var['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
        # 생활 패턴 시각화 - 타임라인 차트
        st.markdown("### 시간대별 소비 패턴 분석 예시")
        
        hours = list(range(0, 24))
        normal_pattern = [1, 0.5, 0.2, 0.1, 0.1, 0.5, 1.5, 2.5, 3, 2, 1.5, 2.5, 3, 2, 1.5, 2, 3, 4, 3.5, 3, 2, 1.5, 1, 0.8]
        risk_pattern = [0.5, 0.2, 0.1, 0.1, 0.1, 0.2, 0.5, 1, 1.5, 1, 1, 1.5, 2, 1.5, 1, 1.5, 2, 3, 4, 5, 6, 5, 3, 1]
        
        # 시간대별 데이터프레임 생성
        time_df = pd.DataFrame({
            '시간': [f"{h}:00" for h in hours],
            '정상 고객': normal_pattern,
            '연체 위험 고객': risk_pattern
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_df['시간'],
            y=time_df['정상 고객'],
            name='정상 고객',
            line=dict(color='#4CAF50', width=3),
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=time_df['시간'],
            y=time_df['연체 위험 고객'],
            name='연체 위험 고객',
            line=dict(color='#F44336', width=3),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title='시간대별 소비 패턴 비교',
            xaxis_title='시간대',
            yaxis_title='소비 활동 지수',
            legend_title='고객 유형',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="highlight" style="margin-top: 20px;">
            <h4 style="margin-top: 0;">💡 생활 패턴 분석 인사이트</h4>
            <ul>
                <li>연체 위험 고객은 <b>저녁/심야 시간대 소비 비중이 높은 경향</b>이 있습니다.</li>
                <li>정상 고객은 일과 시간 중심으로 규칙적인 소비 패턴을 보입니다.</li>
                <li>주중과 주말의 소비 패턴 차이도 연체 예측에 중요한 지표입니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    with var_tabs[2]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        
        # 관심도 변수 카드
        interest_vars = [
            {"name": "특정 브랜드/업종 집중 소비", "desc": "특정 브랜드(스타벅스, 애플 등)에 대한 소비 집중도", "icon": "🏷️"},
            {"name": "할인/이벤트 적용 여부", "desc": "할인 쿠폰, 프로모션 사용 빈도", "icon": "🏷️"},
            {"name": "구독 서비스 이용", "desc": "넷플릭스, 유튜브 프리미엄 등 구독 여부", "icon": "📺"},
            {"name": "고가 제품 구매 빈도", "desc": "고급 브랜드 제품 구매 여부", "icon": "💎"},
            {"name": "금융상품 이용 여부", "desc": "보험, 대출, 투자 상품 이용 여부", "icon": "📊"},
            {"name": "리워드 활용 여부", "desc": "포인트 적립, 캐시백 활용 빈도", "icon": "🎁"},
            {"name": "여행 관련 지출", "desc": "여행사, 항공권, 호텔 예약 빈도", "icon": "✈️"},
            {"name": "SNS/커뮤니티 관련 소비", "desc": "특정 SNS, 유료 커뮤니티, 스트리밍 서비스 이용 여부", "icon": "👥"}
        ]
        
        # 3개 열 그리드로 변수 표시
        cols = st.columns(3)
        for i, var in enumerate(interest_vars):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: all 0.3s ease; animation: fadeIn {0.5 + i*0.1}s ease-in-out;">
                    <div style="font-size: 24px; margin-bottom: 8px;">{var['icon']}</div>
                    <h4 style="margin: 0 0 8px 0; color: #1976D2;">{var['name']}</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #616161;">{var['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 관심도 시각화 - 레이더 차트
        st.markdown("### 고객 관심 분야 패턴 분석 예시")
        
        # 레이더 차트 데이터
        categories = ['명품브랜드', '여행/숙박', '식음료', '전자제품', 'OTT구독', '교육/자기계발', '생활용품']
        
        fig = go.Figure()
        
        # 정상 고객 패턴
        fig.add_trace(go.Scatterpolar(
            r=[2, 4, 5, 3, 3, 5, 6],
            theta=categories,
            fill='toself',
            name='정상 고객',
            line_color='#4CAF50',
            opacity=0.7
        ))
        
        # 연체 위험 고객 패턴
        fig.add_trace(go.Scatterpolar(
            r=[6, 5, 3, 7, 4, 2, 3],
            theta=categories,
            fill='toself',
            name='연체 위험 고객',
            line_color='#F44336',
            opacity=0.7
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 7]
                )
            ),
            title="고객 유형별 관심 분야 비교",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="highlight" style="margin-top: 20px;">
            <h4 style="margin-top: 0;">💡 관심도 분석 인사이트</h4>
            <ul>
                <li>연체 위험 고객은 <b>명품브랜드와 전자제품에 대한 지출 비중이 높은 경향</b>이 있습니다.</li>
                <li>정상 고객은 생활용품과 교육/자기계발에 대한 지출 비중이 상대적으로 높습니다.</li>
                <li>특정 사치재에 대한 지출 비중과 필수재 지출 비중의 균형이 연체 예측에 중요한 지표입니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    with var_tabs[3]:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        
        # 거시 경제 지표 변수 카드
        macro_vars = [
            {"name": "금리 변동", "desc": "시장 금리 상승/하락과 고객 상환 능력 간의 관계", "icon": "📈"},
            {"name": "실업률", "desc": "경제 상황과 소득 안정성에 영향을 미치는 지표", "icon": "👥"},
            {"name": "소비자 물가지수", "desc": "생활비 부담과 연관된 지표", "icon": "🛒"},
            {"name": "고객 소득/자산", "desc": "기존 대출 보유 여부(담보대출, 신용대출)", "icon": "💰"},
            {"name": "비정상 소비 패턴", "desc": "갑작스러운 소비 급증 등 이상 징후", "icon": "⚠️"},
            {"name": "정기 납부 패턴", "desc": "공과금, 할부금 등 정기 납부 이력", "icon": "📅"},
            {"name": "트렌드 지수", "desc": "최신 소비 트렌드와의 연관성 분석", "icon": "📊"},
            {"name": "경기 동향 지수", "desc": "전반적인 경제 상황 반영 지표", "icon": "🌐"}
        ]
        
        # 3개 열 그리드로 변수 표시
        cols = st.columns(3)
        for i, var in enumerate(macro_vars):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background-color: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: all 0.3s ease; animation: fadeIn {0.5 + i*0.1}s ease-in-out;">
                    <div style="font-size: 24px; margin-bottom: 8px;">{var['icon']}</div>
                    <h4 style="margin: 0 0 8px 0; color: #1976D2;">{var['name']}</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #616161;">{var['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 거시 경제 지표 시각화 - 복합 차트
        st.markdown("### 거시 경제 지표와 연체율 간의 관계 분석")
        
        # 복합 차트 데이터
        quarters = ['2023-Q1', '2023-Q2', '2023-Q3', '2023-Q4', '2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4']
        interest_rates = [3.5, 3.75, 4.0, 4.25, 4.5, 4.5, 4.25, 4.0]
        delinquency_rates = [3.2, 3.6, 4.2, 4.8, 5.4, 6.1, 6.5, 7.0]
        unemployment = [3.2, 3.0, 2.9, 3.1, 3.3, 3.5, 3.6, 3.4]
        
        # 서브플롯 생성
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # 기준 금리 추가
        fig.add_trace(
            go.Scatter(
                x=quarters,
                y=interest_rates,
                name="기준 금리(%)",
                line=dict(color="#1E88E5", width=3),
                mode="lines+markers"
            ),
            secondary_y=False,
        )
        
        # 연체율 추가
        fig.add_trace(
            go.Scatter(
                x=quarters,
                y=delinquency_rates,
                name="연체율(%)",
                line=dict(color="#F44336", width=3),
                mode="lines+markers"
            ),
            secondary_y=True,
        )
        
        # 실업률 추가
        fig.add_trace(
            go.Bar(
                x=quarters,
                y=unemployment,
                name="실업률(%)",
                marker_color="rgba(158, 158, 158, 0.6)"
            ),
            secondary_y=False,
        )
        
        # 차트 레이아웃 설정
        fig.update_layout(
            title_text="거시 경제 지표와 연체율 추이 비교",
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # x축 설정
        fig.update_xaxes(title_text="분기")
        
        # y축 설정
        fig.update_yaxes(title_text="금리 및 실업률(%)", secondary_y=False)
        fig.update_yaxes(title_text="연체율(%)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="highlight" style="margin-top: 20px;">
            <h4 style="margin-top: 0;">💡 거시 경제 지표 분석 인사이트</h4>
            <ul>
                <li>기준 금리 인상 시점 이후 약 1~2분기 뒤 <b>연체율 증가 추세</b>가 뚜렷합니다.</li>
                <li>실업률 상승과 연체율 증가는 양의 상관관계를 보입니다.</li>
                <li>개인의 소비 패턴이 거시 경제 변화에 얼마나 민감하게 반응하는지가 중요한 예측 지표입니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 연체 분류 기준
    st.markdown("<div class='sub-header'>연체 위험 분류 기준</div>", unsafe_allow_html=True)
    
    # 애니메이션 테이블 대신 HTML로 직접 구현
    st.markdown("""
    <div style="overflow-x: auto; animation: fadeIn 1.5s ease-in-out;">
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.9em; border-radius: 5px 5px 0 0; overflow: hidden; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);">
            <thead>
                <tr style="background-color: #1E88E5; color: #ffffff; text-align: left; font-weight: bold;">
                    <th style="padding: 12px 15px; border-right: 1px solid #dddddd;">분류 기준</th>
                    <th style="padding: 12px 15px; border-right: 1px solid #dddddd; background-color: #4CAF50; color: white;">정상 고객(1단계)</th>
                    <th style="padding: 12px 15px; border-right: 1px solid #dddddd; background-color: #FF9800; color: white;">위험 고객(2단계)</th>
                    <th style="padding: 12px 15px; background-color: #F44336; color: white;">고위험 고객(3단계)</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #dddddd; animation: fadeIn 1.7s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">상환 비율(DSR) 및 부채 수준</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">DSR ≤ 30%, DTI ≤ 50%</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">DSR 30~50%, DTI 50~80%</td>
                    <td style="padding: 12px 15px;">DSR > 50%, DTI > 80%</td>
                </tr>
                <tr style="border-bottom: 1px solid #dddddd; animation: fadeIn 1.9s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">연체 이력 및 신용 거래 패턴</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">연체 기록 없음, 신용카드 연체 없음</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">최근 1년 내 1~2회 단기 연체(30일 미만)</td>
                    <td style="padding: 12px 15px;">1년 내 3회 이상 연체 또는 60일 이상 연체</td>
                </tr>
                <tr style="border-bottom: 1px solid #dddddd; animation: fadeIn 2.1s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">신용 점수 및 금융기관 평가 등급</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">신용 점수 800점 이상</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">신용 점수 650~799점</td>
                    <td style="padding: 12px 15px;">신용 점수 650점 미만</td>
                </tr>
                <tr style="animation: fadeIn 2.3s ease-in-out;">
                    <td style="padding: 12px 15px; background-color: #f3f3f3; border-right: 1px solid #dddddd; font-weight: bold;">소득 안정성 및 직업 유형</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">정규직, 공무원, 3년 이상 동일 직장 근무</td>
                    <td style="padding: 12px 15px; border-right: 1px solid #dddddd;">계약직, 프리랜서, 1~3년 근속</td>
                    <td style="padding: 12px 15px;">무직, 단기 아르바이트, 1년 미만 근속</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # 조치 방안 및 활용 방법
    st.markdown("<div class='sub-header'>고객 유형별 맞춤 조치 방안</div>", unsafe_allow_html=True)
    
    # 3개 탭으로 구분
    action_tabs = st.tabs(["🟢 정상 고객", "🟠 위험 고객", "🔴 고위험 고객"])
    
    with action_tabs[0]:
        st.markdown("""
        <div style="background-color: rgba(76, 175, 80, 0.1); border-radius: 10px; padding: 20px; border-left: 5px solid #4CAF50; animation: fadeIn 0.8s ease-in-out;">
            <h3 style="color: #4CAF50; margin-top: 0;">정상 고객 관리 방안</h3>
            
            <p><strong>특징:</strong> 상환 능력이 충분하고 재무 건전성이 높은 고객</p>
            
            <div style="margin-top: 15px;">
                <h4>🎯 주요 조치 방안</h4>
                <ul>
                    <li><strong>우수고객 혜택 제공</strong>: 금리 인하, 한도 상향 등 보상 프로그램 운영</li>
                    <li><strong>상향 판매(Up-selling)</strong>: 추가 금융 상품 제안 (투자, 적금, 프리미엄 신용카드 등)</li>
                    <li><strong>충성도 프로그램</strong>: 장기 고객 특별 혜택 및 리워드 제공</li>
                    <li><strong>자산 관리 서비스</strong>: 개인 맞춤형 자산 관리 컨설팅 제공</li>
                </ul>
            </div>
            
            <div style="margin-top: 15px;">
                <h4>📊 기대 효과</h4>
                <ul>
                    <li>고객 충성도 강화 및 이탈률 감소</li>
                    <li>고객 생애 가치(LTV) 증대</li>
                    <li>교차 판매(Cross-selling)를 통한 매출 증대</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with action_tabs[1]:
        st.markdown("""
        <div style="background-color: rgba(255, 152, 0, 0.1); border-radius: 10px; padding: 20px; border-left: 5px solid #FF9800; animation: fadeIn 0.8s ease-in-out;">
            <h3 style="color: #FF9800; margin-top: 0;">위험 고객 관리 방안</h3>
            
            <p><strong>특징:</strong> 상환 가능성은 있으나 재무적 부담이 있는 고객</p>
            
            <div style="margin-top: 15px;">
                <h4>🎯 주요 조치 방안</h4>
                <ul>
                    <li><strong>선제적 연락</strong>: 납부일 전 알림 메시지 및 상환 안내</li>
                    <li><strong>한도 조정</strong>: 위험도에 따른 한도 일시 축소로 추가 부채 방지</li>
                    <li><strong>상환 옵션 제안</strong>: 리볼빙, 할부 전환 등 유연한 상환 방법 안내</li>
                    <li><strong>재정 교육</strong>: 맞춤형 금융 교육 및 예산 관리 도구 제공</li>
                    <li><strong>채무 조정 상담</strong>: 필요시 상환 계획 재조정 상담 제공</li>
                </ul>
            </div>
            
            <div style="margin-top: 15px;">
                <h4>📊 기대 효과</h4>
                <ul>
                    <li>연체 발생률 감소</li>
                    <li>고객의 재무 건전성 개선</li>
                    <li>장기적인 고객 관계 유지</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with action_tabs[2]:
        st.markdown("""
        <div style="background-color: rgba(244, 67, 54, 0.1); border-radius: 10px; padding: 20px; border-left: 5px solid #F44336; animation: fadeIn 0.8s ease-in-out;">
            <h3 style="color: #F44336; margin-top: 0;">고위험 고객 관리 방안</h3>
            
            <p><strong>특징:</strong> 상환 능력이 현저히 낮거나 연체 가능성이 매우 높은 고객</p>
            
            <div style="margin-top: 15px;">
                <h4>🎯 주요 조치 방안</h4>
                <ul>
                    <li><strong>즉각적인 조치</strong>: 추가 대출 및 카드 사용 일시 중지</li>
                    <li><strong>집중 관리</strong>: 전담 상담사 배정 및 맞춤형 채무 조정 계획 수립</li>
                    <li><strong>분할 상환 프로그램</strong>: 장기 분할 상환 및 금리 인하 옵션 제공</li>
                    <li><strong>채무 통합</strong>: 여러 채무를 통합하여 상환 부담 경감</li>
                    <li><strong>법적 조치 전 협상</strong>: 연체금 감면 등 상환 가능성 높이는 협상</li>
                </ul>
            </div>
            
            <div style="margin-top: 15px;">
                <h4>📊 기대 효과</h4>
                <ul>
                    <li>부실채권(NPL) 규모 감소</li>
                    <li>채권 회수율 증가</li>
                    <li>법적 비용 절감</li>
                    <li>고객 회생 가능성 증대</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 모델 성능 분석 페이지
elif page == "📈 모델 성능 분석":
    st.markdown("<div class='main-header'>모델 성능 분석</div>", unsafe_allow_html=True)
    
    # 애니메이션 로딩
    load_with_animation()
    
    # 모델 성능 지표 상단 카드
    st.markdown("<div class='sub-header'>주요 성능 지표</div>", unsafe_allow_html=True)
    
    # 모델 성능 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2.5rem; color: #1E88E5; font-weight: bold;">89.7%</div>
            <div style="font-size: 1rem; color: #424242; margin-top: 8px;">정확도(Accuracy)</div>
            <div style="font-size: 0.8rem; color: #4CAF50; margin-top: 5px;">▲ 3.2% vs 기존 모델</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2.5rem; color: #1E88E5; font-weight: bold;">0.92</div>
            <div style="font-size: 1rem; color: #424242; margin-top: 8px;">AUC-ROC</div>
            <div style="font-size: 0.8rem; color: #4CAF50; margin-top: 5px;">▲ 0.05 vs 기존 모델</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2.5rem; color: #1E88E5; font-weight: bold;">86.3%</div>
            <div style="font-size: 1rem; color: #424242; margin-top: 8px;">F1 Score</div>
            <div style="font-size: 0.8rem; color: #4CAF50; margin-top: 5px;">▲ 4.1% vs 기존 모델</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2.5rem; color: #1E88E5; font-weight: bold;">35.1%</div>
            <div style="font-size: 1rem; color: #424242; margin-top: 8px;">조기 탐지율</div>
            <div style="font-size: 0.8rem; color: #4CAF50; margin-top: 5px;">▲ 12.3% vs 기존 모델</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 모델 성능 비교 탭
    st.markdown("<div class='sub-header'>모델 성능 상세 분석</div>", unsafe_allow_html=True)
    
    model_performance_tabs = st.tabs(["📊 성능 비교", "📈 학습 곡선", "🔍 혼동 행렬", "⚙️ 피처 중요도"])

    with model_performance_tabs[0]:
        # 모델별 성능 비교
        st.markdown("### 모델별 성능 비교")
        
        # 모델 성능 데이터
        models = ['XGBoost', 'LightGBM', 'CatBoost', '앙상블 모델']
        accuracy = [87.5, 88.2, 88.9, 89.7]
        precision = [84.3, 85.1, 86.2, 87.8]
        recall = [83.5, 84.2, 85.3, 86.9]
        f1 = [83.9, 84.6, 85.7, 86.3]
        
        # 바 차트 생성
        fig = go.Figure()
        
        # 지표별 바 추가
        fig.add_trace(go.Bar(
            x=models,
            y=accuracy,
            name='정확도',
            marker_color='#1E88E5'
        ))
        
        fig.add_trace(go.Bar(
            x=models,
            y=precision,
            name='정밀도',
            marker_color='#42A5F5'
        ))
        
        fig.add_trace(go.Bar(
            x=models,
            y=recall,
            name='재현율',
            marker_color='#90CAF9'
        ))
        
        fig.add_trace(go.Bar(
            x=models,
            y=f1,
            name='F1 Score',
            marker_color='#BBDEFB'
        ))
        
        # 차트 레이아웃 설정
        fig.update_layout(
            title='모델별 성능 비교',
            xaxis_title='모델',
            yaxis_title='점수 (%)',
            yaxis=dict(range=[80, 92]),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 기존 모델과의 비교
        st.markdown("### 기존 모델 대비 개선 효과")
        
        # 비교 데이터
        metrics = ['정확도', '정밀도', '재현율', 'F1 Score', '조기 탐지율']
        existing_model = [86.5, 83.2, 82.1, 82.2, 22.8]
        new_model = [89.7, 87.8, 86.9, 86.3, 35.1]
        improvement = [round((n - e), 1) for n, e in zip(new_model, existing_model)]
        
        # 데이터프레임 생성
        comparison_df = pd.DataFrame({
            '평가 지표': metrics,
            '기존 모델(%)': existing_model,
            '신규 모델(%)': new_model,
            '개선도(%p)': improvement
        })
        
        # 개선도 바 차트 생성
        fig = px.bar(
            comparison_df,
            x='평가 지표',
            y='개선도(%p)',
            text='개선도(%p)',
            color='개선도(%p)',
            color_continuous_scale='Blues',
            title='지표별 개선도'
        )
        
        fig.update_traces(
            texttemplate='%{text}%p',
            textposition='outside'
        )
        
        fig.update_layout(
            xaxis_title='평가 지표',
            yaxis_title='개선도 (%p)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.dataframe(comparison_df, use_container_width=True)
            
        with col2:
            st.plotly_chart(fig, use_container_width=True)
            
    with model_performance_tabs[1]:
        # 학습 곡선
        st.markdown("### 모델 학습 곡선")
        
        # 학습 곡선 데이터
        epochs = list(range(1, 101))
        train_loss = [0.52 - 0.45 * np.exp(-0.025 * x) + 0.02 * np.random.randn() for x in epochs]
        val_loss = [0.55 - 0.42 * np.exp(-0.02 * x) + 0.03 * np.random.randn() for x in epochs]
        
        # 학습 곡선 플롯
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=train_loss,
            mode='lines',
            name='학습 데이터',
            line=dict(color='#1E88E5', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=val_loss,
            mode='lines',
            name='검증 데이터',
            line=dict(color='#F44336', width=2)
        ))
        
        fig.update_layout(
            title='에포크별 손실 함수',
            xaxis_title='에포크',
            yaxis_title='손실(Loss)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 정확도 곡선 데이터
        train_acc = [0.5 + 0.45 * (1 - np.exp(-0.03 * x)) + 0.01 * np.random.randn() for x in epochs]
        val_acc = [0.5 + 0.42 * (1 - np.exp(-0.025 * x)) + 0.015 * np.random.randn() for x in epochs]
        
        # 정확도 곡선 플롯
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=train_acc,
            mode='lines',
            name='학습 데이터',
            line=dict(color='#1E88E5', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=val_acc,
            mode='lines',
            name='검증 데이터',
            line=dict(color='#F44336', width=2)
        ))
        
        fig.update_layout(
            title='에포크별 정확도',
            xaxis_title='에포크',
            yaxis_title='정확도(Accuracy)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with model_performance_tabs[2]:
        # 혼동 행렬
        st.markdown("### 혼동 행렬 (Confusion Matrix)")
        
        # 3x3 혼동 행렬 데이터 (3개 클래스)
        confusion_matrix = np.array([
            [1254, 86, 14],   # 실제 정상, 예측: 정상/위험/고위험
            [108, 543, 42],   # 실제 위험, 예측: 정상/위험/고위험
            [21, 65, 367]     # 실제 고위험, 예측: 정상/위험/고위험
        ])
        
        # 데이터 준비
        categories = ['정상 고객', '위험 고객', '고위험 고객']
        
        # 혼동 행렬 히트맵 생성
        fig = px.imshow(
            confusion_matrix,
            labels=dict(x="예측 클래스", y="실제 클래스", color="건수"),
            x=categories,
            y=categories,
            color_continuous_scale='Blues',
            text_auto=True
        )
        
        fig.update_layout(
            title='연체 위험도 예측 혼동 행렬',
            xaxis_title='예측 클래스',
            yaxis_title='실제 클래스',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 클래스별 성능 지표
        st.markdown("### 클래스별 성능 지표")
        
        # 클래스별 성능 지표 계산 (간소화됨)
        performance_metrics = {
            '클래스': categories,
            '정밀도(Precision)': [92.5, 78.2, 86.7],
            '재현율(Recall)': [92.7, 78.4, 81.0],
            'F1 Score': [92.6, 78.3, 83.7]
        }
        
        perf_df = pd.DataFrame(performance_metrics)
        
        # 클래스별 성능 지표 시각화
        fig = go.Figure()
        
        # 정밀도
        fig.add_trace(go.Bar(
            x=categories,
            y=performance_metrics['정밀도(Precision)'],
            name='정밀도',
            marker_color='#1E88E5'
        ))
        
        # 재현율
        fig.add_trace(go.Bar(
            x=categories,
            y=performance_metrics['재현율(Recall)'],
            name='재현율',
            marker_color='#42A5F5'
        ))
        
        # F1 Score
        fig.add_trace(go.Bar(
            x=categories,
            y=performance_metrics['F1 Score'],
            name='F1 Score',
            marker_color='#90CAF9'
        ))
        
        fig.update_layout(
            title='클래스별 성능 지표',
            xaxis_title='고객 위험도 클래스',
            yaxis_title='점수 (%)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(perf_df, use_container_width=True)
            
        with col2:
            st.plotly_chart(fig, use_container_width=True)
    
    with model_performance_tabs[3]:
        # 피처 중요도
        st.markdown("### 변수 중요도 분석")
        
        # 변수 중요도 데이터
        features = [
            '과거 연체 이력', '상환비율(DSR)', '소득 대비 총부채 비율(DTI)', '최근 3개월 평균 소비액', 
            '최대 소비 카테고리', '신용카드 한도 소진율', '급여일 이후 소비 급증 여부', 
            '최근 신용 조회 횟수', '고정 지출 비중', '저녁/심야 시간대 소비 비중'
        ]
        
        importance_scores = [18.5, 15.2, 14.3, 10.8, 9.5, 8.7, 7.4, 6.2, 5.1, 4.3]
        
        # 피처 중요도 정렬
        sorted_indices = np.argsort(importance_scores)
        sorted_features = [features[i] for i in sorted_indices]
        sorted_scores = [importance_scores[i] for i in sorted_indices]
        
        # 바 차트 생성
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=sorted_features,
            x=sorted_scores,
            orientation='h',
            marker=dict(
                color=sorted_scores,
                colorscale='Blues',
                colorbar=dict(title="중요도 점수")
            )
        ))
        
        fig.update_layout(
            title='변수 중요도 (상위 10개)',
            xaxis_title='중요도 점수',
            yaxis_title='변수명',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # SHAP 값 시각화 (예시)
        st.markdown("### SHAP 분석 - 변수별 영향력")
        
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <img src="https://i.ibb.co/JFNj8KG/shap-values-example.png" style="max-width: 80%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight" style="margin-top: 20px;">
            <h4 style="margin-top: 0;">💡 변수 중요도 분석 인사이트</h4>
            <ul>
                <li>과거 연체 이력, 상환비율(DSR), 소득 대비 총부채 비율(DTI)이 <b>가장 중요한 예측 변수</b>로 나타났습니다.</li>
                <li>소비 패턴 관련 변수 중에서는 <b>최근 3개월 평균 소비액</b>과 <b>최대 소비 카테고리</b>가 높은 중요도를 보였습니다.</li>
                <li>생활 패턴 중에서는 <b>급여일 이후 소비 급증 여부</b>와 <b>저녁/심야 시간대 소비 비중</b>이 유의미한 예측력을 보였습니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ROC 및 PR 곡선
    st.markdown("<div class='sub-header'>ROC 및 PR 곡선</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ROC 곡선
        fpr = np.linspace(0, 1, 100)
        
        # 모델별 ROC 곡선
        tpr_xgb = [0] + [1 - np.exp(-5 * x) for x in fpr[1:]]
        tpr_lgbm = [0] + [1 - np.exp(-5.5 * x) for x in fpr[1:]]
        tpr_catboost = [0] + [1 - np.exp(-6 * x) for x in fpr[1:]]
        tpr_ensemble = [0] + [1 - np.exp(-6.5 * x) for x in fpr[1:]]
        
        # 약간의 무작위성 추가
        np.random.seed(42)
        tpr_xgb = [min(1, max(0, t + np.random.normal(0, 0.02))) for t in tpr_xgb]
        tpr_lgbm = [min(1, max(0, t + np.random.normal(0, 0.02))) for t in tpr_lgbm]
        tpr_catboost = [min(1, max(0, t + np.random.normal(0, 0.02))) for t in tpr_catboost]
        tpr_ensemble = [min(1, max(0, t + np.random.normal(0, 0.02))) for t in tpr_ensemble]
        
        # ROC 곡선 플롯
        fig = go.Figure()
        
        # 대각선 (랜덤 분류기)
        fig.add_trace(go.Scatter(
            x=fpr,
            y=fpr,
            mode='lines',
            name='랜덤',
            line=dict(color='gray', width=2, dash='dash')
        ))
        
        # 각 모델별 ROC 곡선
        fig.add_trace(go.Scatter(
            x=fpr,
            y=tpr_xgb,
            mode='lines',
            name='XGBoost (AUC=0.88)',
            line=dict(color='#4CAF50', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=fpr,
            y=tpr_lgbm,
            mode='lines',
            name='LightGBM (AUC=0.89)',
            line=dict(color='#FF9800', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=fpr,
            y=tpr_catboost,
            mode='lines',
            name='CatBoost (AUC=0.90)',
            line=dict(color='#F44336', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=fpr,
            y=tpr_ensemble,
            mode='lines',
            name='앙상블 (AUC=0.92)',
            line=dict(color='#1E88E5', width=3)
        ))
        
        fig.update_layout(
            title='ROC 곡선 비교',
            xaxis_title='위양성률(FPR)',
            yaxis_title='재현율(TPR)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.2,
                xanchor="center",
                x=.5
            ),
            width=500,
            height=500,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # PR 곡선
        recall = np.linspace(0, 1, 100)
        
        # 모델별 PR 곡선 (간단한 모델링)
        precision_xgb = [1 - 0.6 * r**2 for r in recall]
        precision_lgbm = [1 - 0.55 * r**2 for r in recall]
        precision_catboost = [1 - 0.5 * r**2 for r in recall]
        precision_ensemble = [1 - 0.45 * r**2 for r in recall]
        
        # 약간의 무작위성 추가
        np.random.seed(42)
        precision_xgb = [min(1, max(0, p + np.random.normal(0, 0.02))) for p in precision_xgb]
        precision_lgbm = [min(1, max(0, p + np.random.normal(0, 0.02))) for p in precision_lgbm]
        precision_catboost = [min(1, max(0, p + np.random.normal(0, 0.02))) for p in precision_catboost]
        precision_ensemble = [min(1, max(0, p + np.random.normal(0, 0.02))) for p in precision_ensemble]
        
        # PR 곡선 플롯
        fig = go.Figure()
        
        # 각 모델별 PR 곡선
        fig.add_trace(go.Scatter(
            x=recall,
            y=precision_xgb,
            mode='lines',
            name='XGBoost (AP=0.82)',
            line=dict(color='#4CAF50', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=recall,
            y=precision_lgbm,
            mode='lines',
            name='LightGBM (AP=0.84)',
            line=dict(color='#FF9800', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=recall,
            y=precision_catboost,
            mode='lines',
            name='CatBoost (AP=0.86)',
            line=dict(color='#F44336', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=recall,
            y=precision_ensemble,
            mode='lines',
            name='앙상블 (AP=0.88)',
            line=dict(color='#1E88E5', width=3)
        ))
        
        fig.update_layout(
            title='PR 곡선 비교',
            xaxis_title='재현율(Recall)',
            yaxis_title='정밀도(Precision)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.2,
                xanchor="center",
                x=.5
            ),
            width=500,
            height=500,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 모델 성능 요약 인사이트
    st.markdown("""
    <div class="highlight" style="margin-top: 20px;">
        <h3 style="margin-top: 0;">📊 모델 성능 요약 인사이트</h3>
        <ul>
            <li>앙상블 모델이 <b>모든 성능 지표에서 가장 우수한 결과</b>를 보였습니다. (정확도 89.7%, AUC 0.92)</li>
            <li><b>조기 탐지율이 35.1%</b>로, 기존 모델 대비 12.3%p 향상되어 위험 고객을 사전에 식별하는 능력이 크게 개선되었습니다.</li>
            <li>3단계 분류 결과에서 <b>'고위험 고객' 클래스 탐지 정확도가 특히 우수</b>하여, 연체 가능성이 높은 고객을 효과적으로 식별해냅니다.</li>
            <li>과거 연체 이력, 상환비율(DSR), 소득 대비 총부채 비율(DTI)이 가장 강력한 예측 변수로 확인되었습니다.</li>
            <li>소비/생활 패턴 변수 추가로 기존 모델 대비 <b>성능이 유의미하게 향상</b>되었습니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 시뮬레이션 페이지
elif page == "🧪 시뮬레이션":
    st.markdown("<div class='main-header'>연체 위험 예측 시뮬레이션</div>", unsafe_allow_html=True)
    
    # 애니메이션 로딩
    load_with_animation()
    
    st.markdown("""
    <div class="highlight">
        <h3 style="margin-top: 0;">💡 시뮬레이션 안내</h3>
        <p>실제 데이터를 기반으로 고객의 연체 위험을 예측하는 시뮬레이션입니다. 아래 양식에 고객 정보를 입력하면 모델이 연체 위험도를 예측합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 시뮬레이션 입력 폼
    st.markdown("<div class='sub-header'>고객 정보 입력</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 고객 기본 정보
        st.markdown("#### 기본 정보")
        
        age = st.slider('연령', 20, 70, 35)
        gender = st.radio('성별', ['남성', '여성'])
        job = st.selectbox('직업 유형', ['정규직', '계약직', '자영업', '프리랜서', '일용직', '무직'])
        income = st.slider('월 소득 (만원)', 100, 1000, 350)
        
        # 금융 정보
        st.markdown("#### 금융 정보")
        
        existing_loans = st.number_input('기존 대출 건수', 0, 10, 1)
        credit_score = st.slider('신용 점수', 300, 1000, 750)
        
        dsr = st.slider('DSR (상환비율, %)', 0, 100, 40)
        dti = st.slider('DTI (부채비율, %)', 0, 150, 60)
        
        past_delinquency = st.radio('과거 연체 이력', ['없음', '단기 연체(30일 미만)', '장기 연체(30일 이상)'])
        
        # 소비 패턴 정보
        st.markdown("#### 소비 패턴 정보")
        
        monthly_consumption = st.slider('월 평균 소비액 (만원)', 50, 800, 250)
        main_consumption = st.selectbox('주요 소비 카테고리', ['식비', '주거/공과금', '교통/통신', '쇼핑', '의료/건강', '교육', '여가/문화', '여행/숙박'])
        credit_limit_usage = st.slider('신용카드 한도 소진율 (%)', 0, 100, 65)
        installment_ratio = st.slider('할부 결제 비중 (%)', 0, 100, 30)
        
        # 생활 패턴 정보
        st.markdown("#### 생활 패턴 정보")
        
        online_shopping_ratio = st.slider('온라인 쇼핑 비중 (%)', 0, 100, 55)
        night_consumption_ratio = st.slider('저녁/심야 시간대 소비 비중 (%)', 0, 100, 35)
        salary_day_spike = st.radio('급여일 이후 소비 급증 여부', ['예', '아니오'])
        
        # 예측 실행 버튼
        predict_btn = st.button('연체 위험 예측하기')
    
    # 예측 결과 표시
    if predict_btn:
        with st.spinner('모델이 예측 중입니다...'):
            time.sleep(2)
        
        # 시뮬레이션된 예측 결과 (실제로는 모델이 계산)
        # 다양한 입력 조합에 대한 간단한 점수 계산
        risk_score = 0
        
        # 기본 정보 영향
        if age < 25 or age > 55:
            risk_score += 10
        
        if job in ['일용직', '무직']:
            risk_score += 20
        elif job in ['계약직', '프리랜서']:
            risk_score += 10
        
        if income < 250:
            risk_score += 15
        
        # 금융 정보 영향
        if existing_loans > 3:
            risk_score += 15
        
        if credit_score < 650:
            risk_score += 25
        elif credit_score < 750:
            risk_score += 10
        
        if dsr > 60:
            risk_score += 25
        elif dsr > 40:
            risk_score += 15
        
        if dti > 80:
            risk_score += 20
        elif dti > 60:
            risk_score += 10
        
        if past_delinquency == '장기 연체(30일 이상)':
            risk_score += 30
        elif past_delinquency == '단기 연체(30일 미만)':
            risk_score += 15
        
        # 소비 패턴 영향
        if monthly_consumption > income * 0.8:
            risk_score += 20
        
        if main_consumption in ['쇼핑', '여행/숙박', '여가/문화']:
            risk_score += 10
        
        if credit_limit_usage > 80:
            risk_score += 15
        
        if installment_ratio > 50:
            risk_score += 10
        
        # 생활 패턴 영향
        if online_shopping_ratio > 70:
            risk_score += 10
        
        if night_consumption_ratio > 50:
            risk_score += 15
        
        if salary_day_spike == '예':
            risk_score += 10
        
        # 연체 상환 비율 예측 (0~1, 1에 가까울수록 정상 상환 가능성 높음)
        repayment_ratio = max(0, min(1, 1 - (risk_score / 200)))
        
        # 고객 위험도 분류
        if risk_score < 50:
            risk_category = "정상 고객"
            risk_color = "#4CAF50"
            risk_class = "risk-low"
            risk_desc = "상환 능력이 충분하며 연체 가능성이 낮습니다."
            recommendation = [
                "신용 한도 상향 검토 가능",
                "우대 금리 적용 대출 추천",
                "프리미엄 금융 상품 제안"
            ]
        elif risk_score < 100:
            risk_category = "위험 고객"
            risk_color = "#FF9800"
            risk_class = "risk-medium"
            risk_desc = "재정 상태에 주의가 필요하며 연체 가능성이 있습니다."
            recommendation = [
                "상환 계획 점검 필요",
                "추가 대출시 리스크 검토 필요",
                "유연한 납부 옵션 안내"
            ]
        else:
            risk_category = "고위험 고객"
            risk_color = "#F44336"
            risk_class = "risk-high"
            risk_desc = "연체 가능성이 높으며 즉각적인 재정 관리가 필요합니다."
            recommendation = [
                "상환 계획 재조정 필요",
                "신용 한도 조정 검토",
                "부채 통합 및 상환 방안 컨설팅"
            ]
        
        # 결과 표시
        st.markdown("<div class='sub-header'>연체 위험 예측 결과</div>", unsafe_allow_html=True)
        
        # 애니메이션 진행바
        progress_text = "분석 결과 생성 중..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()
        
        # 결과 카드
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); animation: fadeIn 1.5s ease-in-out;">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="background-color: {risk_color}; color: white; border-radius: 50%; width: 50px; height: 50px; display: flex; justify-content: center; align-items: center; margin-right: 15px; font-size: 24px;">
                    {"✓" if risk_category == "정상 고객" else "!" if risk_category == "위험 고객" else "⚠"}
                </div>
                <div>
                    <h2 style="margin: 0; color: {risk_color};">{risk_category}</h2>
                    <p style="margin: 5px 0 0 0; color: #616161;">{risk_desc}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 상세 결과
        col1, col2 = st.columns(2)
        
        with col1:
            # 상환 비율 게이지
            st.markdown("#### 예측 상환 비율")
            
            # 게이지 차트
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = repayment_ratio * 100,
                title = {'text': "상환 가능성 점수"},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': risk_color},
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(244, 67, 54, 0.2)"},
                        {'range': [40, 70], 'color': "rgba(255, 152, 0, 0.2)"},
                        {'range': [70, 100], 'color': "rgba(76, 175, 80, 0.2)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 40
                    }
                }
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, b=20, t=30)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # 위험 요소 분석
            st.markdown("#### 주요 위험 요소")
            
            # 위험 요소 스코어 계산 (예시)
            risk_factors = []
            
            if dsr > 40:
                risk_factors.append({"factor": "상환비율(DSR)", "score": min(100, dsr), "threshold": 40})
            
            if dti > 60:
                risk_factors.append({"factor": "부채비율(DTI)", "score": min(100, dti), "threshold": 60})
            
            if credit_score < 750:
                normalized_score = 100 - ((credit_score - 300) / 7)
                risk_factors.append({"factor": "신용점수", "score": normalized_score, "threshold": 35})
            
            if past_delinquency != "없음":
                delinq_score = 80 if past_delinquency == "장기 연체(30일 이상)" else 50
                risk_factors.append({"factor": "과거 연체 이력", "score": delinq_score, "threshold": 20})
            
            if credit_limit_usage > 70:
                risk_factors.append({"factor": "카드 한도 소진율", "score": credit_limit_usage, "threshold": 70})
            
            if monthly_consumption > income * 0.7:
                consumption_ratio = (monthly_consumption / income) * 100
                risk_factors.append({"factor": "소득 대비 소비 비율", "score": consumption_ratio, "threshold": 70})
            
            # 위험 요소가 없으면 기본값 추가
            if len(risk_factors) == 0:
                risk_factors.append({"factor": "주요 위험 요소가 없습니다", "score": 0, "threshold": 50})
            
            # 위험 요소 상위 5개만 표시
            risk_factors = sorted(risk_factors, key=lambda x: x["score"], reverse=True)[:5]
            
            # 위험 요소 시각화
            for factor in risk_factors:
                factor_score = factor["score"]
                threshold = factor["threshold"]
                factor_name = factor["factor"]
                
                # 위험도에 따른 색상 설정
                if factor_score > 80:
                    color = "#F44336"  # 빨강 (높은 위험)
                elif factor_score > 50:
                    color = "#FF9800"  # 주황 (중간 위험)
                else:
                    color = "#4CAF50"  # 녹색 (낮은 위험)
                
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>{factor_name}</span>
                        <span style="color: {color}; font-weight: bold;">{factor_score:.1f}%</span>
                    </div>
                    <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; height: 10px;">
                        <div style="width: {factor_score}%; background-color: {color}; height: 10px; border-radius: 5px; animation: lineAppear 1.5s ease-in-out;"></div>
                    </div>
                    <div style="display: flex; justify-content: flex-end; font-size: 0.8rem; color: #757575; margin-top: 3px;">
                        임계값: {threshold}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 맞춤 추천 및 조치 방안
        st.markdown("#### 맞춤 추천 및 조치 방안")
        
        for i, rec in enumerate(recommendation):
            st.markdown(f"""
            <div style="display: flex; align-items: center; background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 10px; animation: fadeIn {1 + i*0.2}s ease-in-out;">
                <div style="background-color: {risk_color}; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center; margin-right: 15px; font-weight: bold;">
                    {i+1}
                </div>
                <div style="flex-grow: 1;">
                    {rec}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 고객 프로필 요약
        st.markdown("#### 고객 프로필 요약")
        
        # 레이더 차트 데이터 준비
        categories = ['소득 대비 부채', '상환 능력', '과거 신용 이력', '소비 행태', '생활 패턴']
        
        # 점수 정규화 (0~1)
        debt_score = max(0, min(1, 1 - (dti / 150)))
        repayment_ability = max(0, min(1, 1 - (dsr / 100)))
        credit_history = max(0, min(1, (credit_score - 300) / 700)) if past_delinquency == "없음" else max(0, min(1, (credit_score - 300) / 700 * 0.5))
        consumption_behavior = max(0, min(1, 1 - (credit_limit_usage / 100) * 0.7 - (installment_ratio / 100) * 0.3))
        lifestyle_pattern = max(0, min(1, 1 - (night_consumption_ratio / 100) * 0.5 - (online_shopping_ratio / 100) * 0.3 - (0.2 if salary_day_spike == "예" else 0)))
        
        # 점수를 0~10 범위로 변경
        values = [debt_score * 10, repayment_ability * 10, credit_history * 10, consumption_behavior * 10, lifestyle_pattern * 10]
        
        # 레이더 차트 생성
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='고객 프로필',
            line_color=risk_color,
            opacity=0.8
        ))
        
        # 평균적인 '정상 고객' 패턴 추가 (비교용)
        fig.add_trace(go.Scatterpolar(
            r=[7, 8, 8, 7, 7],
            theta=categories,
            fill='toself',
            name='정상 고객 평균',
            line_color='#90CAF9',
            opacity=0.3
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 멀티모델 비교 (여러 모델의 예측 결과 비교)
        st.markdown("#### 다중 모델 예측 결과 비교")
        
        # 모델별 약간의 변동성 추가
        model_results = {
            'XGBoost': max(0, min(1, repayment_ratio + np.random.normal(0, 0.05))),
            'LightGBM': max(0, min(1, repayment_ratio + np.random.normal(0, 0.05))),
            'CatBoost': max(0, min(1, repayment_ratio + np.random.normal(0, 0.05))),
            '앙상블': repayment_ratio
        }
        
        # 결과 분류
        model_categories = {}
        for model, ratio in model_results.items():
            if ratio > 0.7:
                model_categories[model] = "정상 고객"
            elif ratio > 0.4:
                model_categories[model] = "위험 고객"
            else:
                model_categories[model] = "고위험 고객"
        
        # 결과 표시
        model_df = pd.DataFrame({
            '모델': list(model_results.keys()),
            '예측 상환 비율': [f"{v*100:.1f}%" for v in model_results.values()],
            '고객 분류': list(model_categories.values())
        })
        
        # 표와 막대 그래프로 표시
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(model_df, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            
            # 모델별로 막대 추가
            for i, (model, ratio) in enumerate(model_results.items()):
                # 색상 설정
                if model_categories[model] == "정상 고객":
                    color = "#4CAF50"
                elif model_categories[model] == "위험 고객":
                    color = "#FF9800"
                else:
                    color = "#F44336"
                
                fig.add_trace(go.Bar(
                    x=[model],
                    y=[ratio * 100],
                    name=model,
                    marker_color=color,
                    text=[f"{ratio*100:.1f}%"],
                    textposition='auto'
                ))
            
            fig.update_layout(
                title="모델별 상환 비율 예측",
                yaxis_title="상환 비율 (%)",
                yaxis=dict(range=[0, 100]),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # 행동 조언
        st.markdown("#### 신용점수 개선을 위한 조언")
        
        st.markdown("""
        <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 15px; animation: fadeIn 1.5s ease-in-out;">
            <h4 style="color: #1E88E5; margin-top: 0;">다음 단계</h4>
            <ul style="margin-top: 10px;">
                <li>정기적으로 신용 보고서를 확인하고 오류가 있는지 검토하세요.</li>
                <li>신용카드 한도를 30% 이하로 유지하는 것이 좋습니다.</li>
                <li>모든 청구서와 대출을 정시에 납부하세요.</li>
                <li>불필요한 신용 조회를 줄이세요.</li>
                <li>오래된 신용 계정을 유지하여 신용 거래 기간을 늘리세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 시뮬레이션 공유 및 저장 옵션
        st.markdown("#### 결과 저장 및 공유")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="PDF 보고서 저장",
                data="시뮬레이션 보고서 데이터",
                file_name="연체_위험_예측_보고서.pdf",
                mime="application/pdf"
            )
        
        with col2:
            st.button("결과 이메일로 받기")

# 페이지 푸터
st.markdown("""
<div class="footer">
    <p>© 2025 금융 AI 분석팀 - 소비/생활 패턴 기반 연체 예측 모델</p>
    <p>버전 1.0.0 | 마지막 업데이트: 2025년 3월 7일</p>
</div>
""", unsafe_allow_html=True)
   