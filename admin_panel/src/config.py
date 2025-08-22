import os

from pydantic_settings import BaseSettings
from pydantic import Field



class Settings(BaseSettings):

    basedir: str = os.path.dirname(os.path.abspath(__file__))

    mysql_database_name: str = Field(
        default="rag_flow",
        description="RAGFlow Database Name"
    )

    mysql_user: str = Field(
        default="root",
        description="RAGFlow Database Name"
    )

    mysql_root_password: str = Field(
        default="password",
        description="RAGFlow Database Password"
    )

    mysql_host: str = Field(
        default="mysql",
        description="RAGFlow Database Host"
    )

    mysql_port: int = Field(
        default=3306,
        description="RAGFlow Database Port "
    )

    # chat_model: str = Field(
    #     default="",
    #     descritpion="JSON String with Chat model settings"
    # )

    # embedding_model: str = Field(
    #     default="",
    #     descritpion="JSON String with Embedding model settings"
    # )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensetive = False


settings = Settings()