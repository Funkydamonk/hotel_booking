from fastapi import APIRouter
from passlib.context import CryptContext

from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository




router = APIRouter(prefix='/auth', tags=['Authenticate and Authorize'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/register',
             summary='Sign up endpoint',
             description='To sign up you need to provide a valid email and a password')
async def register_user(
    data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        
        return {'status': 'ok'}
    