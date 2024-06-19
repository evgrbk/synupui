import streamlit as st


def menu():
    st.sidebar.page_link("main.py", label="Главная", icon='🏠')
    st.sidebar.page_link("pages/prompts.py", label="Промты", icon="📚")
    st.sidebar.page_link("pages/billing.py", label="Биллинг", icon="💵")
    # st.sidebar.page_link("pages/dataframes.py", label="Тест", icon="💵")
