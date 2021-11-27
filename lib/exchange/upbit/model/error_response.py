from pydantic import BaseModel


class Error(BaseModel):
    message: str
    name: str


class ErrorResponse(BaseModel):
    error: Error

