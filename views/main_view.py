import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import uuid
from views.case_view import CaseView
from controllers.case_controller import CaseController
from config_loader import load_config
from utils.logger import get_logs_as_text, clear_memory_logs, clear_all_logs, get_sheets_logs, is_production
from utils.sheets_logger import sheets_logger


def set_custom_style():
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            .stApp > header {display: none;}
            .stApp > div:first-child {padding-top: 0;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
          --primary: #2563eb;
          --primary-dark: #1d4ed8;
          --primary-light: #3b82f6;
          --secondary: #7c3aed;
          --accent: #f59e0b;
          --success: #10b981;
          --warning: #f59e0b;
          --error: #ef4444;
          --info: #06b6d4;
          
          --bg-primary: #ffffff;
          --bg-secondary: #f8fafc;
          --bg-tertiary: #f1f5f9;
          --bg-dark: #0f172a;
          --bg-card: #ffffff;
          --bg-glass: rgba(255, 255, 255, 0.8);
          
          --text-primary: #1e293b;
          --text-secondary: #64748b;
          --text-muted: #94a3b8;
          --text-light: #ffffff;
          
          --border-light: #e2e8f0;
          --border-medium: #cbd5e1;
          --border-dark: #94a3b8;
          
          --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
          --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
          --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
          --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
          
          --radius-sm: 0.375rem;
          --radius-md: 0.5rem;
          --radius-lg: 0.75rem;
          --radius-xl: 1rem;
          --radius-2xl: 1.5rem;
        }
        
        * {
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Main App Container */
        .main .block-container {
          padding: 2rem 1rem;
          max-width: 1400px;
        }
        
        [data-testid="stAppViewContainer"] {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
        }
        
        /* Header Styling */
        .app-header {
          background: var(--bg-glass);
          backdrop-filter: blur(20px);
          border-bottom: 1px solid var(--border-light);
          padding: 1rem 2rem;
          margin-bottom: 2rem;
          border-radius: 0 0 var(--radius-2xl) var(--radius-2xl);
          box-shadow: var(--shadow-lg);
        }
        
        .app-title {
          font-size: 2rem;
          font-weight: 800;
          color: var(--text-primary);
          margin: 0;
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        
        .app-subtitle {
          color: var(--text-secondary);
          font-size: 1rem;
          font-weight: 400;
          margin: 0.25rem 0 0 0;
        }
        
        /* Card Components */
        .card {
          background: var(--bg-card);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-xl);
          padding: 1.5rem;
          margin-bottom: 1rem;
          box-shadow: var(--shadow-md);
          transition: all 0.3s ease;
        }
        
        .card:hover {
          box-shadow: var(--shadow-xl);
          transform: translateY(-2px);
        }
        
        .card-header {
          margin-bottom: 1.5rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid var(--border-light);
        }
        
        .card-title {
          font-size: 1.5rem;
          font-weight: 700;
          color: var(--text-primary);
          margin: 0 0 0.5rem 0;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        
        .card-subtitle {
          color: var(--text-secondary);
          font-size: 0.95rem;
          margin: 0;
        }
        
        /* Metrics Grid */
        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin-bottom: 1rem;
        }
        
        .metric-card {
          background: var(--bg-card);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-lg);
          padding: 1.5rem;
          text-align: center;
          box-shadow: var(--shadow-sm);
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
        }
        
        .metric-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .metric-card:hover {
          transform: translateY(-4px);
          box-shadow: var(--shadow-lg);
        }
        
        .metric-value {
          font-size: 2.5rem;
          font-weight: 800;
          color: var(--text-primary);
          margin: 0.5rem 0;
          line-height: 1;
        }
        
        .metric-label {
          color: var(--text-secondary);
          font-size: 0.875rem;
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        
        .metric-icon {
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
          opacity: 0.7;
        }
        
        /* Status Badges */
        .badge {
          display: inline-flex;
          align-items: center;
          padding: 0.375rem 0.75rem;
          border-radius: var(--radius-md);
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.025em;
          margin-right: 0.5rem;
          margin-bottom: 0.25rem;
        }
        
        .badge-open {
          background: #dbeafe;
          color: #1e40af;
          border: 1px solid #93c5fd;
        }
        
        .badge-compromised {
          background: #fef3c7;
          color: #92400e;
          border: 1px solid #fcd34d;
        }
        
        .badge-award {
          background: #d1fae5;
          color: #065f46;
          border: 1px solid #6ee7b7;
        }
        
        .badge-dd {
          background: #fee2e2;
          color: #991b1b;
          border: 1px solid #fca5a5;
        }
        
        .badge-mact {
          background: #e0e7ff;
          color: #3730a3;
          border: 1px solid #a5b4fc;
        }
        
        .badge-wcc {
          background: #dcfce7;
          color: #166534;
          border: 1px solid #86efac;
        }
        
        .badge-dcf {
          background: #fef3c7;
          color: #92400e;
          border: 1px solid #fcd34d;
        }
        
        .badge-pla {
          background: #e0e7ff;
          color: #3730a3;
          border: 1px solid #a5b4fc;
        }
        
        /* Buttons */
        .stButton > button {
          background: var(--primary);
          color: white;
          border: none;
          border-radius: var(--radius-md);
          padding: 0.75rem 1.5rem;
          font-weight: 600;
          font-size: 0.875rem;
          transition: all 0.3s ease;
          box-shadow: var(--shadow-sm);
        }
        
        .stButton > button:hover {
          background: var(--primary-dark);
          transform: translateY(-1px);
          box-shadow: var(--shadow-md);
        }
        
        .btn-secondary {
          background: var(--bg-tertiary);
          color: var(--text-primary);
          border: 1px solid var(--border-medium);
        }
        
        .btn-secondary:hover {
          background: var(--border-light);
        }
        
        /* Form Elements */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea {
          border: 1px solid var(--border-medium);
          border-radius: var(--radius-md);
          padding: 0.75rem;
          font-size: 0.875rem;
          transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus {
          border-color: var(--primary);
          box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
          outline: none;
        }
        
        /* Data Tables */
        .stDataFrame {
          border-radius: var(--radius-lg);
          overflow: hidden;
          box-shadow: var(--shadow-sm);
          border: 1px solid var(--border-light);
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
          backdrop-filter: blur(20px);
          border-right: 1px solid rgba(255, 255, 255, 0.1);
          box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
        }
        
        section[data-testid="stSidebar"] .stRadio > div {
          gap: 0.5rem;
          padding: 0.5rem;
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label {
          padding: 0.875rem 1.25rem;
          border-radius: var(--radius-lg);
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          font-weight: 500;
          color: #cbd5e1;
          background: transparent;
          border: 1px solid transparent;
          position: relative;
          overflow: hidden;
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
          opacity: 0;
          transition: opacity 0.3s ease;
          border-radius: var(--radius-lg);
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label:hover {
          background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
          border-color: rgba(99, 102, 241, 0.3);
          color: #f1f5f9;
          transform: translateX(4px);
          box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label:hover::before {
          opacity: 1;
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label[data-testid="stRadio"]:checked {
          background: linear-gradient(135deg, #6366f1, #a855f7);
          color: white;
          border-color: #6366f1;
          box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
          transform: translateX(4px);
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label[data-testid="stRadio"]:checked::before {
          opacity: 0;
        }
        
        /* Sidebar header styling */
        section[data-testid="stSidebar"] .app-header {
          background: linear-gradient(135deg, #1e293b, #334155);
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          margin: -1rem -1rem 1rem -1rem;
          padding: 1.5rem 1rem;
          border-radius: 0;
        }
        
        section[data-testid="stSidebar"] .app-title {
          color: #f1f5f9;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        section[data-testid="stSidebar"] .app-subtitle {
          color: #cbd5e1;
        }
        
        /* Quick Actions */
        .quick-actions {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 1rem;
        }
        
        .action-btn {
          background: var(--bg-card);
          border: 1px solid var(--border-light);
          border-radius: var(--radius-lg);
          padding: 1.5rem;
          text-align: center;
          transition: all 0.3s ease;
          cursor: pointer;
          text-decoration: none;
          color: var(--text-primary);
        }
        
        .action-btn:hover {
          background: var(--primary);
          color: white;
          transform: translateY(-2px);
          box-shadow: var(--shadow-lg);
        }
        
        .action-icon {
          font-size: 2rem;
          margin-bottom: 0.5rem;
          display: block;
        }
        
        .action-label {
          font-weight: 600;
          font-size: 0.875rem;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
          .main .block-container {
            padding: 1rem 0.5rem;
          }
          
          .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
          }
          
          .app-title {
            font-size: 1.5rem;
          }
          
          .card {
            padding: 1rem;
          }
        }
        
        /* Loading States */
        .loading {
          opacity: 0.6;
          pointer-events: none;
        }
        
        /* Success/Error Messages */
        .stSuccess {
          background: #d1fae5;
          border: 1px solid #6ee7b7;
          color: #065f46;
          border-radius: var(--radius-md);
          padding: 1rem;
        }
        
        .stError {
          background: #fee2e2;
          border: 1px solid #fca5a5;
          color: #991b1b;
          border-radius: var(--radius-md);
          padding: 1rem;
        }
        
        .stWarning {
          background: #fef3c7;
          border: 1px solid #fcd34d;
          color: #92400e;
          border-radius: var(--radius-md);
          padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)


def sidebar_nav():
    st.sidebar.markdown("""
    <div class="app-header" style="margin: -1rem -1rem 1rem -1rem; padding: 1.5rem 1rem; background: linear-gradient(135deg, #1e293b, #334155); border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
        <div class="app-title" style="color: #f1f5f9; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);">
            <span style='font-size:1.5rem; margin-right: 0.5rem;'>⚖️</span>
            <span>Advocate Diary</span>
        </div>
        <div class="app-subtitle" style="color: #cbd5e1; font-size: 0.875rem; margin-top: 0.25rem;">Legal Practice Management</div>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("📊", "Dashboard"),
        ("➕", "Add Case"),
        ("🔍", "Search Case"),
        ("📅", "Today's Cases"),
        ("📆", "By Date"),
        ("⏳", "Pending Cases"),
        ("🏢", "By Company"),
        ("📋", "Case Details"),
        ("✏️", "Update Case"),
    ]
    
    # Create navigation with icons
    page_options = [f"{icon} {name}" for icon, name in pages]
    selected = st.sidebar.radio("", page_options, label_visibility="collapsed")
    
    # Extract the page name from the selected option
    for icon, name in pages:
        if f"{icon} {name}" == selected:
            return name
    return "Dashboard"


def badge(text: str, color: str) -> str:
    color_map = {
        "blue": "open",
        "green": "award", 
        "yellow": "compromised",
        "red": "dd",
        "mact": "mact",
        "wcc": "wcc",
        "dcf": "dcf",
        "pla": "pla"
    }
    badge_class = color_map.get(color.lower(), "open")
    return f'<span class="badge badge-{badge_class}">{text}</span>'


def parse_date(d: str | date) -> date:
    if isinstance(d, date):
        return d
    if d is None or str(d).lower() in ['none', 'null', '']:
        return date.today()  # Return today's date as default for null values
    try:
        return datetime.fromisoformat(str(d)).date()
    except ValueError:
        # If parsing fails, return today's date as fallback
        return date.today()


def render_metrics(df: pd.DataFrame):
    today = date.today()
    
    # Handle empty DataFrame
    if df.empty:
        closed = pending = todays = 0
    else:
        # Handle null values in Status column
        status_series = df["Status"].fillna("").astype(str)
        closed = (status_series.str.upper()=="AWARD").sum()
        pending = (status_series.str.upper()=="OPEN").sum()
        
        # Handle null values in Upcoming Date column
        upcoming_series = df["Upcoming Date"].fillna("")
        todays = (upcoming_series.apply(parse_date) == today).sum()

    metrics_data = [
        ("📊", "Total Cases", len(df), "#3b82f6"),
        ("⏳", "Pending", pending, "#f59e0b"),
        ("✅", "Closed", closed, "#10b981"),
        ("📅", "Today's Hearings", todays, "#8b5cf6"),
    ]
    
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    for icon, title, value, color in metrics_data:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon" style="color: {color};">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_upcoming(df: pd.DataFrame):
    st.markdown("""
    <div class="card-header">
        <div class="card-title">📅 Upcoming Hearings</div>
        <div class="card-subtitle">Next 5 scheduled court proceedings</div>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No cases available.")
    else:
        today = date.today()
        dff = df.copy()
        # Handle null values in Upcoming Date column
        dff["Upcoming Date"] = dff["Upcoming Date"].fillna("").apply(parse_date)
        dff = dff[dff["Upcoming Date"] >= today].sort_values("Upcoming Date").head(5)
        
        if dff.empty:
            st.info("No upcoming hearings scheduled.")
        else:
            st.dataframe(dff[["Case Number","Case Title","Upcoming Date","Stage"]], use_container_width=True, hide_index=True)


def update_company_cases(edited_df, original_df):
    """Update company cases with previous date handling"""
    from models.database import get_connection
    sheets_service = get_connection()
    
    try:
        # Find changes in the edited dataframe
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if upcoming date changed
            if str(row["Upcoming Date"]) != str(original_row["Upcoming Date"]):
                # Get the case ID
                case_id = row["ID"]
                
                # Prepare the updated case data
                updated_case_data = row.to_dict()
                
                # Handle previous dates - move old upcoming date to previous dates
                old_upcoming_date = str(original_row["Upcoming Date"])
                previous_dates = str(original_row["Previous Dates"]) if original_row["Previous Dates"] else ""
                
                # Add old upcoming date to previous dates if not already there
                if previous_dates:
                    previous_dates_list = previous_dates.split("|")
                else:
                    previous_dates_list = []
                
                if old_upcoming_date not in previous_dates_list:
                    previous_dates_list.append(old_upcoming_date)
                
                updated_case_data["Previous Dates"] = "|".join(previous_dates_list)
                updated_case_data["Upcoming Date"] = str(row["Upcoming Date"])
                
                # Update in backend
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} - Previous date moved to history")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        # Check for other changes (Stage, Status, Remarks)
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if any other fields changed
            fields_changed = False
            for col in ["Stage", "Status", "Remarks"]:
                if str(row[col]) != str(original_row[col]):
                    fields_changed = True
                    break
            
            if fields_changed:
                case_id = row["ID"]
                updated_case_data = row.to_dict()
                
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} details")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        st.rerun()  # Refresh the page to show updated data
        
    except Exception as e:
        st.error(f"❌ Error updating cases: {e}")


def update_pending_cases(edited_df, original_df):
    """Update pending cases with previous date handling"""
    from models.database import get_connection
    sheets_service = get_connection()
    
    try:
        # Find changes in the edited dataframe
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if upcoming date changed
            if str(row["Upcoming Date"]) != str(original_row["Upcoming Date"]):
                # Get the case ID
                case_id = row["ID"]
                
                # Prepare the updated case data
                updated_case_data = row.to_dict()
                
                # Handle previous dates - move old upcoming date to previous dates
                old_upcoming_date = str(original_row["Upcoming Date"])
                previous_dates = str(original_row["Previous Dates"]) if original_row["Previous Dates"] else ""
                
                # Add old upcoming date to previous dates if not already there
                if previous_dates:
                    previous_dates_list = previous_dates.split("|")
                else:
                    previous_dates_list = []
                
                if old_upcoming_date not in previous_dates_list:
                    previous_dates_list.append(old_upcoming_date)
                
                updated_case_data["Previous Dates"] = "|".join(previous_dates_list)
                updated_case_data["Upcoming Date"] = str(row["Upcoming Date"])
                
                # Update in backend
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} - Previous date moved to history")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        # Check for other changes (Stage, Status, Remarks)
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if any other fields changed
            fields_changed = False
            for col in ["Stage", "Status", "Remarks"]:
                if str(row[col]) != str(original_row[col]):
                    fields_changed = True
                    break
            
            if fields_changed:
                case_id = row["ID"]
                updated_case_data = row.to_dict()
                
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} details")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        st.rerun()  # Refresh the page to show updated data
        
    except Exception as e:
        st.error(f"❌ Error updating cases: {e}")


def update_date_cases(edited_df, original_df):
    """Update cases by date with previous date handling"""
    from models.database import get_connection
    sheets_service = get_connection()
    
    try:
        # Find changes in the edited dataframe
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if upcoming date changed
            if str(row["Upcoming Date"]) != str(original_row["Upcoming Date"]):
                # Get the case ID
                case_id = row["ID"]
                
                # Prepare the updated case data
                updated_case_data = row.to_dict()
                
                # Handle previous dates - move old upcoming date to previous dates
                old_upcoming_date = str(original_row["Upcoming Date"])
                previous_dates = str(original_row["Previous Dates"]) if original_row["Previous Dates"] else ""
                
                # Add old upcoming date to previous dates if not already there
                if previous_dates:
                    previous_dates_list = previous_dates.split("|")
                else:
                    previous_dates_list = []
                
                if old_upcoming_date not in previous_dates_list:
                    previous_dates_list.append(old_upcoming_date)
                
                updated_case_data["Previous Dates"] = "|".join(previous_dates_list)
                updated_case_data["Upcoming Date"] = str(row["Upcoming Date"])
                
                # Update in backend
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} - Previous date moved to history")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        # Check for other changes (Stage, Status, Remarks)
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if any other fields changed
            fields_changed = False
            for col in ["Stage", "Status", "Remarks"]:
                if str(row[col]) != str(original_row[col]):
                    fields_changed = True
                    break
            
            if fields_changed:
                case_id = row["ID"]
                updated_case_data = row.to_dict()
                
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} details")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        st.rerun()  # Refresh the page to show updated data
        
    except Exception as e:
        st.error(f"❌ Error updating cases: {e}")


def update_today_cases(edited_df, original_df):
    """Update today's cases with previous date handling"""
    from models.database import get_connection
    sheets_service = get_connection()
    
    try:
        # Find changes in the edited dataframe
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if upcoming date changed
            if str(row["Upcoming Date"]) != str(original_row["Upcoming Date"]):
                # Get the case ID
                case_id = row["ID"]
                
                # Prepare the updated case data
                updated_case_data = row.to_dict()
                
                # Handle previous dates - move old upcoming date to previous dates
                old_upcoming_date = str(original_row["Upcoming Date"])
                previous_dates = str(original_row["Previous Dates"]) if original_row["Previous Dates"] else ""
                
                # Add old upcoming date to previous dates if not already there
                if previous_dates:
                    previous_dates_list = previous_dates.split("|")
                else:
                    previous_dates_list = []
                
                if old_upcoming_date not in previous_dates_list:
                    previous_dates_list.append(old_upcoming_date)
                
                updated_case_data["Previous Dates"] = "|".join(previous_dates_list)
                updated_case_data["Upcoming Date"] = str(row["Upcoming Date"])
                
                # Update in backend
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} - Previous date moved to history")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        # Check for other changes (Stage, Status, Remarks)
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if any other fields changed
            fields_changed = False
            for col in ["Stage", "Status", "Remarks"]:
                if str(row[col]) != str(original_row[col]):
                    fields_changed = True
                    break
            
            if fields_changed:
                case_id = row["ID"]
                updated_case_data = row.to_dict()
                
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} details")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        st.rerun()  # Refresh the page to show updated data
        
    except Exception as e:
        st.error(f"❌ Error updating cases: {e}")


def update_search_results(edited_df, original_df):
    """Update search results with previous date handling"""
    from models.database import get_connection
    sheets_service = get_connection()
    
    try:
        # Find changes in the edited dataframe
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if upcoming date changed
            if str(row["Upcoming Date"]) != str(original_row["Upcoming Date"]):
                # Get the case ID
                case_id = row["ID"]
                
                # Prepare the updated case data
                updated_case_data = row.to_dict()
                
                # Handle previous dates - move old upcoming date to previous dates
                old_upcoming_date = str(original_row["Upcoming Date"])
                previous_dates = str(original_row["Previous Dates"]) if original_row["Previous Dates"] else ""
                
                # Add old upcoming date to previous dates if not already there
                if previous_dates:
                    previous_dates_list = previous_dates.split("|")
                else:
                    previous_dates_list = []
                
                if old_upcoming_date not in previous_dates_list:
                    previous_dates_list.append(old_upcoming_date)
                
                updated_case_data["Previous Dates"] = "|".join(previous_dates_list)
                updated_case_data["Upcoming Date"] = str(row["Upcoming Date"])
                
                # Update in backend
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} - Previous date moved to history")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        # Check for other changes (Stage, Status, Remarks)
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if any other fields changed
            fields_changed = False
            for col in ["Stage", "Status", "Remarks"]:
                if str(row[col]) != str(original_row[col]):
                    fields_changed = True
                    break
            
            if fields_changed:
                case_id = row["ID"]
                updated_case_data = row.to_dict()
                
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} details")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        st.rerun()  # Refresh the page to show updated data
        
    except Exception as e:
        st.error(f"❌ Error updating cases: {e}")


