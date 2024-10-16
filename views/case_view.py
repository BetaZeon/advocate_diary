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
                update_status = self.controller.update_case(case_id, case_data)
                st.write(update_status)

    def search_case(self):
        st.header("Search Case")
        search_criteria = st.selectbox("Search Case By", ["Case Number", "Case Title"])
        search_query = st.text_input(f"Enter {search_criteria}", "")

        if st.button("Search"):
            with st.spinner("Searching for cases..."):
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
        with st.spinner("Fetching cases..."):
            cases = self.controller.search_case_by_company(company_name)
        if not cases:
            st.write("No cases found.")
        else:
            df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
            st.dataframe(df_cases)

    def todays_case_list(self):
        st.header("Today's Case List")

        # Initialize session state for messages
        if 'show_message' not in st.session_state:
            st.session_state.show_message = False
        if 'message' not in st.session_state:
            st.session_state.message = ""

        # Display message if it exists in session state
        if st.session_state.show_message:
            st.info(st.session_state.message)
            # Clear the message flag
            st.session_state.show_message = False

        with st.form("todays_case_list"):
            submit_button = st.form_submit_button("Get Cases")

            if submit_button:
                with st.spinner("Fetching today's cases..."):
                    cases = self.controller.get_todays_cases()
                if not cases:
                    st.write("No cases scheduled for today.")
                    if 'df_value' in st.session_state:
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
                key="today_cases_editor"
            )

            if st.button("Update Cases"):
                with st.spinner("Updating cases..."):
                    updates_made = update_cases_and_previous_dates(self, edited_df, date.today())
                
                if updates_made:
                    st.session_state.message = "Cases updated successfully!"
                    # Refresh the data after update
                    updated_cases = self.controller.get_todays_cases()
                    if updated_cases:
                        st.session_state.df_value = pd.DataFrame(updated_cases, columns=config_loader.load_config()['headers'])
                else:
                    st.session_state.message = "No changes were made."
                
                st.session_state.show_message = True
                st.rerun()

    def cases_by_date(self):
        st.header("Cases by Date")
        
        # Initialize session state variables if they don't exist
        if 'cases_df' not in st.session_state:
            st.session_state.cases_df = None
        if 'selected_date' not in st.session_state:
            st.session_state.selected_date = pd.Timestamp.now().date()
        if 'show_cases' not in st.session_state:
            st.session_state.show_cases = False
        
        # Create a placeholder for the message
        message_placeholder = st.empty()
        
        # Function to handle case updates
        def update_cases():
            with st.spinner("Updating cases..."):
                updates_made = update_cases_and_previous_dates(self, st.session_state.edited_df, st.session_state.cases_df)
            if updates_made:
                st.session_state.update_message = "Cases updated successfully."
                # Refresh the data after update
                st.session_state.cases_df = pd.DataFrame(
                    self.controller.get_cases_by_date(st.session_state.selected_date),
                    columns=config_loader.load_config()['headers']
                )
            else:
                st.session_state.update_message = "No changes were made."
            st.session_state.show_message = True
        
        # Display message if it exists in session state
        if st.session_state.get('show_message', False):
            message_placeholder.info(st.session_state.update_message)
            # Clear the message flag
            st.session_state.show_message = False
        
        # Date input and Get Cases button
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_date = st.date_input("Select Date", value=st.session_state.selected_date)
        with col2:
            get_cases = st.button("Get Cases")

        if get_cases:
            st.session_state.selected_date = selected_date
            st.session_state.show_cases = True
            cases = self.controller.get_cases_by_date(selected_date)
            if not cases:
                st.write(f"No cases found for {selected_date}.")
                st.session_state.cases_df = None
            else:
                st.session_state.cases_df = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])

        if st.session_state.show_cases and st.session_state.cases_df is not None:
            column_config = {col: st.column_config.Column(disabled=True) for col in st.session_state.cases_df.columns if
                            col not in ["Upcoming Date", "Stage"]}

            st.session_state.edited_df = st.data_editor(
                st.session_state.cases_df,
                num_rows="fixed",
                column_config=column_config,
                key="cases_editor"
            )
            
            # Update Cases button
            st.button("Update Cases", on_click=update_cases)
    # def pending_cases(self):
    #     st.header("Pending Cases")
    #     cases = self.controller.get_pending_cases()
    #     if not cases:
    #         st.write("No pending cases found.")
    #     else:
    #         df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
    #         st.dataframe(df_cases)

    # def pending_cases(self):
    #     st.header("Pending Cases")
    #     with st.spinner("Fetching pending cases..."):
    #         cases = self.controller.get_pending_cases()
    #     if not cases:
    #         st.write("No pending cases found.")
    #     else:
    #         df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
    #         st.session_state.df_value = df_cases

    #         column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if
    #                         col not in ["Upcoming Date", "Stage"]}

    #         edited_df = st.data_editor(
    #             df_cases,
    #             num_rows="fixed",
    #             column_config=column_config,
    #         )
    #         if st.button("Update Cases"):
    #             with st.spinner("Updating cases..."):
    #                 update_cases_and_previous_dates(self, edited_df, date.today())
    #             st.rerun()

    def pending_cases(self):
        st.header("Pending Cases")
        
        # Create a placeholder for the message
        message_placeholder = st.empty()
        
        # Function to handle case updates
        def update_cases():
            with st.spinner("Updating cases..."):
                updates_made = update_cases_and_previous_dates(self, edited_df, df_cases)
            if updates_made:
                st.session_state.update_message = "Cases updated successfully."
            else:
                st.session_state.update_message = "No changes were made."
            st.session_state.show_message = True
        
        # Display message if it exists in session state
        if st.session_state.get('show_message', False):
            message_placeholder.info(st.session_state.update_message)
            # Clear the message flag
            st.session_state.show_message = False
        
        # Fetch pending cases
        with st.spinner("Fetching pending cases..."):
            cases = self.controller.get_pending_cases()
        
        if not cases:
            st.write("No pending cases found.")
        else:
            df_cases = pd.DataFrame(cases, columns=config_loader.load_config()['headers'])
            
            column_config = {col: st.column_config.Column(disabled=True) for col in df_cases.columns if
                            col not in ["Upcoming Date", "Stage"]}

            edited_df = st.data_editor(
                df_cases,
                num_rows="fixed",
                column_config=column_config,
                key="pending_cases_editor"
            )
            
            # Use on_click parameter for the button
            st.button("Update Cases", on_click=update_cases)
    
    def update_config(self):
        st.header("Update Config")
        config = config_loader.load_config()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Case Types")
            case_types = st.multiselect("Select Case Types", config['case_types'], default=config['case_types'])
            new_case_type = st.text_input("Add New Case Type", "")
            if st.button("Add Case Type"):
                if new_case_type:
                    config['case_types'].append(new_case_type)
                    config_loader.save_config(config)
                    st.success("Case Type added successfully!")

        with col2:
            st.subheader("Statuses")
            statuses = st.multiselect("Select Statuses", config['statuses'], default=config['statuses'])
            new_status = st.text_input("Add New Status", "")
            if st.button("Add Status"):
                if new_status:
                    config['statuses'].append(new_status)
                    config_loader.save_config(config)
                    st.success("Status added successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Company Names")
            company_names = st.multiselect("Select Company Names", config['company_names'], default=config['company_names'])
            new_company_name = st.text_input("Add New Company Name", "")
            if st.button("Add Company Name"):
                if new_company_name:
                    config['company_names'].append(new_company_name)
                    config_loader.save_config(config)
                    st.success("Company Name added successfully!")

        with col2:
            st.subheader("Locations")
            locations = st.multiselect("Select Locations", config['locations'], default=config['locations'])
            new_location = st.text_input("Add New Location", "")
            if st.button("Add Location"):
                if new_location:
                    config['locations'].append(new_location)
                    config_loader.save_config(config)
                    st.success("Location added successfully!")