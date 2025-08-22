import streamlit as st



st.set_page_config(
    page_title="Админ-панель", 
    page_icon="⚙️", 
    initial_sidebar_state="expanded"
)
st.sidebar.title("⚙️ Админ-панель управления пользователями")
st.sidebar.page_link("main.py", label="Main")
st.sidebar.page_link("pages/users.py", label="Users")
st.sidebar.page_link("pages/models.py", label="Models")
