from pydantic import BaseModel

class VideoFileSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    file_path: str | None = None
    status: str | None = None

    class Config:
        from_attributes = True
