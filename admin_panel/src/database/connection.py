from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings


DATABASE_URL = f"mysql+mysqlconnector://{settings.mysql_user}:{settings.mysql_root_password}" + \
               f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database_name}"

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

session_factory = sessionmaker(
    autoflush=False, 
    autocommit=False, 
    expire_on_commit=False,
    bind=engine
)

session = session_factory()
        