import streamlit as st
from controllers.case_controller import CaseController
import pandas as pd
class CaseView:
    def __init__(self):
        self.controller = CaseController()

    def add_case(self):
        st.header("Add New Case")
        # Implement the form for adding a new case
        # Call self.controller.add_new_case(case_data) to add the case

    def search_case(self):
        st.header("Search Case")
        search_criteria = st.selectbox("Search Case By", ["Case Number", "Case Title"])
        search_query = st.text_input(f"Enter {search_criteria}", "")

        if st.button("Search"):
            cases = self.controller.search_case(search_criteria, search_query)
            if not cases:
                st.write("No cases found.")
            else:
                df_cases = pd.DataFrame(cases)
                st.dataframe(df_cases)

    def todays_case_list(self):
        st.header("Today's Case List")
        cases = self.controller.get_todays_cases()
        if not cases:
            st.write("No cases scheduled for today.")
        else:
            df_cases = pd.DataFrame(cases)
            st.dataframe(df_cases)

    def cases_by_date(self):
        st.header("Cases by Date")
        selected_date = st.date_input("Select Date")
        if st.button("Get Cases"):
            cases = self.controller.get_cases_by_date(selected_date)
            if not cases:
                st.write(f"No cases found for {selected_date}.")
            else:
                df_cases = pd.DataFrame(cases)
                st.dataframe(df_cases)

    def pending_cases(self):
        st.header("Pending Cases")
        cases = self.controller.get_pending_cases()
        if not cases:
            st.write("No pending cases found.")
        else:
            df_cases = pd.DataFrame(cases)
            st.dataframe(df_cases)
