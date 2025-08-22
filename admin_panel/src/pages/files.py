import streamlit as st
import pandas as pd

from typing import List
from pages._base import BasePage
from database.models import File
from database.repositories import get_all_files


class FilePage(BasePage):

    columns: list[str] = [
        "parent_id",
        "tenant_id",
        "created_by",
        "name",
        "location",
        "size",
        "type",
        "source_type"
    ]

    def __init__(self):
        super().__init__()
        self.view_table()
    
    def view_table(self):
        files: List[File] = get_all_files()
        files: List[dict] = [file.__dict__ for file in files]
        files_dataframe = pd.DataFrame(files, columns=self.columns)

        placeholder = st.container()
        placeholder.title("Файлы и каталоги созданные пользователями")
        placeholder.dataframe(
            files_dataframe,
            use_container_width=True
        )

files_page = FilePage()