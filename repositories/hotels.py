from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel 

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset):
        query = select(HotelsOrm)
        if title:
            query = query.where(func.lower(HotelsOrm.__table__.c.title).contains(title.strip().lower()))
        if location:
            query = query.where(func.lower(HotelsOrm.__table__.c.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset((offset) * limit)
        )
        result = await self.session.execute(query)
            
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        