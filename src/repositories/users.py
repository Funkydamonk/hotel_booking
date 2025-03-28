from sqlalchemy import select
from pydantic import EmailStr
from repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User 
 
    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
        