from typing import List
import streamlit as st
import pandas as pd

from pages._base import BasePage
from database.models import TenantLLM
from database.repositories import get_all_models


class ModelsPage(BasePage):

    columns: list = [ 
        "tenant_id",
        "llm_factory",
        "model_type",
        "llm_name",
        "api_key",
        "api_base",
        "max_tokens",
        "used_tokens",
        "create_date",
    ]

    def __init__(self):
        super().__init__()
        self.view_table()

    def view_table(self):
        models: List[TenantLLM] = get_all_models()
        models: List[dict] = [model.__dict__ for model in models]
        models_dataframe = pd.DataFrame(models, columns=self.columns)

        placeholder = st.container()
        placeholder.title("Модели созданные пользователями")
        placeholder.dataframe(
            models_dataframe,
            use_container_width=True
        )


models_page = ModelsPage()
