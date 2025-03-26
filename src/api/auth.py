from fastapi import APIRouter
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from repositories.users import UsersRepository


router = APIRouter('/auth', tags=['Authenticate and Authorize'])

@router.post('/register',
             summary='',
             description='')
async def register_user(
    data: UserRequestAdd
):
    hashed_password = ...
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(data=data)
        await session.commit()
        
        return {'status': 'ok'}