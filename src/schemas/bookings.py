from pydantic import BaseModel
from datetime import date


class BookingCreateRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingCreate(BookingCreateRequest):
    user_id: int
    price: int
    

class Booking(BookingCreate):
    id: int
