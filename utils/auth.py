import streamlit as st
import hmac

def login(username, password):
    if username in st.secrets["passwords"]:
        if hmac.compare_digest(st.secrets["passwords"][username], password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = st.secrets["roles"][username]
            return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None