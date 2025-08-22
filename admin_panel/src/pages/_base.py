import streamlit as st



class BasePage:

    def __init__(self):
        self.view_sidebar()

    def view_sidebar(self):
        st.sidebar.title("⚙️ Админ-панель управления пользователями")
        st.sidebar.page_link("main.py", label="Main")
        st.sidebar.page_link("pages/users.py", label="Users")
        st.sidebar.page_link("pages/models.py", label="Models")
