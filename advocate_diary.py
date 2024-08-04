import streamlit as st
from datetime import date, timedelta
import psycopg2
import pandas as pd
import logging

def get_config():
    return {
        "database": {
            "host": st.secrets["database"]["host"],
            "port": st.secrets["database"]["port"],
            "database": st.secrets["database"]["database"],
            "user": st.secrets["database"]["user"],
            "password": st.secrets["database"]["password"]
        },
        "table_name": "case_records",
        "locations": ["Farrukhabad", "Kanpur Nagar - North", "Kanpur Nagar - South", "Kannauj"],
        "case_types": ["MACT", "WCC", "DCF", "PLA"],
        "company_names": ["BAGIC", "SGIC", "OIC", "UIIC", "NIC", "ICICI", "UNIVERSAL", "MAGMA", "TAGIC", "CHOLA MS", "FUTURE", "KOTAK", "ACKO", "SBI", "HDFC", "RELIANCE", "LIBERTY", "IFFCO", "ZUNO"],
        "statuses": ["OPEN", "COMPROMISED", "DD", "AWARD"],
        "headers": ["ID", "Case Number", "Case Title", "Case Type", "Location", "Company Name", "Upcoming Date", "Previous Dates", "Stage", "Remarks", "Status", "Claimant Advocate Name", "Claimant Advocate Mobile Number"],
        "editableHeaders": ["Upcoming Date", "Stage"]
    }

def get_connection(config):
    return psycopg2.connect(
        host=config['database']['host'],
        port=config['database']['port'],
        database=config['database']['database'],
        user=config['database']['user'],
        password=config['database']['password']
    )

