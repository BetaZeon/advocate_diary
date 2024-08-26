import psycopg2
import streamlit as st

def get_connection():
    config = {
        "host": st.secrets["database"]["host"],
        "port": st.secrets["database"]["port"],
        "database": st.secrets["database"]["database"],
        "user": st.secrets["database"]["user"],
        "password": st.secrets["database"]["password"]
    }
    return psycopg2.connect(**config)
