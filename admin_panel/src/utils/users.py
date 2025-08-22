import os
import uuid
import time
import base64
import datetime

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from werkzeug.security import generate_password_hash

from config import settings
from database.repositories import (
    create_user,
    create_file,
    create_tenant,
    create_tenant_llm,
    create_user_tenant,
    check_user_exists,
    check_tenant_llm_exists,
)


def register_user(email: str, nickname: str, password) -> bool:
    """Регистрация пользователя в системе
    1. Создает запись в таблице User;
    2. Создает две записи в таблице TenantLLM (если llm не созданы);
    3. Создает запись в таблице Tenant (установка дефолтных моделей);
    4. Создает запись в таблице UserTenant (для создания связи);
    5. Создает запись в таблице File (информация о загруженных файлах пользователя);
    """
    # Если пользователь существует то выходим из функции
    if check_user_exists(email):
        return False

    user_id = generate_uuid()
    user_dict = {
        "id": user_id,
        "access_token": generate_uuid(),
        "email": email,
        "nickname": nickname,
        "password": generate_hash_password(password),
        "login_channel": "password",
        "language": "English",
        "color_schema": "Bright",
        "timezone": "UTC+4  Europe/Samara",
        "last_login_time": get_format_time(),
        "is_superuser": False,
        "is_authenticated": True,
        "is_active": True,
        "is_anonymous": False,
        "status": True,
        "create_time": current_timestamp(),
        "create_date": get_format_time(),
        "update_time": current_timestamp(),
        "update_date": get_format_time(),
    }

    tenant_dict = {
        "id": user_id,
        "name": nickname + "‘s Kingdom",
        "llm_id": "Qwen/Qwen2.5-72B-Instruct-GPTQ-Int8___VLLM@VLLM",
        "embd_id": "BAAI/bge-m3___VLLM@VLLM",
        "asr_id": "",
        "parser_ids": "naive:General,qa:Q&A,resume:Resume,manual:Manual,table:Table,paper:Paper,book:Book,laws:Laws,presentation:Presentation,picture:Picture,one:One,audio:Audio,email:Email,tag:Tag",
        "img2txt_id": "",
        "rerank_id": "",
        "credit": 512,
        "status": True,
        "create_time": current_timestamp(),
        "create_date": get_format_time(),
        "update_time": current_timestamp(),
        "update_date": get_format_time(),
    }

    user_tenant_dict = {
        "id": generate_uuid(),
        "tenant_id": user_id,
        "user_id": user_id,
        "invited_by": user_id,
        "role": "owner",
        "status": True,
        "create_time": current_timestamp(),
        "create_date": get_format_time(),
        "update_time": current_timestamp(),
        "update_date": get_format_time(),
    }

    file_id = generate_uuid()
    file_dict = {
        "id": user_id,
        "parent_id": user_id,
        "tenant_id": user_id,
        "created_by": user_id,
        "name": "/",
        "type": "folder",
        "size": 0,
        "location": "",
        "create_time": current_timestamp(),
        "create_date": get_format_time(),
        "update_time": current_timestamp(),
        "update_date": get_format_time(),
    }

    default_chat_model = {
        "tenant_id": user_id,
        "model_type": "chat",
        "llm_factory": "VLLM",
        "llm_name": "Qwen/Qwen2.5-72B-Instruct-GPTQ-Int8___VLLM",
        "api_key": "Neurocoder_Large_Qwen_2025",
        "api_base": "http://176.99.135.7:8000/v1",
        "max_tokens": 16344,
        "used_tokens": 0,
        "create_time": current_timestamp(),
        "create_date": get_format_time(),
        "update_time": current_timestamp(),
        "update_date": get_format_time(),
    }
    default_embedding_model = {
        "tenant_id": user_id,
        "model_type": "embedding",
        "llm_factory": "VLLM",
        "llm_name": "BAAI/bge-m3___VLLM",
        "api_key": "PlanetEmbedderModel2025",
        "api_base": "http://81.94.156.134:8088/v1",
        "max_tokens": 8192,
        "used_tokens": 0,
        "create_time": current_timestamp(),
        "create_date": get_format_time(),
        "update_time": current_timestamp(),
        "update_date": get_format_time(),
    }

    # Создание пользователя в БД
    if not create_user(user_dict):
        return False

    # Создание моделей
    if not check_tenant_llm_exists(default_chat_model):  # Если не существует, то
        if not create_tenant_llm(
            default_chat_model
        ):  # Создаем модель, если не получилось то
            return False  # Возвращаем ошибку

    if not check_tenant_llm_exists(default_embedding_model):  # Если не существует, то
        if not create_tenant_llm(
            default_embedding_model
        ):  # Создаем модель, если не получилось то
            return False  # Возвращаем ошибку

    # Создание Tenant
    if not create_tenant(tenant_dict):
        return False
    
    # Создание UserTenant
    if not create_user_tenant(user_tenant_dict):
        return False

    # Создание корневого File
    if not create_file(file_dict):
        return False
    
    return True


def datetime_format(date_time: datetime.datetime) -> datetime.datetime:
    """Функция возвращает дату в установленном формате"""
    return datetime.datetime(
        date_time.year,
        date_time.month,
        date_time.day,
        date_time.hour,
        date_time.minute,
        date_time.second,
    )


def current_timestamp():
    """Функция возвращает временную метку"""
    return int(time.time() * 1000)


def get_format_time() -> datetime.datetime:
    """Функция возвращает дату в установленном формате"""
    return datetime_format(datetime.datetime.now())


def generate_uuid():
    """Функция возвращает сгенерированный уникальный UUID"""
    return uuid.uuid1().hex


def encrypt_password(password: str):
    """Шифрует строку с помощью публичного RSA ключа"""
    public_key = os.path.join(settings.basedir, "keys", "public.pem")
    rsa_key = RSA.import_key(open(public_key).read())
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    return cipher.encrypt(base64.b64encode(password.encode("utf-8")))


def decrypt_password(encrypt_password: bytes):
    """Дешифрует строку с помощью приватного ключа RSA"""
    private_key = os.path.join(settings.basedir, "keys", "private.pem")
    rsa_key = RSA.import_key(open(private_key).read(), "Welcome")
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    return cipher.decrypt(encrypt_password, "Fail to decrypt password!").decode("utf-8")


def generate_hash_password(password: str) -> str:
    """
    Функция воспроизводит шифрование и дешифрование строки
    Возвращает хеш пароля
    """
    encrypted_password = encrypt_password(password)
    decrypted_password = decrypt_password(encrypted_password)
    return generate_password_hash(decrypted_password)
