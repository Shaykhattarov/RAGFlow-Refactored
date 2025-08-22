from database.connection import Base, metadata, engine
from sqlalchemy.schema import Table



class User(Base):
    """ Таблица пользователей"""
    __table__ = Table('user', metadata, autoload_with=engine)

class UserTenant(Base):
    """ Таблица связи пользователей и tenant """
    __table__ = Table('user_tenant', metadata, autoload_with=engine)

class Tenant(Base):
    """ Таблица с дефолтными моделями (tenant.id == user.id)"""
    __table__ = Table('tenant', metadata, autoload_with=engine)

class TenantLLM(Base):
    """ таблица с настройками моделей и с моделями"""
    __table__ = Table('tenant_llm', metadata, autoload_with=engine)

class File(Base):
    """ Таблица с файлами """
    __table__ = Table('file', metadata, autoload_with=engine)
