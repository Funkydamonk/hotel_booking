from sqlalchemy import select, func
from datetime import date
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from src.models.bookings import BookingsOrm
from src.database import engine
from src.repositories.utils import room_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def get_filtered_by_date(self, 
                                   hotel_id, 
                                   date_from: date, 
                                   date_to: date):
        
        room_ids_to_get = room_ids_for_booking(hotel_id=hotel_id,
                                               date_from=date_from,
                                               date_to=date_to)
        result = await self.get_filtered(self.model.id.in_(room_ids_to_get))
        return result