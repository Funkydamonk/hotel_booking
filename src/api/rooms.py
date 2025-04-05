from fastapi import APIRouter, Query, Body
from datetime import date

from src.repositories.rooms import RoomsRepository
from src.models.facilities import RoomsFacilitiesOrm
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.schemas.facilities import RoomFacilityAdd
from src.api.dependencies import DBDep
from src.database import async_session_maker


router = APIRouter(prefix='/hotels/{hotel_id}/rooms', tags=['Комнаты'])


@router.get('',
            summary='Получение списка комнат отеля',
            description='Получения полного списка комнат выбранного отеля')
async def get_rooms(db: DBDep, 
                    hotel_id: int,
                    date_from: date = Query(example='2025-03-31'),
                    date_to: date = Query(example='2025-04-15')):
    data = await db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return {'status': 'OK', 'data': data}
    

@router.get('/{room_id}',
            summary='Получение конкретной комнаты',
            description='Получение комнанты по её id')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
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
                            'quantity': 2,
                            'facilities_ids': [

                            ]
                    }}})):
    _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
    room = await db.rooms.add(data=_room_data)
    
    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {'status': 'OK', 'data': room}


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
    _room_data = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id) 
    await db.rooms.edit(data=_room_data, id=room_id)
    room_facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
    room_facilities_ids = [rf.facility_id for rf in room_facilities]
    facilities_to_delete = [f_id for f_id in room_facilities_ids if f_id not in room_data.facilities_ids]
    facilities_to_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids if f_id not in room_facilities_ids]
    if facilities_to_delete:
        await db.rooms_facilities.delete(RoomsFacilitiesOrm.facility_id.in_(facilities_to_delete), room_id=room_id)
    if facilities_to_add:
        await db.rooms_facilities.add_bulk(facilities_to_add)
    await db.commit()
    return {'status': 'OK'}


@router.patch('/{room_id}',
              summary='Частичное изменение данных комнаты',
              description='Частичное изменение данных комнаты по id')
async def part_edit_room(db: DBDep, 
                         hotel_id: int,
                         room_id: int,
                         room_data: RoomPatchRequest):
    _room_data = RoomPatch(**room_data.model_dump(exclude_unset=True), hotel_id=hotel_id)
    await db.rooms.edit(id=room_id, data=_room_data, exclude_unset=True, hotel_id=hotel_id)

    if room_data.facilities_ids:
        room_facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
        room_facilities_ids = [rf.facility_id for rf in room_facilities]
        facilities_to_delete = [f_id for f_id in room_facilities_ids if f_id not in room_data.facilities_ids]
        facilities_to_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids if f_id not in room_facilities_ids]
        if facilities_to_delete:
            await db.rooms_facilities.delete(RoomsFacilitiesOrm.facility_id.in_(facilities_to_delete), room_id=room_id)
        if facilities_to_add:
            await db.rooms_facilities.add_bulk(facilities_to_add)
    await db.commit()
    return {'status': 'OK'}
        