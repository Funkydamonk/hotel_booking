from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomWithRels
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
        
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(self.model.id.in_(room_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model, from_attributes=True)
