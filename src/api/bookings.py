from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingCreateRequest, BookingCreate


router = APIRouter(prefix='/bookings', tags=['Бронирование номеров'])


@router.post('',
             summary='Добавление брони',
             description='Создание брони на номер в отеле')
async def create_booking(db: DBDep,
                         user_id: UserIdDep,
                         booking_data: BookingCreateRequest):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = None
    if room:
        _booking_data = BookingCreate(**booking_data.model_dump(), user_id=user_id, price=room.price)
        result = await db.bookings.add(_booking_data)
        await db.commit()
        return {'status': 'OK', 'data': result}
    raise HTTPException(status_code=404, detail='Номер не найден')
