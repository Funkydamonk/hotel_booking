from fastapi import APIRouter, Query, Body

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.api.dependencies import DBDep
from src.database import async_session_maker


router = APIRouter(prefix='/hotels/{hotel_id}/rooms', tags=['Комнаты'])


@router.get('',
            summary='Получение списка комнат отеля',
            description='Получения полного списка комнат выбранного отеля')
async def get_rooms(db: DBDep, hotel_id: int):
    data = await db.rooms.get_filtered(hotel_id=hotel_id)
    return {'status': 'OK', 'data': data}
    

@router.get('/{room_id}',
            summary='Получение конкретной комнаты',
            description='Получение комнанты по её id')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.get_one_or_none(id=room_id, hotel_id=hotel_id)
    return {'status': 'OK', 'data': room}


@router.post('',
             summary='Добавление комнаты',
             description='Добавление комнаты для конкретного отеля')
async def create_room(db: DBDep, 
                      hotel_id: int, 
                      room_data: RoomAddRequest = Body(
                      openapi_examples={
                    '1': {'summary':  'Базовый номер', 'value': {
                            'title': 'Базовый номер на 2-х',
                            'description': '',
                            'price': 1500,
                            'quantity': 2
                    }}})):
    _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
    result = await db.rooms.add(data=_room_data)
    await db.commit()
    return {'status': 'OK', 'data': result}


@router.delete('/{room_id}',
               summary='Удаление комнаты',
               description='Удаление комнаты у конкретного отеля по id')
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {'status': 'OK'}
    

@router.put('/{room_id}',
            summary='Полное измение данных комнаты',
            description='Полное изменение данных комнаты')
async def edit_room(db: DBDep, 
                    hotel_id: int,
                    room_id: int,
                    room_data: RoomAddRequest):
    _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id, room_id=room_id) 
    await db.rooms.edit(id=room_id, data=_room_data)
    await db.commit()
    return {'status': 'OK'}


@router.patch('/{room_id}',
              summary='Частичное изменение данных комнаты',
              description='Частичное изменение данных комнаты по id')
async def part_edit_room(db: DBDep, 
                         hotel_id: int,
                         room_id: int,
                         room_data: RoomPatchRequest):
    _room_data = RoomPatch(**room_data.model_dump(), hotel_id=hotel_id)
    await db.edit(id=room_id, data=room_data, exclude_unset=True, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK'}
        