def update_upcoming_hearings(edited_df, original_df):
    """Update upcoming hearings with previous date handling"""
    from models.database import get_connection
    sheets_service = get_connection()
    
    try:
        # Find changes in the edited dataframe
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if upcoming date changed
            if str(row["Upcoming Date"]) != str(original_row["Upcoming Date"]):
                # Get the case ID
                case_id = row["ID"]
                
                # Prepare the updated case data
                updated_case_data = row.to_dict()
                
                # Handle previous dates - move old upcoming date to previous dates
                old_upcoming_date = str(original_row["Upcoming Date"])
                previous_dates = str(original_row["Previous Dates"]) if original_row["Previous Dates"] else ""
                
                # Add old upcoming date to previous dates if not already there
                if previous_dates:
                    previous_dates_list = previous_dates.split("|")
                else:
                    previous_dates_list = []
                
                if old_upcoming_date not in previous_dates_list:
                    previous_dates_list.append(old_upcoming_date)
                
                updated_case_data["Previous Dates"] = "|".join(previous_dates_list)
                updated_case_data["Upcoming Date"] = str(row["Upcoming Date"])
                
                # Update in backend
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} - Previous date moved to history")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        # Check for other changes (Stage, Status, Remarks)
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            
            # Check if any other fields changed
            fields_changed = False
            for col in ["Stage", "Status", "Remarks"]:
                if str(row[col]) != str(original_row[col]):
                    fields_changed = True
                    break
            
            if fields_changed:
                case_id = row["ID"]
                updated_case_data = row.to_dict()
                
                if sheets_service.update_case(case_id, updated_case_data):
                    st.success(f"✅ Updated case {row['Case Number']} details")
                else:
                    st.error(f"❌ Failed to update case {row['Case Number']}")
        
        st.rerun()  # Refresh the page to show updated data
        
    except Exception as e:
        st.error(f"❌ Error updating cases: {e}")


