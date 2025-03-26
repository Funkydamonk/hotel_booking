from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.services.auth import AuthService


router = APIRouter(prefix='/auth', tags=['Authenticate and Authorize'])


@router.post('/register',
             summary='Sign up endpoint',
             description='To sign up you need to provide a valid email and a password')
async def register_user(
    data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(password=data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        
        return {'status': 'ok'}


@router.post('/login',
             summary='',
             description='')
async def login_user(data: UserRequestAdd,
                     response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        auth_service = AuthService()
        if not user:
            raise HTTPException(status_code=401, detail='Incorrect user or password')
        if not auth_service.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Incorrect user or password')
        access_token = auth_service.create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}
    