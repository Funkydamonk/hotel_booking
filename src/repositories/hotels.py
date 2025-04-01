from datetime  import date

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from sqlalchemy import select, func
from src.schemas.hotels import Hotel
from src.repositories.utils import room_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel 


    async def get_filtered_by_date(
            self,
            date_from: date,
            date_to: date,
            title: str,
            location: str,
            limit: int,
            offset: int
    ):
        room_ids_to_get = room_ids_for_booking(date_from=date_from,
                                               date_to=date_to)
        hotel_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(room_ids_to_get))
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotel_ids_to_get))
        if title:
            query = (
                query
                .where(func.lower(self.model.title).contains(title.strip().lower()))
            )
        if location:
            query = (
                query
                .where(func.lower(self.model.location).contains(location.strip().lower()))
            )
        query = (
            query
            .limit(limit)
            .offset(offset)
        ) 
        
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
    