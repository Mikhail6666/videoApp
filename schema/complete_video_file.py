from pydantic import BaseModel

class CompleteVideoFileSchema(BaseModel):
    id: int | None = None
    main_id: int | None = None
    name_complete_file: str | None = None
    path_complete_file: str | None = None

    class Config:
        from_attributes = True