def render_upcoming_detailed(df: pd.DataFrame):
    """Render upcoming hearings with all case details"""
    # Use the same header style as Dashboard
    st.markdown("""
    <div class="app-header" style="margin-top: 1rem;">
        <div class="app-title">📅 Upcoming Hearings</div>
        <div class="app-subtitle">All scheduled court proceedings with complete details</div>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No cases available.")
    else:
        today = date.today()
        dff = df.copy()
        # Handle null values in Upcoming Date column
        dff["Upcoming Date"] = dff["Upcoming Date"].fillna("").apply(parse_date)
        dff = dff[dff["Upcoming Date"] >= today].sort_values("Upcoming Date")
        
        if dff.empty:
            st.info("No upcoming hearings scheduled.")
        else:
            # Add filtering options
            st.markdown("### 🔍 Filter Cases")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_filter = st.selectbox("Status", ["All"] + list(dff["Status"].unique()), key="status_filter_upcoming")
            with col2:
                location_filter = st.selectbox("Location", ["All"] + list(dff["Location"].unique()), key="location_filter_upcoming")
            with col3:
                company_filter = st.selectbox("Company", ["All"] + list(dff["Company Name"].unique()), key="company_filter_upcoming")
            
            # Apply filters
            filtered_df = dff.copy()
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df["Status"] == status_filter]
            if location_filter != "All":
                filtered_df = filtered_df[filtered_df["Location"] == location_filter]
            if company_filter != "All":
                filtered_df = filtered_df[filtered_df["Company Name"] == company_filter]
            
            st.markdown(f"**Showing {len(filtered_df)} of {len(dff)} cases**")
            
            # Show filtered data with edit functionality
            if not filtered_df.empty:
                # Use data_editor for inline editing
                edited_df = st.data_editor(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Upcoming Date": st.column_config.DateColumn(
                            "Upcoming Date",
                            help="Click to edit the upcoming hearing date",
                            format="YYYY-MM-DD",
                            step=1,
                        ),
                        "Stage": st.column_config.TextColumn(
                            "Stage",
                            help="Current stage of the case",
                            max_chars=50,
                        ),
                        "Status": st.column_config.SelectboxColumn(
                            "Status",
                            help="Case status",
                            options=["OPEN", "COMPROMISED", "DD", "AWARD"],
                        ),
                        "Remarks": st.column_config.TextColumn(
                            "Remarks",
                            help="Additional remarks",
                            max_chars=200,
                        ),
                    },
                    disabled=["ID", "Case Number", "Case Title", "Case Type", "Location", "Company Name", "Previous Dates", "Claimant Advocate Name", "Claimant Advocate Mobile Number"],
                    num_rows="fixed",
                    key="upcoming_hearings_editor"
                )
                
                # Update button
                if st.button("💾 Save Changes", key="save_upcoming_changes"):
                    update_upcoming_hearings(edited_df, dff)
            else:
                st.info("No cases match the current filters.")


def render_case_overview(df: pd.DataFrame):
    st.markdown("""
    <div class="card-header">
        <div class="card-title">📋 Case Overview</div>
        <div class="card-subtitle">Complete list of all cases in your practice</div>
    </div>
    """, unsafe_allow_html=True)
    if df.empty:
        st.info("No cases available.")
    else:
        dfv = df.copy()
        # Handle null values in Status column
        dfv["Status"] = dfv["Status"].fillna("OPEN")
        
        # status badge column rendered as markdown
        STATUS_COLOR = {
            "OPEN": "blue",
            "COMPROMISED": "yellow",
            "AWARD": "green",
            "DD": "red",
        }
        dfv["Status Tag"] = dfv["Status"].apply(lambda s: badge(s, STATUS_COLOR.get(s.upper(), "blue")))
        st.dataframe(
            dfv[["Case Number","Case Title","Upcoming Date","Status","Company Name","Location"]],
            use_container_width=True,
            hide_index=True,
        )


def page_dashboard(df: pd.DataFrame):
    # Page header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">📊 Dashboard</div>
        <div class="app-subtitle">Overview of your legal practice and case management</div>
    </div>
    """, unsafe_allow_html=True)
    
    render_metrics(df)
    
    # Show upcoming hearings with all details
    render_upcoming_detailed(df)