# Function to search cases by case number
def search_by_case_number(case_number, config):
    conn = get_connection(config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {config['table_name']} WHERE case_number = %s", (case_number,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Function to search cases by case title
def search_by_case_title(case_title, config):
    conn = get_connection(config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {config['table_name']} WHERE case_title ILIKE %s", ('%' + case_title + '%',))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Function to check if case number already exists for a given location
def case_number_exists(case_number, location, config):
    conn = get_connection(config)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM {config['table_name']} WHERE case_number = %s AND location = %s", (case_number, location))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists

# Function to get today's case list
def get_todays_case_list(config):
    today = date.today()
    conn = get_connection(config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {config['table_name']} WHERE upcoming_date = %s", (today,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Function to get cases by a specific date
def get_cases_by_date(selected_date, config):
    conn = get_connection(config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {config['table_name']} WHERE upcoming_date = %s", (selected_date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Function to get pending cases
def get_pending_cases(config):
    today = date.today()
    conn = get_connection(config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {config['table_name']} WHERE upcoming_date <= %s", (today,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_case_data(case_data, config):

    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Print case_data
    logger.debug(f"Case data: {case_data}")
    try:
        conn = get_connection(config)
        cur = conn.cursor()

        for _, row in case_data.iterrows():
            update_query = f"""
                UPDATE {config['table_name']} SET
                    case_number = %s,
                    case_title = %s,
                    case_type = %s,
                    location = %s,
                    company_name = %s,
                    upcoming_date = %s,
                    previous_dates = %s,
                    stage = %s,
                    remarks = %s,
                    status = %s,
                    claimant_advocate_name = %s,
                    claimant_advocate_mobile_number = %s
                WHERE id = %s
            """
            cur.execute(update_query, (
                row["Case Number"], row["Case Title"], row["Case Type"], row["Location"],
                row["Company Name"], row["Upcoming Date"], row["Previous Dates"], row["Stage"],
                row["Remarks"], row["Status"], row["Claimant Advocate Name"],
                row["Claimant Advocate Mobile Number"], row["ID"]
            ))

        conn.commit()
        cur.close()
        conn.close()
        st.success("Cases updated successfully!")
    except Exception as e:
        st.error(f"Error updating cases: {e}")


# Main function to run the app
def main():
    config = get_config()

    # Set page layout to wide mode
    st.set_page_config(layout="wide")

    st.title("Case Management System")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.button("Add New Case", on_click=lambda: st.session_state.update(page="add_case"))
        st.button("Search Case", on_click=lambda: st.session_state.update(page="search_case"))
        st.button("Today's Case List", on_click=lambda: st.session_state.update(page="todays_case_list"))
        st.button("Cases by Date", on_click=lambda: st.session_state.update(page="cases_by_date"))
        st.button("Pending Cases", on_click=lambda: st.session_state.update(page="pending_cases"))

    if st.session_state.page == "add_case":
        add_new_case(config)

    if st.session_state.page == "search_case":
        search_case(config)
    
    if st.session_state.page == "todays_case_list":
        todays_case_list(config)
    
    if st.session_state.page == "cases_by_date":
        cases_by_date(config)
    
    if st.session_state.page == "pending_cases":
        pending_cases(config)

# Function to handle adding a new case
def add_new_case(config):
    st.header("Add New Case")

    validation_errors = {}

    def validate(field_name, value, required=True):
        if required and not value:
            validation_errors[field_name] = f"{field_name} is required."
        else:
            validation_errors.pop(field_name, None)

    col1, col2 = st.columns(2)

    with col1:
        case_number = st.text_input("Case Number", max_chars=10, key="case_number")
        case_title = st.text_input("Case Title", max_chars=255, key="case_title")
        case_type = st.selectbox("Case Type", config['case_types'], key="case_type")
        location = st.selectbox("Location", config['locations'], key="location")
        company_name = st.selectbox("Company Name", config['company_names'], key="company_name")
        upcoming_date = st.date_input("Upcoming Date", key="upcoming_date")
        stage = st.text_input("Stage", max_chars=50, key="stage")
        status = st.selectbox("Status", config['statuses'], key="status")
        claimant_advocate_name = st.text_input("Claimant Advocate Name", max_chars=100, key="claimant_advocate_name")
        claimant_advocate_mobile_number = st.text_input("Claimant Advocate Mobile Number", max_chars=15, key="claimant_advocate_mobile_number")
        remarks = st.text_area("Remarks", key="remarks")

    with col2:
        for field, error in validation_errors.items():
            st.error(error)

    if st.button("Submit"):
        validate("Case Number", case_number)
        validate("Case Title", case_title)

        if validation_errors:
            with col2:
                for field, error in validation_errors.items():
                    st.error(error)
            st.error("Please fix the errors above.")
        else:
            if case_number_exists(case_number, location, config):
                st.error("Case number already exists for the selected location")
            else:
                try:
                    conn = get_connection(config)
                    cur = conn.cursor()
                    insert_query = f"""
                        INSERT INTO {config['table_name']} (
                            case_number, case_title, case_type, location, company_name, 
                            upcoming_date, stage, remarks, status, 
                            claimant_advocate_name, claimant_advocate_mobile_number
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    parameters = (
                        case_number, case_title, case_type, location, company_name, 
                        upcoming_date, stage, remarks, status, 
                        claimant_advocate_name, claimant_advocate_mobile_number
                    )
                    cur.execute(insert_query, parameters)
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("Case added successfully!")
                except Exception as e:
                    st.error(f"Error adding case: {e}")

    st.button("Go to Main Page", on_click=lambda: st.session_state.update(page="home"))

def search_case(config):
    st.header("Search Case")

    search_criteria = st.selectbox("Search Case By", ["Case Number", "Case Title"])
    search_query = st.text_input(f"Enter {search_criteria}", "")

    if st.button("Search"):
        if search_criteria == "Case Number":
            cases = search_by_case_number(search_query, config)
        else:
            cases = search_by_case_title(search_query, config)

        if not cases:
            st.write("No cases found.")
        else:
            st.write("Case Details:")
            df_cases = pd.DataFrame(cases, columns=config['headers'])
            st.session_state.df_value = df_cases

    if "df_value" in st.session_state:
        df_cases = st.session_state.df_value

        # Create a column_config dictionary to disable all columns except "Upcoming Date" and "Stage"
        column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if col not in ["Upcoming Date", "Stage"]}

        # Display editable DataFrame with column configuration
        edited_df = st.data_editor(
            df_cases,
            num_rows="fixed",
            column_config=column_config,
        )

        # Check if the data_editor was edited
        if st.button("Update Cases"):
            if edited_df is not None:
                update_case_data(edited_df, config)
                st.session_state.df_value = edited_df
            else:
                st.write("No changes detected.")

    st.button("Go to Main Page", on_click=lambda: st.session_state.update(page="home"))

def todays_case_list(config):
    st.header("Today's Case List")

    cases = get_todays_case_list(config)

    if not cases:
        st.write("No cases scheduled for today.")
    else:
        st.write("Today's Case List:")
        df_cases = pd.DataFrame(cases, columns=config['headers'])
        st.session_state.df_value = df_cases

    if "df_value" in st.session_state:
        df_cases = st.session_state.df_value

        # Create a column_config dictionary to disable all columns except "Upcoming Date" and "Stage"
        column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if col not in ["Upcoming Date", "Stage"]}

        # Display editable DataFrame with column configuration
        edited_df = st.data_editor(
            df_cases,
            num_rows="fixed",
            column_config=column_config,
        )

        # Check if the data_editor was edited
        if st.button("Update Cases"):
            if edited_df is not None:
                update_case_data(edited_df, config)
                st.session_state.df_value = edited_df
            else:
                st.write("No changes detected.")

    st.button("Go to Main Page", on_click=lambda: st.session_state.update(page="home"))


# Main function to display and edit cases by date
def cases_by_date(config):
    st.header("Cases by Date")

    selected_date = st.date_input("Select Date")

    if st.button("Get Cases"):
        cases = get_cases_by_date(selected_date, config)

        if not cases:
            st.write(f"No cases found for {selected_date}.")
        else:
            st.write(f"Cases for {selected_date}:")

            # Convert cases to DataFrame
            df_cases = pd.DataFrame(cases, columns=config['headers'])

            # Store the initial DataFrame in session state
            st.session_state.df_value = df_cases

    if "df_value" in st.session_state:
        df_cases = st.session_state.df_value

        # Create a column_config dictionary to disable all columns except "Upcoming Date" and "Stage"
        column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if col not in ["Upcoming Date", "Stage"]}

        # Display editable DataFrame with column configuration and fixed number of rows
        edited_df = st.data_editor(
            df_cases,
            num_rows="fixed",
            column_config=column_config,
        )

        # Check if the data_editor was edited
        if st.button("Update Cases"):
            if edited_df is not None:
                update_case_data(edited_df, config)
                st.session_state.df_value = edited_df
            else:
                st.write("No changes detected.")

    st.button("Go to Main Page", on_click=lambda: st.session_state.update(page="home"))

def pending_cases(config):
    st.header("Pending Cases")

    cases = get_pending_cases(config)

    if not cases:
        st.write("No pending cases found.")
    else:
        st.write("Pending Cases:")
        df_cases = pd.DataFrame(cases, columns=config['headers'])
        st.session_state.df_value = df_cases

    if "df_value" in st.session_state:
        df_cases = st.session_state.df_value

        # Create a column_config dictionary to disable all columns except "Upcoming Date" and "Stage"
        column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if col not in ["Upcoming Date", "Stage"]}

        # Display editable DataFrame with column configuration
        edited_df = st.data_editor(
            df_cases,
            num_rows="fixed",
            column_config=column_config,
        )

        # Check if the data_editor was edited
        if st.button("Update Cases"):
            if edited_df is not None:
                update_case_data(edited_df, config)
                st.session_state.df_value = edited_df
            else:
                st.write("No changes detected.")

    st.button("Go to Main Page", on_click=lambda: st.session_state.update(page="home"))


if __name__ == "__main__":
    main()
