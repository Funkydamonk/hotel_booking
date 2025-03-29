from fastapi import APIRouter, Query, Body

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPatch
from src.api.dependencies import PaginationDep, UserIdDep
from src.database import async_session_maker


router = APIRouter(prefix='/hotels/{hotel_id}/rooms', tags=['Комнаты'])


@router.get('',
            summary='Получение списка комнат отеля',
            description='Получения полного списка комнат выбранного отеля')
async def get_rooms(pagination: PaginationDep,
                    hotel_id: int,
                    title: str | None = Query(None),
                    description: str | None = Query(None),
                    price: int | None = Query(None),
                    quantity: int | None = Query(None)):
    per_page = pagination.per_page or 5
    page = (pagination.page - 1) * per_page
    async with async_session_maker() as session:
        data = await RoomsRepository(session).get_all(hotel_id=hotel_id,
                                                    title=title,
                                                    description=description,
                                                    price=price,
                                                    quantity=quantity,
                                                    limit=per_page,
                                                    offset=page)
        return {'status': 'OK', 'data': data}
    

@router.get('/{room_id}',
            summary='Получение конкретной комнаты',
            description='Получение комнанты по её id')
async def get_room(room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        return {'status': 'OK', 'data': room}


@router.post('',
             summary='Добавление комнаты',
             description='Добавление комнаты для конкретного отеля')
async def create_room(hotel_id: int, 
                      room_data: RoomAdd = Body(
                      openapi_examples={
                    '1': {'summary':  'Базовый номер', 'value': {
                            'hotel_id': 27,
                            'title': 'Базовый номер на 2-х',
                            'description': '',
                            'price': 1500,
                            'quantity': 2
                    }}})):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add(data=room_data)
        await session.commit()
        return {'status': 'OK', 'data': result}


@router.delete('/{room_id}',
               summary='Удаление комнаты',
               description='Удаление комнаты у конкретного отеля по id')
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
        return {'status': 'OK'}
    

@router.put('/{room_id}',
            summary='Полное измение данных комнаты',
            description='Полное изменение данных комнаты')
async def edit_room(room_id: int,
                    hotel_id: int,
                    room_data: RoomAdd):
    room_data.hotel_id = hotel_id
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, data=room_data)
        await session.commit()
        return {'status': 'OK'}


@router.patch('/{room_id}',
              summary='Частичное изменение данных комнаты',
              description='Частичное изменение данных комнаты по id')
async def part_edit_room(room_id: int,
                         room_data: RoomPatch):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, data=room_data, exclude_unset=True)
        await session.commit()
        return {'status': 'OK'}
        