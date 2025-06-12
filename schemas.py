from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Users(BaseModel):
    user_id: int
    username: str
    email: str
    password_hash: str


class ReadUsers(BaseModel):
    user_id: int
    username: str
    email: str
    password_hash: str
    class Config:
        from_attributes = True




class PostUsers(BaseModel):
    user_id: int = Field(...)
    username: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)
    password_hash: str = Field(..., max_length=100)

    class Config:
        from_attributes = True



class PostLogin(BaseModel):
    email: str = Field(max_length=100)

    @field_validator('email')
    def validate_email(cls, value: Optional[str]):
        if value is None:
            if True:
                return value
            else:
                raise ValueError("Field 'email' cannot be None")
        # Ensure re is imported in the generated file
        pattern= r'''^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'''  
        if isinstance(value, str) and not re.match(pattern, value):
            # Use repr() for the regex pattern in the error for clarity
            raise ValueError(f"Field '{schema.key}' does not match regex pattern: {repr(schema.regularExpression)}")
        return value
    password_hash: str = Field(max_length=100)

    @field_validator('password_hash')
    def validate_password_hash(cls, value: Optional[str]):
        if value is None:
            if True:
                return value
            else:
                raise ValueError("Field 'password_hash' cannot be None")
        # Ensure re is imported in the generated file
        pattern= r'''^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'",.<>/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|;:'",.<>/?]{8,}$'''  
        if isinstance(value, str) and not re.match(pattern, value):
            # Use repr() for the regex pattern in the error for clarity
            raise ValueError(f"Field '{schema.key}' does not match regex pattern: {repr(schema.regularExpression)}")
        return value

    class Config:
        from_attributes = True

