from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def post_users(db: Session, raw_data: schemas.PostUsers):
    user_id: int = raw_data.user_id
    username: str = raw_data.username
    email: str = raw_data.email
    password_hash: str = raw_data.password_hash

    record_to_be_added = {
        "email": email,
        "user_id": user_id,
        "username": username,
        "password_hash": password_hash,
    }
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    add_records = new_users.to_dict()

    res = {
        "test": add_records,
    }
    return res


async def post_login(db: Session, raw_data: schemas.PostLogin):
    email: str = raw_data.email
    password_hash: str = raw_data.password_hash

    query = db.query(models.Users)
    query = query.filter(
        and_(models.Users.email == email, models.Users.password_hash == password_hash)
    )

    user_login = query.first()

    user_login = (
        (user_login.to_dict() if hasattr(user_login, "to_dict") else vars(user_login))
        if user_login
        else user_login
    )

    bs_jwt_payload = {
        "exp": int(
            (
                datetime.datetime.utcnow() + datetime.timedelta(seconds=100000)
            ).timestamp()
        ),
        "data": user_login,
    }

    jwt = jwt.encode(
        bs_jwt_payload,
        "N7FvUc2oQW8WgN+f3z9qYfRw2yRh5hJ4E8gH9zTDUUk=",
        algorithm="HS256",
    )

    res = {
        "user_login": user_login,
        "jwt": jwt,
    }
    return res


async def post_file_upload(db: Session, document: UploadFile):

    bucket_name = "ap-south-1"
    region_name = "cvGqVpfttA2pfCrvnpx8OG3jNfPPhfNeankyVK5A"
    file_path = "resources"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id="AKIATET5D5CPSTHVVX25",
        aws_secret_access_key="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",
        aws_session_token=None,  # Optional, can be removed if not used
        region_name="cvGqVpfttA2pfCrvnpx8OG3jNfPPhfNeankyVK5A",
    )

    # Read file content
    file_content = await document.read()

    name = document.filename
    file_path = file_path + "/" + name

    import mimetypes

    document.file.seek(0)

    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    s3_client.upload_fileobj(
        document.file, bucket_name, name, ExtraArgs={"ContentType": content_type}
    )

    file_type = Path(document.filename).suffix
    file_size = 200

    file_url = f"https://{bucket_name}.s3.amazonaws.com/{name}"

    self_hosted_url = file_url
    res = {
        "self_hosted_url": self_hosted_url,
    }
    return res
