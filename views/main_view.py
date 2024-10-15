import streamlit as st
from views.case_view import CaseView


def set_custom_style():
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.markdown("""
        <style>
            /* Main layout */
            .main .block-container {
                padding-top: 1rem;
                padding-bottom: 2rem;
            }

            /* Title */
            .main-title {
                font-size: 2.8em;
                font-weight: 700;
                color: #1E3A8A;
                text-align: center;
                margin-bottom: 2rem;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }

            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #F3F4F6 !important;
                border-right: 1px solid #E5E7EB !important;
            }
            [data-testid="stSidebar"] > div:first-child {
                height: calc(100vh - 2rem) !important;
                overflow-y: auto;
            }
            [data-testid="stSidebar"] .stButton {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            [data-testid="stSidebar"] .stButton > button {
                width: 100%;
                text-align: left;
                padding: 0.75rem 1rem;
                background-color: #ffffff;
                color: #1E3A8A;
                border: 1px solid #D1D5DB;
                border-radius: 0.375rem;
                font-size: 1em;
                font-weight: 500;
                margin-bottom: 0.5rem;
                transition: all 0.3s ease;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background-color: #EFF6FF;
                border-color: #1E3A8A;
            }

            /* Move sidebar content down */
            [data-testid="stSidebar"] .sidebar-content {
                display: flex !important;
                flex-direction: column !important;
                justify-content: flex-end !important;
                height: 100% !important;
                padding-top: 100vh !important; /* Adjust this value to move content up or down */
                box-sizing: border-box !important;
            }

            /* Content area */
            .content-container {
                background-color: #ffffff;
                border-radius: 0.5rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                padding: 2rem;
                margin-top: 1rem;
            }

            /* Headers */
            h2 {
                color: #1E3A8A;
                font-weight: 600;
                margin-bottom: 1rem;
                border-bottom: 2px solid #E5E7EB;
                padding-bottom: 0.5rem;
            }

            /* Form inputs */
            .stTextInput>div>div>input, .stSelectbox>div>div>select {
                border-radius: 0.375rem;
                border: 1px solid #D1D5DB;
            }

            /* Buttons in content area */
            .stButton>button {
                background-color: #1E3A8A;
                color: white;
                font-weight: 500;
                padding: 0.5rem 1rem;
                border-radius: 0.375rem;
                border: none;
                transition: background-color 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #1C3366;
            }
        </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="⚖️ Case Management System", layout="wide")
    set_custom_style()

    st.markdown('<h1 class="main-title">⚖️ Case Management System</h1>', unsafe_allow_html=True)

    case_view = CaseView()

    # Sidebar navigation
    with st.sidebar:
        nav_options = {
            "🏠 Home": "home",
            "➕ Add New Case": "add_case",
            "🔍 Search Case": "search_case",
            "📅 Today's Case List": "todays_case_list",
            "📆 Cases by Date": "cases_by_date",
            "⏳ Pending Cases": "pending_cases",
            "🏢 Cases By Company Name": "cases_by_company_name",
            "📝 Update Config": "update_config",
            "✍️ Update Case": "update_case"
        }
        for label, page in nav_options.items():
            if st.button(label):
                st.session_state.page = page

    # Main content area
    with st.container():
        if "page" not in st.session_state:
            st.session_state.page = "home"

        content = st.container()
        with content:
            if st.session_state.page == "home":
                st.write("## Welcome to the Case Management System")
                st.write("Select an option from the sidebar to get started.")
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
            elif st.session_state.page == "update_config":
                case_view.update_config()
            elif st.session_state.page == "update_case":
                case_view.update_case()