def page_add_case(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">➕ Add New Case</div>
        <div class="app-subtitle">Enter case details to add a new legal matter to your practice</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("add_case"):
        st.markdown("### Case Information")
        c1, c2 = st.columns(2)
        case_number = c1.text_input("Case Number", placeholder="Enter case number")
        case_title = c2.text_input("Case Title", placeholder="Enter case title")
        
        st.markdown("### Case Details")
        c1, c2 = st.columns(2)
        ctype = c1.selectbox("Case Type", ["MACT","WCC","DCF","PLA"])
        location = c2.selectbox("Location", ["Farrukhabad","Kanpur Nagar - North","Kanpur Nagar - South","Kannauj"])        
        company = c1.text_input("Company Name", placeholder="Enter company name")
        upcoming = c2.date_input("Upcoming Hearing Date", value=date.today())
        stage = c1.text_input("Stage", placeholder="Enter current stage")
        status = c2.selectbox("Status", ["OPEN","COMPROMISED","DD","AWARD"], index=0)
        
        st.markdown("### Advocate Information")
        c1, c2 = st.columns(2)
        adv_name = c1.text_input("Claimant Advocate Name", placeholder="Enter advocate name")
        adv_mobile = c2.text_input("Claimant Advocate Mobile Number", placeholder="Enter mobile number")
        
        st.markdown("### Additional Information")
        remarks = st.text_area("Remarks", placeholder="Enter any additional remarks or notes")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("💾 Save Case", use_container_width=True)
    
    if submitted:
        if not case_number or not case_title:
            st.error("Case Number and Case Title are required.")
            return
        
        # Check if case number already exists for this location
        from models.database import get_connection
        sheets_service = get_connection()
        if sheets_service.case_number_exists(case_number, location):
            st.warning("A case with this Case Number already exists for this location.")
            return
        
        # Prepare case data
        case_data = {
            "Case Number": case_number,
            "Case Title": case_title,
            "Case Type": ctype,
            "Location": location,
            "Company Name": company or "",
            "Upcoming Date": upcoming.isoformat(),
            "Previous Dates": "",
            "Stage": stage,
            "Remarks": remarks,
            "Status": status,
            "Claimant Advocate Name": adv_name,
            "Claimant Advocate Mobile Number": adv_mobile,
        }
        
        # Add case to backend
        if sheets_service.add_case(case_data):
            st.success("✅ Case added successfully!")
            st.rerun()  # Refresh the page to show updated data
        else:
            st.error("❌ Failed to add case. Please try again.")


def page_search(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🔍 Search Cases</div>
        <div class="app-subtitle">Find specific cases using various search criteria</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Search Criteria")
    q1, q2, q3 = st.columns(3)
    num = q1.text_input("Case Number", placeholder="Enter case number")
    title = q2.text_input("Case Title contains", placeholder="Enter title keywords")
    company = q3.text_input("Company Name contains", placeholder="Enter company name")
    
    # Use backend search if specific criteria are provided
    search_results = []
    if num or title or company:
        from models.database import get_connection
        sheets_service = get_connection()
        
        if num:
            search_results = sheets_service.search_by_case_number(num)
        elif title:
            search_results = sheets_service.search_by_case_title(title)
        elif company:
            search_results = sheets_service.search_by_company_name(company)
        
        # Convert to DataFrame
        if search_results:
            dff = pd.DataFrame(search_results)
        else:
            dff = pd.DataFrame(columns=df.columns)
    else:
        # Show all cases if no search criteria
        dff = df.copy()
    
    st.markdown("### Search Results")
    if len(dff) == 0:
        st.info("No cases found matching your search criteria.")
    else:
        # Add filtering options for search results
        st.markdown("#### 🔍 Filter Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_status_filter = st.selectbox("Status", ["All"] + list(dff["Status"].unique()), key="search_status_filter")
        with col2:
            search_location_filter = st.selectbox("Location", ["All"] + list(dff["Location"].unique()), key="search_location_filter")
        with col3:
            search_company_filter = st.selectbox("Company", ["All"] + list(dff["Company Name"].unique()), key="search_company_filter")
        
        # Apply filters
        filtered_search_df = dff.copy()
        if search_status_filter != "All":
            filtered_search_df = filtered_search_df[filtered_search_df["Status"] == search_status_filter]
        if search_location_filter != "All":
            filtered_search_df = filtered_search_df[filtered_search_df["Location"] == search_location_filter]
        if search_company_filter != "All":
            filtered_search_df = filtered_search_df[filtered_search_df["Company Name"] == search_company_filter]
        
        st.markdown(f"**Showing {len(filtered_search_df)} of {len(dff)} results**")
        
        # Add CSV download button
        csv_data = filtered_search_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_search_csv"
        )
        
        # Show filtered data with edit functionality
        if not filtered_search_df.empty:
            # Convert date columns to proper date format for editing
            edit_df = filtered_search_df.copy()
            if 'Upcoming Date' in edit_df.columns:
                edit_df['Upcoming Date'] = edit_df['Upcoming Date'].apply(parse_date)
            
            # Use data_editor for inline editing
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Upcoming Date": st.column_config.DateColumn(
                        "Upcoming Date",
                        help="Click to edit the upcoming hearing date",
                        format="YYYY-MM-DD",
                        step=1,
                    ),
                    "Stage": st.column_config.TextColumn(
                        "Stage",
                        help="Current stage of the case",
                        max_chars=50,
                    ),
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        help="Case status",
                        options=["OPEN", "COMPROMISED", "DD", "AWARD"],
                    ),
                    "Remarks": st.column_config.TextColumn(
                        "Remarks",
                        help="Additional remarks",
                        max_chars=200,
                    ),
                },
                disabled=["ID", "Case Number", "Case Title", "Case Type", "Location", "Company Name", "Previous Dates", "Claimant Advocate Name", "Claimant Advocate Mobile Number"],
                num_rows="fixed",
                key="search_results_editor"
            )
            
            # Update button
            if st.button("💾 Save Changes", key="save_search_changes"):
                update_search_results(edited_df, filtered_search_df)


