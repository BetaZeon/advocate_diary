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
            "✍️ Update Case": "update_case",
            "📋 View Logs": "view_logs"
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
            elif st.session_state.page == "update_case":
                case_view.update_case()
            elif st.session_state.page == "view_logs":
                view_logs()