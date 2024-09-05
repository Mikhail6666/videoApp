from pydantic import BaseModel

class CompletePngFileSchema(BaseModel):
    id: int | None = None
    main_id: int | None = None
    name_complete_png_file: str | None = None
    path_complete_png_file: str | None = None

    class Config:
        from_attributes = True