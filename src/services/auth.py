from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from src.config import settings
from fastapi.exceptions import HTTPException



class AuthService:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    
    def create_access_token(self, data: dict ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire} 
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token,
                            settings.SECRET_KEY,
                            algorithms=settings.ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail='Неверный токен')
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Токен невалиден')
        