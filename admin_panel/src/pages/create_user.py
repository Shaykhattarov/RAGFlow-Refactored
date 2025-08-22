import streamlit as st

from utils.users import register_user
from pages._base import BasePage



class CreateUserPage(BasePage):

    def __init__(self):
        super().__init__()

        self.view_title()
        self.view_create_form()

    def view_title(self):
        self.placeholder = st.container()
        self.placeholder.title("Создать нового пользователя")

    def view_create_form(self):
        self.form = self.placeholder.form(key="create_user", clear_on_submit=True)
        email = self.form.text_input(label="Введите email", placeholder="Email")
        nickname = self.form.text_input(label="Введите имя", placeholder="Имя")
        password = self.form.text_input(label="Введите пароль", type="password", placeholder="Password")
        submit = self.form.form_submit_button(label="Создать")

        if submit:
            print(email, nickname, password)
            if register_user(email, nickname, password): # Регистрация пользователя
                self.placeholder.success("Пользователь добавлен!")
            else:
                self.placeholder.error("Произошла ошибка при добавлении пользователя!")


create_user_page = CreateUserPage()