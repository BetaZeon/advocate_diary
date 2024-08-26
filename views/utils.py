import streamlit as st

def go_to_main_page_button():
    st.button("Go to Main Page", on_click=lambda: st.session_state.update(page="home"))
