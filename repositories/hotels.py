from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func


class HotelsRepository(BaseRepository):
    model = HotelsOrm

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
            
        return result.scalars().all()
        