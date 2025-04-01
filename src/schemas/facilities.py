from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int


class FacilityPatch(BaseModel):
    title: str | None = None
    