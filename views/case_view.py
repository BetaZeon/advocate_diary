import streamlit as st
from datetime import date
from controllers.case_controller import CaseController
from models.case import Case
import pandas as pd
import config_loader
from views.utils import update_cases_and_previous_dates


class CaseView:

    def __init__(self):
        self.controller = CaseController()

    def add_case(self):
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
            case_type = st.selectbox("Case Type", config_loader.load_config()['case_types'], key="case_type")
            location = st.selectbox("Location", config_loader.load_config()['locations'], key="location")
            company_name = st.selectbox("Company Name", config_loader.load_config()['company_names'], key="company_name")
            upcoming_date = st.date_input("Upcoming Date", key="upcoming_date")
            stage = st.text_input("Stage", max_chars=50, key="stage")
            status = st.selectbox("Status", config_loader.load_config()['statuses'], key="status")
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
                # Show spinner while case is being added
                with st.spinner("Adding new case..."):
                    if self.controller.add_new_case(case_number, location):
                        st.error("Case number already exists for the selected location")
                    else:
                        case_data = {
                            "case_number": case_number,
                            "case_title": case_title,
                            "case_type": case_type,
                            "location": location,
                            "company_name": company_name,
                            "upcoming_date": upcoming_date,
                            "stage": stage,
                            "remarks": remarks,
                            "status": status,
                            "claimant_advocate_name": claimant_advocate_name,
                            "claimant_advocate_mobile_number": claimant_advocate_mobile_number
                        }
                        try:
                            Case.add_case(case_data)
                            st.success("Case added successfully!")
                        except Exception as e:
                            st.error(f"Error adding case: {e}")

    def update_case(self):
        st.header("Update Case")
        search_query = st.text_input("Enter Case Number or Case Title")
        
        if st.button("Search"):
            case = self.controller.get_case_by_number_or_title(search_query)
            if case:
                st.session_state.case_to_update = case
                st.success("Case found. Please update the fields below.")
            else:
                st.error("Case not found.")

        if 'case_to_update' in st.session_state:
            case = st.session_state.case_to_update
            case_id = case[0]  # Assuming the ID is the first column

            col1, col2 = st.columns(2)

            with col1:
                case_number = st.text_input("Case Number", value=case[1], max_chars=10)
                case_title = st.text_input("Case Title", value=case[2], max_chars=255)
                case_type = st.selectbox("Case Type", config_loader.load_config()['case_types'], index=config_loader.load_config()['case_types'].index(case[3]) if case[3] in config_loader.load_config()['case_types'] else 0)
                location = st.selectbox("Location", config_loader.load_config()['locations'], index=config_loader.load_config()['locations'].index(case[4]) if case[4] in config_loader.load_config()['locations'] else 0)
                company_name = st.selectbox("Company Name", config_loader.load_config()['company_names'], index=config_loader.load_config()['company_names'].index(case[5]) if case[5] in config_loader.load_config()['company_names'] else 0)
                upcoming_date = st.date_input("Upcoming Date", value=case[6] if case[6] else None)
                stage = st.text_input("Stage", value=case[8], max_chars=50)                
                # Handle the case where status might be empty or not in the list
                statuses = config_loader.load_config()['statuses']
                status_index = statuses.index(case[10]) if case[10] in statuses else 0
                status = st.selectbox("Status", statuses, index=status_index)
                
                claimant_advocate_name = st.text_input("Claimant Advocate Name", value=case[11], max_chars=100)
                claimant_advocate_mobile_number = st.text_input("Claimant Advocate Mobile Number", value=case[12], max_chars=15)
                remarks = st.text_area("Remarks", value=case[9])
            if st.button("Update"):
                with st.spinner("Updating the case..."):
                    case_data = {
                        "case_number": case_number,
                        "case_title": case_title,
                        "case_type": case_type,
                        "location": location,
                        "company_name": company_name,
                        "upcoming_date": upcoming_date,
                        "stage": stage,
                        "remarks": remarks,
                        "status": status,
                        "claimant_advocate_name": claimant_advocate_name,
                        "claimant_advocate_mobile_number": claimant_advocate_mobile_number
                    }
                    try:
                        self.controller.update_case(case_id, case_data)
                        st.success("Case updated successfully!")
                    except Exception as e:
                        st.error(f"Error updating case: {e}")

    def search_case(self):
        st.header("Search Case")
        search_criteria = st.selectbox("Search Case By", ["Case Number", "Case Title"])
        search_query = st.text_input(f"Enter {search_criteria}", "")

        if st.button("Search"):
            cases = self.controller.search_case(search_criteria, search_query)
            if not cases:
                st.write("No cases found.")
            else:
                df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
                st.dataframe(df_cases)

    def search_cases_by_company_name(self):
        st.header("Search Cases By Company Name")
        company_name = st.selectbox("Company Name",
                                    config_loader.load_config()['company_names'], key="company_name")
        cases = self.controller.search_case_by_company(company_name)
        if not cases:
           st.write("No cases found.")
        else:
           df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
           st.dataframe(df_cases)

    def todays_case_list(self):
        st.header("Today's Case List")
        with st.form("todays_case_list"):
            submit_button = st.form_submit_button("Get Cases")

            # Fetch data if the button is clicked or if it's the current date
            if submit_button:
                cases = self.controller.get_todays_cases()
                if not cases:
                    st.write("No cases scheduled for today.")
                else:
                    df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
                    st.session_state.df_value = df_cases
        if "df_value" in st.session_state:
            df_cases = st.session_state.df_value

            column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if
                             col not in ["Upcoming Date", "Stage"]}

            edited_df = st.data_editor(
                df_cases,
                num_rows="fixed",
                column_config=column_config,
            )
            if st.button("Update Cases"):
                update_cases_and_previous_dates(self, edited_df, date.today())

    def cases_by_date(self):
        st.header("Cases by Date")
        with st.form("cases_by_date_form"):
            selected_date = st.date_input("Select Date", value=pd.Timestamp.now().date())
            submit_button = st.form_submit_button("Get Cases")

            # Fetch data if the button is clicked or if it's the current date
            if submit_button or selected_date == pd.Timestamp.now().date():
                cases = self.controller.get_cases_by_date(selected_date)
                if not cases:
                    st.write(f"No cases found for {selected_date}.")
                    if "df_value" in st.session_state:
                        del st.session_state.df_value
                else:
                    df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
                    st.session_state.df_value = df_cases

        if "df_value" in st.session_state:
            df_cases = st.session_state.df_value

            column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if
                             col not in ["Upcoming Date", "Stage"]}

            edited_df = st.data_editor(
                df_cases,
                num_rows="fixed",
                column_config=column_config,
            )
            if st.button("Update Cases"):
                update_cases_and_previous_dates(self, edited_df, selected_date)

    def pending_cases(self):
        st.header("Pending Cases")
        cases = self.controller.get_pending_cases()
        if not cases:
            st.write("No pending cases found.")
        else:
            df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
            st.dataframe(df_cases)