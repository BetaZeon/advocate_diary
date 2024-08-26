import streamlit as st
from views.case_view import CaseView


def main():
    st.set_page_config(layout="wide")
    st.title("Case Management System")

    case_view = CaseView()

    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Define a sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        if st.button("Home", key="home"):
            st.session_state.page = "home"
        if st.button("Add New Case", key="add_case"):
            st.session_state.page = "add_case"
        if st.button("Search Case", key="search_case"):
            st.session_state.page = "search_case"
        if st.button("Today's Case List", key="todays_case_list"):
            st.session_state.page = "todays_case_list"
        if st.button("Cases by Date", key="cases_by_date"):
            st.session_state.page = "cases_by_date"
        if st.button("Pending Cases", key="pending_cases"):
            st.session_state.page = "pending_cases"
        if st.button("Cases By Company Name", key="cases_by_company_name"):
            st.session_state.page = "cases_by_company_name"

    # Main content area
    if st.session_state.page == "home":
        st.subheader("Welcome to the Case Management System")
        st.write("Select an option from the sidebar to get started.")

    if st.session_state.page == "add_case":
        case_view.add_case()

    if st.session_state.page == "search_case":
        case_view.search_case()

    if st.session_state.page == "todays_case_list":
        case_view.todays_case_list()

    if st.session_state.page == "cases_by_date":
        case_view.cases_by_date()

    if st.session_state.page == "pending_cases":
        case_view.pending_cases()

    if st.session_state.page == "cases_by_company_name":
        case_view.search_cases_by_company_name()

