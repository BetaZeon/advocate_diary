import streamlit as st
from controllers.auth_controller import AuthController

class AuthView:
    @staticmethod
    def login():
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = AuthController.login_user(username, password)
            if success:
                st.session_state.user = username
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    @staticmethod
    def register():
        st.header("Register")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
             if password != confirm_password:
                st.error("Passwords do not match")
             else:
                success, message = AuthController.register_user(username, email, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)