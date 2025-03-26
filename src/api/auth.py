from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
import jwt
from src.config import settings

from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository




router = APIRouter(prefix='/auth', tags=['Authenticate and Authorize'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict ) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire} 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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


@router.post('/login',
             summary='',
             description='')
async def login_user(data: UserRequestAdd,
                     response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='Incorrect user or password')
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Incorrect user or password')
        access_token = create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}
    