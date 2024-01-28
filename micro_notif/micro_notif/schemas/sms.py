from pydantic import BaseModel, Field


class SMSEvent(BaseModel):
    to: str = Field(pattern=r"^09\d{9}$")
    message: str
