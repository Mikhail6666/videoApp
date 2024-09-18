from pydantic import BaseModel

class ViolationsSchema(BaseModel):
    id: int | None = None
    main_id: int | None = None
    photo: str | None = None
    video: str | None = None
    category: str | None = None
    confidence: str | None = None
    date: str | None = None
    time: str | None = None
    camera: str | None = None
    field: str | None = None
    well_pad: str | None = None
    color: str | None = None

    class Config:
        from_attributes = True