def page_today(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">📅 Today's Cases</div>
        <div class="app-subtitle">Cases scheduled for today's court proceedings</div>
    </div>
    """, unsafe_allow_html=True)
    
    from models.database import get_connection
    sheets_service = get_connection()
    today_cases = sheets_service.get_todays_case_list()
    
    if not today_cases:
        st.info("No cases scheduled for today.")
    else:
        dff = pd.DataFrame(today_cases)
        
        # Add filtering options
        st.markdown("#### 🔍 Filter Today's Cases")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            today_status_filter = st.selectbox("Status", ["All"] + list(dff["Status"].unique()), key="today_status_filter")
        with col2:
            today_location_filter = st.selectbox("Location", ["All"] + list(dff["Location"].unique()), key="today_location_filter")
        with col3:
            today_company_filter = st.selectbox("Company", ["All"] + list(dff["Company Name"].unique()), key="today_company_filter")
        
        # Apply filters
        filtered_today_df = dff.copy()
        if today_status_filter != "All":
            filtered_today_df = filtered_today_df[filtered_today_df["Status"] == today_status_filter]
        if today_location_filter != "All":
            filtered_today_df = filtered_today_df[filtered_today_df["Location"] == today_location_filter]
        if today_company_filter != "All":
            filtered_today_df = filtered_today_df[filtered_today_df["Company Name"] == today_company_filter]
        
        st.markdown(f"**Showing {len(filtered_today_df)} of {len(dff)} cases**")
        
        # Add CSV download button
        csv_data = filtered_today_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"todays_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_today_csv"
        )
        
        # Show filtered data with edit functionality
        if not filtered_today_df.empty:
            # Convert date columns to proper date format for editing
            edit_df = filtered_today_df.copy()
            if 'Upcoming Date' in edit_df.columns:
                edit_df['Upcoming Date'] = edit_df['Upcoming Date'].apply(parse_date)
            
            # Use data_editor for inline editing
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Upcoming Date": st.column_config.DateColumn(
                        "Upcoming Date",
                        help="Click to edit the upcoming hearing date",
                        format="YYYY-MM-DD",
                        step=1,
                    ),
                    "Stage": st.column_config.TextColumn(
                        "Stage",
                        help="Current stage of the case",
                        max_chars=50,
                    ),
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        help="Case status",
                        options=["OPEN", "COMPROMISED", "DD", "AWARD"],
                    ),
                    "Remarks": st.column_config.TextColumn(
                        "Remarks",
                        help="Additional remarks",
                        max_chars=200,
                    ),
                },
                disabled=["ID", "Case Number", "Case Title", "Case Type", "Location", "Company Name", "Previous Dates", "Claimant Advocate Name", "Claimant Advocate Mobile Number"],
                num_rows="fixed",
                key="today_cases_editor"
            )
            
            # Update button
            if st.button("💾 Save Changes", key="save_today_changes"):
                update_today_cases(edited_df, filtered_today_df)


def page_by_date(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">📆 Cases by Date</div>
        <div class="app-subtitle">View cases scheduled for a specific date</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Select Date")
    dt = st.date_input("Choose a date", value=date.today())
    
    from models.database import get_connection
    sheets_service = get_connection()
    cases_by_date = sheets_service.get_cases_by_date(dt)
    
    st.markdown("### Cases for Selected Date")
    if not cases_by_date:
        st.info(f"No cases scheduled for {dt.strftime('%B %d, %Y')}.")
    else:
        dff = pd.DataFrame(cases_by_date)
        
        # Add CSV download button
        csv_data = dff.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"cases_by_date_{dt.strftime('%Y%m%d')}_{datetime.now().strftime('%H%M%S')}.csv",
            mime="text/csv",
            key="download_date_csv"
        )
        
        # Show data with edit functionality
        if not dff.empty:
            # Convert date columns to proper date format for editing
            edit_df = dff.copy()
            if 'Upcoming Date' in edit_df.columns:
                edit_df['Upcoming Date'] = edit_df['Upcoming Date'].apply(parse_date)
            
            # Use data_editor for inline editing
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Upcoming Date": st.column_config.DateColumn(
                        "Upcoming Date",
                        help="Click to edit the upcoming hearing date",
                        format="YYYY-MM-DD",
                        step=1,
                    ),
                    "Stage": st.column_config.TextColumn(
                        "Stage",
                        help="Current stage of the case",
                        max_chars=50,
                    ),
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        help="Case status",
                        options=["OPEN", "COMPROMISED", "DD", "AWARD"],
                    ),
                    "Remarks": st.column_config.TextColumn(
                        "Remarks",
                        help="Additional remarks",
                        max_chars=200,
                    ),
                },
                disabled=["ID", "Case Number", "Case Title", "Case Type", "Location", "Company Name", "Previous Dates", "Claimant Advocate Name", "Claimant Advocate Mobile Number"],
                num_rows="fixed",
                key="date_cases_editor"
            )
            
            # Update button
            if st.button("💾 Save Changes", key="save_date_changes"):
                update_date_cases(edited_df, dff)


def page_pending(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">⏳ Pending Cases</div>
        <div class="app-subtitle">All cases with OPEN status requiring attention</div>
    </div>
    """, unsafe_allow_html=True)
    
    from models.database import get_connection
    sheets_service = get_connection()
    pending_cases = sheets_service.get_pending_cases()
    
    if not pending_cases:
        st.info("No pending cases found.")
    else:
        dff = pd.DataFrame(pending_cases)
        
        # Add CSV download button
        csv_data = dff.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"pending_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_pending_csv"
        )
        
        # Show data with edit functionality
        if not dff.empty:
            # Convert date columns to proper date format for editing
            edit_df = dff.copy()
            if 'Upcoming Date' in edit_df.columns:
                edit_df['Upcoming Date'] = edit_df['Upcoming Date'].apply(parse_date)
            
            # Use data_editor for inline editing
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Upcoming Date": st.column_config.DateColumn(
                        "Upcoming Date",
                        help="Click to edit the upcoming hearing date",
                        format="YYYY-MM-DD",
                        step=1,
                    ),
                    "Stage": st.column_config.TextColumn(
                        "Stage",
                        help="Current stage of the case",
                        max_chars=50,
                    ),
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        help="Case status",
                        options=["OPEN", "COMPROMISED", "DD", "AWARD"],
                    ),
                    "Remarks": st.column_config.TextColumn(
                        "Remarks",
                        help="Additional remarks",
                        max_chars=200,
                    ),
                },
                disabled=["ID", "Case Number", "Case Title", "Case Type", "Location", "Company Name", "Previous Dates", "Claimant Advocate Name", "Claimant Advocate Mobile Number"],
                num_rows="fixed",
                key="pending_cases_editor"
            )
            
            # Update button
            if st.button("💾 Save Changes", key="save_pending_changes"):
                update_pending_cases(edited_df, dff)


