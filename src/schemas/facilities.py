from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int


class FacilityPatch(BaseModel):
    title: str | None = None


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
