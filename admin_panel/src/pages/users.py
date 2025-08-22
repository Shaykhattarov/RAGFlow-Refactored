from typing import List
import streamlit as st
import pandas as pd

from pages._base import BasePage
from database.models import User
from database.repositories import get_all_users


class UsersPage(BasePage):

    columns: list = [
        "id",
        "nickname",
        "email",
        "password",
        "access_token",
        "is_active",
        "update_date",
    ]

    def __init__(self):
        super().__init__()
        self.view_title()
        self.view_action_menu()
        self.view_table()

    def view_title(self):
        self.placeholder = st.container()
        self.placeholder.title("Пользователи")
        
    def view_action_menu(self):
        menu = ("Выберите действие", "Добавить пользователя")
        selected_item = self.placeholder.selectbox("Действия", menu)

        if selected_item == menu[1]:
            st.switch_page("pages/create_user.py")

    def view_table(self):
        users: List[User] = get_all_users()
        users: List[dict] = [user.__dict__ for user in users]
        users_dataframe = pd.DataFrame(users, columns=self.columns)

        self.placeholder.dataframe(
            users_dataframe,
            use_container_width=True
        )


users_page = UsersPage()