def page_by_company(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🏢 Cases by Company</div>
        <div class="app-subtitle">View all cases associated with a specific company</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get unique companies from the data
    companies = sorted([c for c in df["Company Name"].dropna().unique() if c])
    
    if not companies:
        st.info("No companies found in the database.")
    else:
        st.markdown("### Select Company")
        comp = st.selectbox("Choose a company", options=companies)
        
        from models.database import get_connection
        sheets_service = get_connection()
        company_cases = sheets_service.search_by_company_name(comp)
        
        st.markdown("### Cases for Selected Company")
        if not company_cases:
            st.info(f"No cases found for {comp}.")
        else:
            dff = pd.DataFrame(company_cases)
            
            # Add CSV download button
            csv_data = dff.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"company_cases_{comp.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_company_csv"
            )
            
            # Show data with edit functionality
            if not dff.empty:
                # Convert date columns to proper date format for editing
                edit_df = dff.copy()
                if 'Upcoming Date' in edit_df.columns:
                    edit_df['Upcoming Date'] = edit_df['Upcoming Date'].apply(parse_date)
                
                # Use data_editor for inline editing
                edited_df = st.data_editor(
                    edit_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Upcoming Date": st.column_config.DateColumn(
                            "Upcoming Date",
                            help="Click to edit the upcoming hearing date",
                            format="YYYY-MM-DD",
                            step=1,
                        ),
                        "Stage": st.column_config.TextColumn(
                            "Stage",
                            help="Current stage of the case",
                            max_chars=50,
                        ),
                        "Status": st.column_config.SelectboxColumn(
                            "Status",
                            help="Case status",
                            options=["OPEN", "COMPROMISED", "DD", "AWARD"],
                        ),
                        "Remarks": st.column_config.TextColumn(
                            "Remarks",
                            help="Additional remarks",
                            max_chars=200,
                        ),
                    },
                    disabled=["ID", "Case Number", "Case Title", "Case Type", "Location", "Company Name", "Previous Dates", "Claimant Advocate Name", "Claimant Advocate Mobile Number"],
                    num_rows="fixed",
                    key="company_cases_editor"
                )
                
                # Update button
                if st.button("💾 Save Changes", key="save_company_changes"):
                    update_company_cases(edited_df, dff)


