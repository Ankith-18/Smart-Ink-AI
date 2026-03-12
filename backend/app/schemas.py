from pydantic import BaseModel


class InkRequest(BaseModel):
    image_base64: str
    text_hint: str | None = None
