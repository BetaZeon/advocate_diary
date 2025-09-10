import streamlit as st
from views.case_view import CaseView
import os
from pathlib import Path
from datetime import datetime
from utils.logger import get_logs_as_text, clear_memory_logs, clear_all_logs, get_sheets_logs, is_production
from utils.sheets_logger import sheets_logger


def set_custom_style():
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.markdown("""
        <style>
            /* Import Professional Law Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&family=Roboto+Slab:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            /* Professional Law Theme Variables */
            :root {
                /* Primary Law Colors */
                --navy-blue: #1B263B;
                --navy-dark: #0F1419;
                --navy-light: #2C3E50;
                --gold: #C5A880;
                --gold-light: #D4B896;
                --gold-dark: #B8956A;
                
                /* Status Colors */
                --status-open: #2563EB;
                --status-compromised: #F59E0B;
                --status-award: #10B981;
                --status-dd: #DC2626;
                
                /* Professional Grays */
                --ivory: #FEFCF8;
                --ivory-dark: #F5F3F0;
                --charcoal: #374151;
                --charcoal-light: #6B7280;
                
                /* Accent Colors */
                --deep-green: #065F46;
                --maroon: #7C2D12;
                --bronze: #92400E;
                
                /* Glass Effects */
                --glass-bg: rgba(27, 38, 59, 0.85);
                --glass-border: rgba(197, 168, 128, 0.3);
                --glass-light: rgba(254, 252, 248, 0.9);
                
                /* Shadows */
                --shadow-sm: 0 1px 3px 0 rgba(27, 38, 59, 0.1), 0 1px 2px 0 rgba(27, 38, 59, 0.06);
                --shadow-md: 0 4px 6px -1px rgba(27, 38, 59, 0.1), 0 2px 4px -1px rgba(27, 38, 59, 0.06);
                --shadow-lg: 0 10px 15px -3px rgba(27, 38, 59, 0.1), 0 4px 6px -2px rgba(27, 38, 59, 0.05);
                --shadow-xl: 0 20px 25px -5px rgba(27, 38, 59, 0.1), 0 10px 10px -5px rgba(27, 38, 59, 0.04);
                
                /* Border Radius */
                --radius-sm: 0.375rem;
                --radius-md: 0.5rem;
                --radius-lg: 0.75rem;
                --radius-xl: 1rem;
                --radius-2xl: 1.5rem;
            }
            
            /* Global Styles */
            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Professional Background with Glassmorphism */
            .main {
                background: linear-gradient(135deg, #0F1419 0%, #1B263B 50%, #2C3E50 100%);
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }
            
            .main::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="legal-pattern" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M20 0L40 20L20 40L0 20Z" fill="none" stroke="%23C5A880" stroke-width="0.3" opacity="0.15"/></pattern></defs><rect width="100" height="100" fill="url(%23legal-pattern)"/></svg>');
                opacity: 0.4;
                z-index: 0;
            }
            
            .main::after {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at 30% 20%, rgba(197, 168, 128, 0.1) 0%, transparent 50%),
                            radial-gradient(circle at 70% 80%, rgba(27, 38, 59, 0.2) 0%, transparent 50%);
                animation: float 20s ease-in-out infinite;
                z-index: 0;
            }
            
            @keyframes float {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                33% { transform: translate(30px, -30px) rotate(120deg); }
                66% { transform: translate(-20px, 20px) rotate(240deg); }
            }
            
            /* Main Layout */
            .main .block-container {
                padding: 2rem 1rem;
                max-width: 1400px;
                position: relative;
                z-index: 1;
            }
            
            /* Professional Header */
            .main-header {
                background: linear-gradient(135deg, var(--navy-blue) 0%, var(--navy-light) 100%);
                padding: 3rem 2rem;
                border-radius: var(--radius-2xl);
                margin-bottom: 2rem;
                text-align: center;
                color: var(--ivory);
                box-shadow: var(--shadow-xl);
                position: relative;
                overflow: hidden;
                border: 2px solid var(--gold);
            }
            
            .main-header::before {
                content: '⚖️';
                position: absolute;
                top: 1rem;
                right: 2rem;
                font-size: 3rem;
                opacity: 0.1;
                z-index: 0;
            }
            
            .main-title {
                font-family: 'Merriweather', serif;
                font-size: 3.5rem;
                font-weight: 900;
                margin: 0;
                color: var(--gold);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                position: relative;
                z-index: 1;
            }
            
            .main-subtitle {
                font-family: 'Roboto Slab', serif;
                font-size: 1.25rem;
                font-weight: 400;
                margin: 0.5rem 0 0 0;
                color: var(--ivory);
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }
            
            /* Professional Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, var(--navy-blue) 0%, var(--navy-light) 100%) !important;
                border-right: 3px solid var(--gold) !important;
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                box-shadow: var(--shadow-lg);
            }
            
            [data-testid="stSidebar"] > div:first-child {
                height: calc(100vh - 2rem) !important;
                overflow-y: auto;
                padding: 2rem 1rem;
                display: block !important;
                visibility: visible !important;
            }
            
            /* Ensure sidebar is always visible */
            .stApp > div:first-child {
                display: flex !important;
            }
            
            /* Force sidebar to always be visible */
            .stApp > div:first-child > div:first-child {
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                width: 320px !important;
                min-width: 320px !important;
                max-width: 320px !important;
            }
            
            /* Prevent sidebar from collapsing */
            [data-testid="stSidebar"] {
                transform: translateX(0) !important;
                transition: none !important;
            }
            
            /* Hide only the sidebar collapse button */
            .stApp > div:first-child > div:first-child > div:first-child > button:not([data-testid*="stButton"]) {
                display: none !important;
            }
            
            .sidebar-title {
                font-family: 'Merriweather', serif;
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--gold);
                margin-bottom: 2rem;
                padding: 1rem;
                background: var(--glass-bg);
                backdrop-filter: blur(10px);
                border: 2px solid var(--gold);
                border-radius: var(--radius-lg);
                text-align: center;
                box-shadow: var(--shadow-md);
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            
            /* Professional Navigation Buttons */
            [data-testid="stSidebar"] .stButton {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 0.75rem;
            }
            
            [data-testid="stSidebar"] .stButton > button {
                width: 100%;
                background: var(--glass-bg);
                backdrop-filter: blur(10px);
                color: var(--ivory);
                border: 2px solid var(--glass-border);
                border-radius: var(--radius-lg);
                padding: 1rem 1.5rem;
                font-weight: 600;
                font-size: 0.95rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: var(--shadow-sm);
                position: relative;
                overflow: hidden;
                text-align: left;
            }
            
            [data-testid="stSidebar"] .stButton > button:hover {
                background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
                color: var(--navy-blue);
                border-color: var(--gold);
                transform: translateX(5px);
                box-shadow: var(--shadow-lg);
                font-weight: 700;
            }
            
            /* Professional Content Cards with Enhanced Glassmorphism */
            .content-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: var(--radius-xl);
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }
            
            .content-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
                border-color: rgba(197, 168, 128, 0.4);
            }
            
            .content-card::before {
                display: none;
            }
            
            .content-card::after {
                display: none;
            }
            
            .content-card h2 {
                font-family: 'Merriweather', serif;
                color: var(--ivory);
                font-weight: 700;
                margin-bottom: 1rem;
                font-size: 1.75rem;
                position: relative;
                z-index: 1;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .content-card p {
                color: rgba(255, 255, 255, 0.9);
                font-size: 1rem;
                line-height: 1.6;
                position: relative;
                z-index: 1;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            }
            
            /* Professional Form Styling */
            .stSelectbox > div > div {
                background: var(--ivory) !important;
                border: 2px solid var(--gold) !important;
                border-radius: var(--radius-md) !important;
                transition: all 0.3s ease !important;
            }
            
            .stSelectbox > div > div:focus-within {
                border-color: var(--navy-blue) !important;
                box-shadow: 0 0 0 3px rgba(27, 38, 59, 0.1) !important;
                transform: scale(1.02) !important;
            }
            
            .stSelectbox > div > div > select {
                color: var(--navy-blue) !important;
                background: var(--ivory) !important;
                font-weight: 500 !important;
            }
            
            .stSelectbox > div > div > select option {
                color: var(--navy-blue) !important;
                background: var(--ivory) !important;
            }
            
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stDateInput > div > div > input {
                background: var(--ivory) !important;
                border: 2px solid var(--gold) !important;
                border-radius: var(--radius-md) !important;
                padding: 0.75rem 1rem !important;
                font-size: 1rem !important;
                color: var(--navy-blue) !important;
                transition: all 0.3s ease !important;
                font-weight: 500 !important;
            }
            
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus,
            .stDateInput > div > div > input:focus {
                border-color: var(--navy-blue) !important;
                box-shadow: 0 0 0 3px rgba(27, 38, 59, 0.1) !important;
                outline: none !important;
                color: var(--navy-blue) !important;
                transform: scale(1.02) !important;
            }
            
            .stTextInput > div > div > input::placeholder,
            .stTextArea > div > div > textarea::placeholder {
                color: var(--charcoal-light) !important;
                font-style: italic !important;
            }
            
            /* Professional Button Styling */
            .stButton > button {
                background: linear-gradient(135deg, var(--navy-blue) 0%, var(--navy-light) 100%);
                color: var(--ivory);
                font-weight: 600;
                padding: 0.75rem 2rem;
                border-radius: var(--radius-md);
                border: 2px solid var(--gold);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: var(--shadow-md);
                position: relative;
                overflow: hidden;
                font-size: 1rem;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
                color: var(--navy-blue);
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
                border-color: var(--navy-blue);
            }
            
            .stButton > button:active {
                transform: translateY(0);
            }
            
            /* Professional Metrics Cards with Glassmorphism */
            .metric-card {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 2rem;
                border-radius: var(--radius-xl);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                text-align: center;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            
            .metric-card::before {
                display: none;
            }
            
            .metric-card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
                border-color: rgba(197, 168, 128, 0.4);
            }
            
            .metric-value {
                font-family: 'Merriweather', serif;
                font-size: 3rem;
                font-weight: 900;
                color: var(--gold);
                margin: 0;
                text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                position: relative;
                z-index: 1;
            }
            
            .metric-label {
                font-size: 0.9rem;
                color: rgba(255, 255, 255, 0.8);
                margin: 0.5rem 0 0 0;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                position: relative;
                z-index: 1;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            }
            
            /* Status Tags */
            .status-tag {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                border-radius: var(--radius-sm);
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .status-open {
                background-color: var(--status-open);
                color: white;
            }
            
            .status-compromised {
                background-color: var(--status-compromised);
                color: white;
            }
            
            .status-award {
                background-color: var(--status-award);
                color: white;
            }
            
            .status-dd {
                background-color: var(--status-dd);
                color: white;
            }
            
            /* Professional Data Tables */
            .stDataFrame {
                border-radius: var(--radius-lg);
                overflow: hidden;
                box-shadow: var(--shadow-md);
                background: var(--ivory);
                border: 2px solid var(--gold);
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--ivory-dark);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, var(--navy-blue), var(--gold));
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, var(--navy-dark), var(--gold-dark));
            }
            
            /* Professional Messages */
            .stSuccess {
                background: linear-gradient(135deg, var(--status-award) 0%, var(--deep-green) 100%);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: var(--radius-md);
                border: 2px solid var(--status-award);
                box-shadow: var(--shadow-md);
                font-weight: 600;
            }
            
            .stError {
                background: linear-gradient(135deg, var(--status-dd) 0%, var(--maroon) 100%);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: var(--radius-md);
                border: 2px solid var(--status-dd);
                box-shadow: var(--shadow-md);
                font-weight: 600;
            }
            
            .stWarning {
                background: linear-gradient(135deg, var(--status-compromised) 0%, var(--bronze) 100%);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: var(--radius-md);
                border: 2px solid var(--status-compromised);
                box-shadow: var(--shadow-md);
                font-weight: 600;
            }
            
            .stInfo {
                background: linear-gradient(135deg, var(--status-open) 0%, var(--navy-blue) 100%);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: var(--radius-md);
                border: 2px solid var(--status-open);
                box-shadow: var(--shadow-md);
                font-weight: 600;
            }
            
            /* Global Search Bar */
            .global-search {
                background: var(--glass-light);
                border: 2px solid var(--gold);
                border-radius: var(--radius-lg);
                padding: 1rem;
                margin-bottom: 2rem;
                box-shadow: var(--shadow-md);
            }
            
            .global-search h3 {
                font-family: 'Merriweather', serif;
                color: var(--ivory);
                margin-bottom: 1rem;
                font-size: 1.5rem;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            /* Case Header Card */
            .case-header-card {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: var(--radius-xl);
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                position: relative;
                overflow: hidden;
            }
            
            .case-header-card::before {
                display: none;
            }
            
            .case-title {
                font-family: 'Merriweather', serif;
                font-size: 2rem;
                font-weight: 900;
                color: var(--gold);
                margin-bottom: 0.5rem;
                position: relative;
                z-index: 1;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .case-subtitle {
                font-size: 1.1rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 1rem;
                position: relative;
                z-index: 1;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            }
            
            /* Case Details Grid */
            .case-details-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
                margin-bottom: 2rem;
            }
            
            .case-detail-section {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
                position: relative;
                overflow: hidden;
            }
            
            .case-detail-section::before {
                display: none;
            }
            
            .case-detail-section h4 {
                font-family: 'Merriweather', serif;
                color: var(--gold);
                font-size: 1.2rem;
                margin-bottom: 1rem;
                position: relative;
                z-index: 1;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            }
            
            .case-detail-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.5rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                position: relative;
                z-index: 1;
            }
            
            .case-detail-item:last-child {
                border-bottom: none;
            }
            
            .case-detail-label {
                color: rgba(255, 255, 255, 0.7);
                font-weight: 500;
                font-size: 0.9rem;
            }
            
            .case-detail-value {
                color: var(--ivory);
                font-weight: 600;
                font-size: 0.95rem;
            }
            
            /* Timeline Component */
            .timeline-container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
                position: relative;
                overflow: hidden;
            }
            
            .timeline-container::before {
                display: none;
            }
            
            .timeline-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 1rem;
                position: relative;
                z-index: 1;
            }
            
            .timeline-item:last-child {
                margin-bottom: 0;
            }
            
            .timeline-dot {
                width: 12px;
                height: 12px;
                background: var(--gold);
                border-radius: 50%;
                margin-right: 1rem;
                margin-top: 0.5rem;
                box-shadow: 0 0 0 4px rgba(197, 168, 128, 0.3);
            }
            
            .timeline-content {
                flex: 1;
            }
            
            .timeline-date {
                color: var(--gold);
                font-weight: 600;
                font-size: 0.9rem;
                margin-bottom: 0.25rem;
            }
            
            .timeline-stage {
                color: var(--ivory);
                font-weight: 500;
                font-size: 1rem;
                margin-bottom: 0.25rem;
            }
            
            .timeline-remarks {
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.85rem;
                font-style: italic;
            }
            
            /* Action Buttons (no sticky bar) */
            
            .action-button {
                background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
                color: var(--navy-blue);
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: var(--radius-md);
                font-weight: 600;
                font-size: 0.9rem;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            
            .action-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
            }
            
            .action-button.secondary {
                background: rgba(255, 255, 255, 0.1);
                color: var(--ivory);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .action-button.secondary:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)


def detailed_case_view(case_data):
    """Display detailed case information with glassmorphism design"""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    # Case Header Card
    st.markdown('<div class="case-header-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="case-title">Case #{case_data.get("Case Number", "N/A")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="case-subtitle">{case_data.get("Case Title", "No Title")}</div>', unsafe_allow_html=True)
    
    # Status and Type badges
    col1, col2, col3 = st.columns(3)
    with col1:
        status = case_data.get("Status", "OPEN")
        status_class = f"status-{status.lower()}"
        st.markdown(f'<span class="status-tag {status_class}">{status}</span>', unsafe_allow_html=True)
    
    with col2:
        case_type = case_data.get("Case Type", "N/A")
        st.markdown(f'<span class="status-tag status-open">{case_type}</span>', unsafe_allow_html=True)
    
    with col3:
        company = case_data.get("Company Name", "N/A")
        st.markdown(f'<span class="status-tag status-compromised">{company}</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Case Details Grid
    st.markdown('<div class="case-details-grid">', unsafe_allow_html=True)
    
    # Left Column - Basic Information
    st.markdown('<div class="case-detail-section">', unsafe_allow_html=True)
    st.markdown('<h4>📋 Case Information</h4>', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="case-detail-item">
            <span class="case-detail-label">Location:</span>
            <span class="case-detail-value">{case_data.get("Location", "N/A")}</span>
        </div>
        <div class="case-detail-item">
            <span class="case-detail-label">Advocate Name:</span>
            <span class="case-detail-value">{case_data.get("Claimant Advocate Name", "N/A")}</span>
        </div>
        <div class="case-detail-item">
            <span class="case-detail-label">Mobile Number:</span>
            <span class="case-detail-value">{case_data.get("Claimant Advocate Mobile Number", "N/A")}</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right Column - Dates and Status
    st.markdown('<div class="case-detail-section">', unsafe_allow_html=True)
    st.markdown('<h4>📅 Dates & Status</h4>', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="case-detail-item">
            <span class="case-detail-label">Upcoming Date:</span>
            <span class="case-detail-value">{case_data.get("Upcoming Date", "N/A")}</span>
        </div>
        <div class="case-detail-item">
            <span class="case-detail-label">Current Stage:</span>
            <span class="case-detail-value">{case_data.get("Stage", "N/A")}</span>
        </div>
        <div class="case-detail-item">
            <span class="case-detail-label">Status:</span>
            <span class="case-detail-value">{case_data.get("Status", "N/A")}</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Timeline Section
    st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
    st.markdown('<h4>📈 Case Timeline</h4>', unsafe_allow_html=True)
    
    # Parse previous dates if available
    previous_dates = case_data.get("Previous Dates", "")
    if previous_dates:
        dates_list = previous_dates.split(";") if ";" in previous_dates else [previous_dates]
        for i, date_entry in enumerate(dates_list[:5]):  # Show last 5 entries
            if date_entry.strip():
                st.markdown(f'''
                    <div class="timeline-item">
                        <div class="timeline-dot"></div>
                        <div class="timeline-content">
                            <div class="timeline-date">{date_entry.strip()}</div>
                            <div class="timeline-stage">Previous Hearing</div>
                            <div class="timeline-remarks">Case proceedings</div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
    else:
        st.markdown('<div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-content"><div class="timeline-stage">No previous dates recorded</div></div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Remarks Section
    remarks = case_data.get("Remarks", "")
    if remarks:
        st.markdown('<div class="case-detail-section">', unsafe_allow_html=True)
        st.markdown('<h4>📝 Remarks</h4>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: rgba(255, 255, 255, 0.8); font-style: italic; position: relative; z-index: 1;">{remarks}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons (removed sticky bar)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✍️ Update Case", key="update_case_btn", use_container_width=True):
            st.session_state.page = "update_case"
            st.session_state.case_to_update = case_data
            st.rerun()
    
    with col2:
        if st.button("📅 Add Hearing", key="add_hearing_btn", use_container_width=True):
            st.info("Add hearing date functionality would be implemented here")
    
    with col3:
        if st.button("📝 Add Remarks", key="add_remarks_btn", use_container_width=True):
            st.info("Add remarks functionality would be implemented here")
    
    with col4:
        if st.button("✅ Close Case", key="close_case_btn", use_container_width=True):
            st.info("Close case functionality would be implemented here")
    st.markdown('</div>', unsafe_allow_html=True)


def view_logs():
    """Display application logs"""
    st.write("## 📋 Application Logs")
    
    # Check if running in production
    production_mode = is_production()
    
    if production_mode:
        st.info("🌐 **Production Mode**: Logs are stored in Google Sheets and memory.")
        st.success("✅ **Persistent Logging**: Logs are saved to Google Sheets worksheet for permanent storage.")
    else:
        st.info("💻 **Development Mode**: Logs are stored in local files.")
    
    # Debug section for production
    if production_mode:
        with st.expander("🔧 Debug Information", expanded=False):
            st.write("**Google Sheets Logger Status:**")
            st.write(f"- Available: {sheets_logger.is_available}")
            st.write(f"- Worksheet Name: {sheets_logger.worksheet_name}")
            
            if sheets_logger.is_available:
                # Test connection
                success, message = sheets_logger.test_connection()
                st.write(f"- Connection Test: {'✅' if success else '❌'} {message}")
                
                # Worksheet info
                info = sheets_logger.get_worksheet_info()
                st.write(f"- Worksheet Info: {info}")
                
                # Test log entry
                if st.button("🧪 Test Log Entry"):
                    test_result = sheets_logger.log("INFO", "Test log entry from debug panel", "debug_test", "Testing Google Sheets logging")
                    if test_result:
                        st.success("✅ Test log entry successful!")
                    else:
                        st.error("❌ Test log entry failed!")
                
                # Concurrency test
                st.write("**Concurrency Test:**")
                if st.button("🚀 Run Concurrency Test"):
                    with st.spinner("Running concurrency test..."):
                        try:
                            from utils.concurrency_test import simulate_concurrent_case_addition
                            results = simulate_concurrent_case_addition(num_users=3, cases_per_user=2)
                            
                            successful = sum(1 for r in results if r.get('success', False))
                            total = len(results)
                            
                            st.success(f"✅ Concurrency test completed: {successful}/{total} operations successful")
                            
                            # Show results
                            import pandas as pd
                            df = pd.DataFrame(results)
                            st.dataframe(df, use_container_width=True)
                            
                        except Exception as e:
                            st.error(f"❌ Concurrency test failed: {e}")
            else:
                st.error("❌ Google Sheets logging is not available")
                st.write("**Possible issues:**")
                st.write("- No Google Sheets credentials in Streamlit secrets")
                st.write("- Authentication failed")
                st.write("- Spreadsheet access denied")
                st.write("- Network connectivity issues")
    
    # Log controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if production_mode:
            st.write("**Log source:** Google Sheets worksheet + In-memory storage")
        else:
            log_file = Path("logs/advocate_diary.log")
            st.write(f"**Log file:** `{log_file.absolute()}`")
    
    with col2:
        if st.button("🔄 Refresh Logs"):
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear Logs"):
            try:
                if production_mode:
                    clear_all_logs()
                    st.success("All logs cleared successfully! (Google Sheets + Memory)")
                else:
                    log_file = Path("logs/advocate_diary.log")
                    if log_file.exists():
                        log_file.unlink()
                        st.success("Log file cleared successfully!")
                    else:
                        st.info("No log file to clear.")
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing logs: {e}")
    
    # Display logs
    try:
        # Get log content based on environment
        log_content = get_logs_as_text()
        
        if not log_content.strip():
            if production_mode:
                st.info("No logs in memory yet. Start using the application to see logs here.")
            else:
                st.info("Log file is empty. Start using the application to see logs here.")
            return
        
        # Show last N lines
        lines = log_content.strip().split('\n')
        num_lines = len(lines)
        
        st.write(f"**Total log entries:** {num_lines}")
        
        # Option to show last N lines
        show_lines = st.slider("Show last N lines:", min_value=10, max_value=min(1000, num_lines), value=min(100, num_lines))
        
        if show_lines < num_lines:
            display_lines = lines[-show_lines:]
            st.info(f"Showing last {show_lines} lines out of {num_lines} total lines.")
        else:
            display_lines = lines
        
        # Display logs in a text area
        log_text = '\n'.join(display_lines)
        st.text_area("Log Content:", value=log_text, height=400, disabled=True)
        
        # In production, also show structured Google Sheets logs
        if production_mode:
            st.write("---")
            st.write("### 📊 Structured Logs from Google Sheets")
            
            try:
                sheets_logs = get_sheets_logs(limit=50)  # Get last 50 logs
                if sheets_logs:
                    # Convert to DataFrame for better display
                    import pandas as pd
                    df = pd.DataFrame(sheets_logs)
                    
                    # Display as a table
                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=300,
                        column_config={
                            "Timestamp": st.column_config.DatetimeColumn(
                                "Timestamp",
                                format="YYYY-MM-DD HH:mm:ss"
                            ),
                            "Level": st.column_config.TextColumn(
                                "Level",
                                width="small"
                            ),
                            "Message": st.column_config.TextColumn(
                                "Message",
                                width="large"
                            ),
                            "Function": st.column_config.TextColumn(
                                "Function",
                                width="medium"
                            ),
                            "Context": st.column_config.TextColumn(
                                "Context",
                                width="large"
                            )
                        }
                    )
                    
                    st.write(f"**Showing last {len(sheets_logs)} structured log entries from Google Sheets**")
                else:
                    st.info("No structured logs found in Google Sheets yet.")
            except Exception as e:
                st.warning(f"Could not load structured logs: {e}")
        
        # Download button
        if log_content.strip():
            st.download_button(
                label="📥 Download Logs",
                data=log_content,
                file_name=f"advocate_diary_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
                mime="text/plain"
            )
        
    except Exception as e:
        st.error(f"Error reading logs: {e}")


def main():
    st.set_page_config(page_title="⚖️ Advocate Diary", layout="wide")
    set_custom_style()

    # Modern header with gradient
    st.markdown("""
        <div class="main-header">
            <h1 class="main-title">⚖️ Advocate Diary</h1>
            <p class="main-subtitle">Professional Case Management System</p>
        </div>
    """, unsafe_allow_html=True)

    case_view = CaseView()

    # Sidebar navigation
    with st.sidebar:
        # Sidebar header
        st.markdown('<div class="sidebar-title">📋 Navigation</div>', unsafe_allow_html=True)
        
        nav_options = {
            "🏠 Dashboard": "home",
            "📋 Add Case": "add_case",
            "🔍 Search Cases": "search_case",
            "⚖️ Today's Hearings": "todays_case_list",
            "📅 Cases by Date": "cases_by_date",
            "⏳ Pending Cases": "pending_cases",
            "🏢 By Company": "cases_by_company_name",
            "✍️ Update Case": "update_case",
            "📄 Case Details": "case_details"
        }
        
        for label, page in nav_options.items():
            if st.button(label, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()

    # Main content area
    with st.container():
        if "page" not in st.session_state:
            st.session_state.page = "home"

        content = st.container()
        with content:
            if st.session_state.page == "home":
                # Global Search Bar
                st.markdown('<div class="global-search">', unsafe_allow_html=True)
                st.markdown("### 🔍 Global Case Search")
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    search_query = st.text_input("Search by case number, title, or company", placeholder="Enter search term...", key="global_search")
                
                with col2:
                    search_criteria = st.selectbox("Search by", ["All", "Case Number", "Case Title", "Company"], key="global_criteria")
                
                with col3:
                    if st.button("🔍 Search", key="global_search_btn", use_container_width=True):
                        if search_query:
                            if search_criteria == "All":
                                st.session_state.page = "search_case"
                                st.session_state.search_query = search_query
                            else:
                                st.session_state.page = "search_case"
                                st.session_state.search_criteria = search_criteria
                                st.session_state.search_query = search_query
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Welcome section with metrics
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown("## 📊 Case Management Dashboard")
                st.markdown("Monitor your legal practice with real-time insights and quick access to essential functions.")
                
                # Quick stats (placeholder - you can make these dynamic)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-value">0</div>
                            <div class="metric-label">Total Cases</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-value">0</div>
                            <div class="metric-label">Active Cases</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-value">0</div>
                            <div class="metric-label">Today's Hearings</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown("""
                        <div class="metric-card">
                            <div class="metric-value">0</div>
                            <div class="metric-label">Pending Cases</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Quick actions
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown("## ⚡ Quick Actions")
                st.markdown("Access the most frequently used features with a single click")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("➕ Add New Case", key="quick_add", use_container_width=True):
                        st.session_state.page = "add_case"
                        st.rerun()
                
                with col2:
                    if st.button("🔍 Search Cases", key="quick_search", use_container_width=True):
                        st.session_state.page = "search_case"
                        st.rerun()
                
                with col3:
                    if st.button("📅 Today's Cases", key="quick_today", use_container_width=True):
                        st.session_state.page = "todays_case_list"
                        st.rerun()
                
                with col4:
                    if st.button("✍️ Update Case", key="quick_update", use_container_width=True):
                        st.session_state.page = "update_case"
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Upcoming Hearings Widget
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown("## ⚖️ Upcoming Hearings")
                st.markdown("Your next 5 scheduled cases")
                
                # Placeholder for upcoming hearings
                st.info("No upcoming hearings scheduled for today.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Features overview
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown("## 🏛️ Professional Features")
                st.markdown("Comprehensive case management tools designed specifically for legal professionals")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                        **📋 Case Management**
                        - Add and track legal cases
                        - Organize by location and type
                        - Set upcoming dates and stages
                        - Track case status and progress
                        
                        **🔍 Advanced Search & Filtering**
                        - Search by case number or title
                        - Filter by insurance company
                        - Find cases by date range
                        - Global search functionality
                    """)
                
                with col2:
                    st.markdown("""
                        **📊 Analytics & Reporting**
                        - View today's scheduled cases
                        - Track pending case status
                        - Generate case summaries
                        - Monitor case progress
                        
                        **🔒 Security & Reliability**
                        - Google Sheets integration
                        - Real-time synchronization
                        - Concurrency-safe operations
                        - Professional data protection
                    """)
                
                st.markdown('</div>', unsafe_allow_html=True)
            elif st.session_state.page == "add_case":
                case_view.add_case()
            elif st.session_state.page == "search_case":
                case_view.search_case()
            elif st.session_state.page == "todays_case_list":
                case_view.todays_case_list()
            elif st.session_state.page == "cases_by_date":
                case_view.cases_by_date()
            elif st.session_state.page == "pending_cases":
                case_view.pending_cases()
            elif st.session_state.page == "cases_by_company_name":
                case_view.search_cases_by_company_name()
            elif st.session_state.page == "update_case":
                case_view.update_case()
            elif st.session_state.page == "case_details":
                # Case Details page with search functionality
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.markdown("## 📄 Case Details")
                st.markdown("Search for a case to view detailed information with timeline and actions.")
                
                search_query = st.text_input("Enter Case Number or Case Title to view details", key="case_details_search")
                
                if st.button("🔍 View Case Details", key="view_case_details_btn"):
                    if search_query:
                        # Search for the case
                        from controllers.case_controller import CaseController
                        controller = CaseController()
                        case = controller.get_case_by_number_or_title(search_query)
                        
                        if case:
                            st.session_state.selected_case = case
                            st.rerun()
                        else:
                            st.error("Case not found. Please check the case number or title.")
                    else:
                        st.warning("Please enter a case number or title to search.")
                
                # Display case details if selected
                if "selected_case" in st.session_state and st.session_state.selected_case:
                    st.markdown('</div>', unsafe_allow_html=True)  # Close the search card
                    detailed_case_view(st.session_state.selected_case)
                else:
                    st.markdown('</div>', unsafe_allow_html=True)