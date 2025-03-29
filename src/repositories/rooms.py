from sqlalchemy import select, func
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    # async def get_all(self,
    #                   hotel_id,
    #                   title,
    #                   description,
    #                   price,
    #                   quantity,
    #                   limit,
    #                   offset):
    #     query = select(RoomsOrm)
    #     if title:
    #         query = query.where(func.lower(RoomsOrm.__table__.c.title).contains(title.strip().lower()))
    #     if description:
    #         query = query.where(func.lower(RoomsOrm.__table__.c.location).contains(description.strip().lower()))
    #     if price:
    #         query = query.where(RoomsOrm.__table__.c.price == price)
    #     if quantity:
    #         query = query.where(RoomsOrm.__table__.c.quantity == quantity)    
    #     query = (
    #         query
    #         .where(RoomsOrm.__table__.c.hotel_id == hotel_id)
    #         .limit(limit)
    #         .offset((offset) * limit)
    #     )
    #     result = await self.session.execute(query)
            
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        