def _timeline(previous: str) -> pd.DataFrame:
    # previous dates stored as pipe-separated ISO strings for the mock
    if not previous:
        return pd.DataFrame(columns=["Date","Stage","Remarks"])
    rows = []
    for token in previous.split("|"):
        if not token: continue
        rows.append({"Date": parse_date(token), "Stage": "", "Remarks": ""})
    return pd.DataFrame(rows).sort_values("Date", ascending=False)


def page_case_details(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">📋 Case Details</div>
        <div class="app-subtitle">View detailed information about a specific case</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Select Case")
    numbers = df["Case Number"].tolist()
    
    if not numbers:
        st.info("No cases available to view.")
        return
    
    selected = st.selectbox("Choose a case number", numbers)
    
    # Get case details from backend
    from models.database import get_connection
    sheets_service = get_connection()
    case_data = sheets_service.get_case_by_number_or_title(selected)
    
    if not case_data:
        st.error("Case not found.")
        return
    
    row = case_data

    # Header Card
    st.markdown("""
    <div class="card-header">
        <div class="card-title">Case Information</div>
    </div>
    """, unsafe_allow_html=True)
    
    left, right = st.columns([3,1])
    with left:
        CASE_TYPE_COLOR = {
            "MACT": "mact", "WCC": "wcc", "DCF": "dcf", "PLA": "pla"
        }
        STATUS_COLOR = {
            "OPEN": "open",
            "COMPROMISED": "compromised",
            "AWARD": "award",
            "DD": "dd",
        }
        st.markdown(f"""
        <h3 style='margin-bottom:6px;'>{row['Case Number']} &nbsp; {row['Case Title']}</h3>
        <div style='color: var(--text-secondary); margin-bottom: 1rem;'>{row['Company Name']}</div>
        <div style='margin-top:8px;'>
            {badge(row['Case Type'], CASE_TYPE_COLOR.get(row['Case Type'], 'mact'))}
            {badge(row['Status'], STATUS_COLOR.get(row['Status'], 'open'))}
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("**Upcoming Hearing**")
        st.write(parse_date(row["Upcoming Date"]).strftime("%b %d, %Y"))

    # Details Card
    st.markdown("""
    <div class="card-header">
        <div class="card-title">Case Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Location**")
        st.write(row["Location"])
        st.markdown("**Advocate Name**")
        st.write(row["Claimant Advocate Name"])
        st.markdown("**Advocate Mobile**")
        st.write(row["Claimant Advocate Mobile Number"])
    with c2:
        st.markdown("**Stage**")
        st.write(row["Stage"])
        st.markdown("**Remarks**")
        st.write(row["Remarks"] or "—")
        st.markdown("**Previous Hearing Dates**")
        st.dataframe(_timeline(row["Previous Dates"]), use_container_width=True, hide_index=True)

    # Action Bar
    st.markdown("""
    <div class="card-header">
        <div class="card-title">Actions</div>
    </div>
    """, unsafe_allow_html=True)
    
    colA, colB, colC, colD = st.columns(4)
    if colA.button("✍️ Update Case", use_container_width=True):
        st.session_state["nav"] = "Update Case"
        st.session_state["edit_case"] = row["ID"]
        st.rerun()
    if colB.button("📅 Add Hearing Date", use_container_width=True):
        st.session_state["nav"] = "Update Case"
        st.session_state["edit_case"] = row["ID"]
        st.rerun()
    if colC.button("📝 Add Remarks", use_container_width=True):
        st.session_state["nav"] = "Update Case"
        st.session_state["edit_case"] = row["ID"]
        st.rerun()
    if colD.button("✅ Close Case", use_container_width=True):
        from models.database import get_connection
        sheets_service = get_connection()
        
        # Update case status to AWARD
        case_data = row.copy()
        case_data["Status"] = "AWARD"
        
        if sheets_service.update_case(row["ID"], case_data):
            st.success("✅ Case marked as closed (AWARD).")
            st.rerun()
        else:
            st.error("❌ Failed to update case status.")


def page_update_case(df: pd.DataFrame):
    st.markdown("""
    <div class="app-header">
        <div class="app-title">✏️ Update Case</div>
        <div class="app-subtitle">Modify case information and status</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Select Case to Update")
    
    # Get case numbers from backend
    numbers = df["Case Number"].tolist()
    if not numbers:
        st.info("No cases available to update.")
        return
    
    # Select the case to edit
    edit_id = st.session_state.get("edit_case")
    if edit_id:
        # Find case by ID
        from models.database import get_connection
        sheets_service = get_connection()
        case_data = None
        for case in sheets_service._get_all_records():
            if case.get("ID") == edit_id:
                case_data = case
                break
        if case_data:
            default_num = case_data["Case Number"]
        else:
            default_num = numbers[0]
    else:
        default_num = numbers[0]
    
    case_num = st.selectbox("Choose a case number", numbers, index=numbers.index(default_num) if default_num in numbers else 0)
    
    # Get case details from backend
    from models.database import get_connection
    sheets_service = get_connection()
    case_data = sheets_service.get_case_by_number_or_title(case_num)
    
    if not case_data:
        st.error("Case not found.")
        return
    
    row = case_data

    st.markdown("### Update Case Information")
    with st.form("update_case"):
        c1, c2 = st.columns(2)
        with c1:
            up_date = st.date_input("Upcoming Hearing Date", value=parse_date(row["Upcoming Date"]))
            stage = st.text_input("Stage", value=row["Stage"], placeholder="Enter current stage")
        with c2:
            status = st.selectbox("Status", ["OPEN","COMPROMISED","DD","AWARD"], index=["OPEN","COMPROMISED","DD","AWARD"].index(row["Status"]))
        add_prev = st.checkbox("Append current upcoming date to Previous Dates before updating", value=True)
        
        remarks = st.text_area("Remarks", value=row["Remarks"], placeholder="Enter any additional remarks")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("💾 Save Updates", use_container_width=True)

    if submitted:
        # Prepare updated case data
        updated_case_data = row.copy()
        updated_case_data["Upcoming Date"] = up_date.isoformat()
        updated_case_data["Stage"] = stage
        updated_case_data["Status"] = status
        updated_case_data["Remarks"] = remarks
        
        # Handle previous dates
        if add_prev:
            prev_list = [p for p in (row["Previous Dates"] or "").split("|") if p]
            current_up = parse_date(row["Upcoming Date"]).isoformat()
            if current_up not in prev_list:
                prev_list.append(current_up)
            updated_case_data["Previous Dates"] = "|".join(prev_list)
        
        # Update case in backend
        if sheets_service.update_case(row["ID"], updated_case_data):
            st.success("✅ Case updated successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to update case. Please try again.")


def get_cases_data():
    """Get cases data from backend (Google Sheets or mock data)"""
    from models.database import get_connection
    
    try:
        # Get data from Google Sheets service
        sheets_service = get_connection()
        records = sheets_service._get_all_records()
        
        if not records:
            # If no records, return empty DataFrame
            columns = [
                "ID","Case Number","Case Title","Case Type","Location","Company Name",
                "Upcoming Date","Previous Dates","Stage","Remarks","Status",
                "Claimant Advocate Name","Claimant Advocate Mobile Number"
            ]
            return pd.DataFrame(columns=columns)
        
        # Convert records to DataFrame
        df = pd.DataFrame(records)
        
        # Ensure all required columns exist
        required_columns = [
            "ID","Case Number","Case Title","Case Type","Location","Company Name",
            "Upcoming Date","Previous Dates","Stage","Remarks","Status",
            "Claimant Advocate Name","Claimant Advocate Mobile Number"
        ]
        
        for col in required_columns:
            if col not in df.columns:
                df[col] = ""
        
        # Clean the data - replace None values with empty strings
        df = df.fillna("")
        
        # Reorder columns to match expected format
        df = df[required_columns]
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return empty DataFrame on error
        columns = [
            "ID","Case Number","Case Title","Case Type","Location","Company Name",
            "Upcoming Date","Previous Dates","Stage","Remarks","Status",
            "Claimant Advocate Name","Claimant Advocate Mobile Number"
        ]
        return pd.DataFrame(columns=columns)


def main():
    set_custom_style()
    
    # allow programmatic nav
    if "nav" not in st.session_state:
        st.session_state.nav = "Dashboard"

    sel = sidebar_nav()
    if sel != st.session_state.nav:
        st.session_state.nav = sel

    page = st.session_state.nav
    df = get_cases_data()

    if page == "Dashboard":
        page_dashboard(df)
    elif page == "Add Case":
        page_add_case(df)
    elif page == "Search Case":
        page_search(df)
    elif page == "Today's Cases":
        page_today(df)
    elif page == "By Date":
        page_by_date(df)
    elif page == "Pending Cases":
        page_pending(df)
    elif page == "By Company":
        page_by_company(df)
    elif page == "Case Details":
        page_case_details(df)
    elif page == "Update Case":
        page_update_case(df)


if __name__ == "__main__":
    main()
