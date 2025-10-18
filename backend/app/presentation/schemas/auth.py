from pydantic import BaseModel, Field


class PhoneIn(BaseModel):
    phone: str = Field(..., pattern=r"^\+\d{10,15}$")


class OTPVerifyIn(BaseModel):
    phone: str
    code: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CompanySignupIn(BaseModel):
    email: str
    password: str
    name: str


class CompanyLoginIn(BaseModel):
    email: str
    password: str


class AdminSignupIn(BaseModel):
    email: str
    password: str
    signup_token: str


class AdminLoginIn(BaseModel):
    email: str
    password: str
