import streamlit as st
from views.case_view import CaseView

def main():
    st.set_page_config(layout="wide")
    st.title("Case Management System")

    case_view = CaseView()

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.button("Add New Case", on_click=lambda: st.session_state.update(page="add_case"))
        st.button("Search Case", on_click=lambda: st.session_state.update(page="search_case"))
        st.button("Today's Case List", on_click=lambda: st.session_state.update(page="todays_case_list"))
        st.button("Cases by Date", on_click=lambda: st.session_state.update(page="cases_by_date"))
        st.button("Pending Cases", on_click=lambda: st.session_state.update(page="pending_cases"))

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
