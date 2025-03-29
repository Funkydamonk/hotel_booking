from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

 
    def __init__(self, session):
        self.session = session
        

    async def get_filtered(self, **filtered_by):
        query = select(self.model).filter_by(**filtered_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model , from_attributes=True) for model in result.scalars().all()]
           
    async def get_all(self):
        return self.get_filtered()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)
        
    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model, from_attributes=True)
    
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = update(self.model).values(**data.model_dump(exclude_unset=exclude_unset)).filter_by(**filter_by)
        # print(stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(stmt)

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
