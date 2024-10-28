from datetime import datetime


from pydantic import BaseModel

class ViolationsSchema(BaseModel):
    id: int | None = None
    main_id: int | None = None
    photo: str | None = None
    video: str | None = None
    category: str | None = None
    confidence: str | None = None
    datetime: datetime
    camera: str | None = None
    field: str | None = None
    well_pad: str | None = None
    color: str | None = None
    sn: int | None = None

    class Config:
        from_attributes = True
