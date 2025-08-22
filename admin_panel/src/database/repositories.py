from typing import List
from sqlalchemy import select

from database.connection import session_factory
from database.models import (
    User, 
    Tenant, 
    TenantLLM,
    UserTenant,
    File,    
)



def get_all_users() -> List[User]:
    session = session_factory()
    statement = select(User)
    users = []
    try:
        response = session.execute(statement)
    except Exception as err:
        print(err)
    else:
        users = response.scalars().fetchall()
    return users

def get_all_models() -> List[TenantLLM]:
    session = session_factory()
    statement = select(TenantLLM)
    users = []
    try:
        response = session.execute(statement)
    except Exception as err:
        print(err)
    else:
        users = response.scalars().fetchall()
    return users

def get_all_default_models() -> List[Tenant]:
    session = session_factory()
    statement = select(Tenant)
    users = []
    try:
        response = session.execute(statement)
    except Exception as err:
        print(err)
    else:
        users = response.scalars().fetchall()
    return users

def check_user_exists(email: str) -> bool:
    session = session_factory()
    statement = select(User).where(User.email == email)

    try:
        response = session.execute(statement)
    except Exception as err:
        print(err)  
        return False
    else:
        if response.first() is None:
            return False
        else:
            return True

def create_user(user_dict: dict) -> bool:
    session = session_factory()
    user = User(
        id=user_dict["id"],
        access_token=user_dict["access_token"],
        email=user_dict["email"],
        nickname=user_dict["nickname"],
        password=user_dict["password"],
        login_channel=user_dict["login_channel"],
        last_login_time=user_dict["last_login_time"],
        is_superuser=user_dict["is_superuser"],
        is_authenticated=user_dict["is_authenticated"],
        is_active=user_dict["is_active"],
        is_anonymous=user_dict["is_anonymous"],
        status=user_dict["status"],
        create_time=user_dict["create_time"],
        create_date=user_dict["create_date"],
        update_time=user_dict["update_time"],
        update_date=user_dict["update_date"],
    )

    try:
        session.add(user)
        session.commit()
    except Exception as err:
        print(err)
        session.rollback()
        return False
    
    return True

def check_tenant_llm_exists(tenant_dict: dict):
    session = session_factory()
    statement = select(TenantLLM).where(TenantLLM.llm_name == tenant_dict["llm_name"])
    try:
        response = session.execute(statement)
    except Exception as err:
        print(err)
        return False
    else:
        if response.first() is None:
            return False
        else:
            return True

def create_tenant_llm(tenant_dict: dict) -> bool:
    session = session_factory()
    tenant_llm = TenantLLM(
        create_time=tenant_dict["create_time"],
        create_date=tenant_dict["create_date"],
        update_time=tenant_dict["update_time"],
        update_date=tenant_dict["update_date"],
        tenant_id=tenant_dict["tenant_id"],
        llm_factory=tenant_dict["llm_factory"],
        model_type=tenant_dict["model_type"],
        llm_name=tenant_dict["llm_name"],
        api_key=tenant_dict["api_key"],
        api_base=tenant_dict["api_base"],
        max_tokens=tenant_dict["max_tokens"],
        used_tokens=tenant_dict["used_tokens"]
    )

    try:
        session.add(tenant_llm)
        session.commit()
    except Exception as err:
        print(err)
        session.rollback()
        return False

    return True

def create_tenant(tenant_dict: dict) -> bool:
    session = session_factory()
    tenant = Tenant(
        id=tenant_dict["id"],
        create_time=tenant_dict["create_time"],
        create_date=tenant_dict["create_date"],
        update_time=tenant_dict["update_time"],
        update_date=tenant_dict["update_date"],
        name=tenant_dict["name"],
        llm_id=tenant_dict["llm_id"],
        embd_id=tenant_dict["embd_id"],
        asr_id=tenant_dict["asr_id"],
        img2txt_id=tenant_dict["img2txt_id"],
        rerank_id=tenant_dict["rerank_id"],
        parser_ids=tenant_dict["parser_ids"],
        credit=tenant_dict["credit"],
        status=tenant_dict["status"]
    )

    try:
        session.add(tenant)
        session.commit()
    except Exception as err:
        print(err)
        session.rollback()
        return False

    return True

def create_user_tenant(user_tenant_dict: dict):
    session = session_factory()
    user_tenant = UserTenant(
        create_time=user_tenant_dict["create_time"],
        create_date=user_tenant_dict["create_date"],
        update_time=user_tenant_dict["update_time"],
        update_date=user_tenant_dict["update_date"],
        id=user_tenant_dict["id"],
        tenant_id=user_tenant_dict["tenant_id"],
        user_id=user_tenant_dict["user_id"],
        invited_by=user_tenant_dict["invited_by"],
        role=user_tenant_dict["role"],
        status=user_tenant_dict["status"]
    )

    try:
        session.add(user_tenant)
        session.commit()
    except Exception as err:
        print(err)
        session.rollback()
        return False

    return True

def create_file(file_dict: dict):
    session = session_factory()
    file = File(
        id=file_dict["id"],
        create_time=file_dict["create_time"],
        create_date=file_dict["create_date"],
        update_time=file_dict["update_time"],
        update_date=file_dict["update_date"],
        parent_id=file_dict["parent_id"],
        tenant_id=file_dict["tenant_id"],
        created_by=file_dict["created_by"],
        name=file_dict["name"],
        type=file_dict["type"],
        size=file_dict["size"],
        location=file_dict["location"],
        source_type=""
    )

    try:
        session.add(file)
        session.commit()
    except Exception as err:
        print(err)
        session.rollback()
        return False

    return True