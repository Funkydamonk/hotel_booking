from fastapi import Query, Body, Depends

from fastapi.routing import APIRouter

from sqlalchemy import insert, select

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm


router = APIRouter(prefix='/hotels', tags=['Отели'])



@router.get('',
            summary='Получения списка отелей',
            description='Получение списка отелей по фильтрам id и title. Фильрацию можно делать как по одному фильтру, так и сразу по двум. При отправлке дефолтных значений для фильтров роутер отдаст весь список отелей.')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Hotel name"),
    location: str | None = Query(default=None, description="Hotel location")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.where(HotelsOrm.__table__.c.title.like(f'%{title}%'))
        if location:
            query = query.where(HotelsOrm.__table__.c.location.like(f'%{location}%'))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels    


@router.post('',
             summary='Добавление отеля',
             description='Добавление отеля в базу данных. Необходимо предоставить title и location в теле запроса.')
async def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={
        '1': {'summary':  'Сочи', 'value': {
                'title': 'Отель у моря',
                'location': 'Сочи, ул. Новороссийская'
        }},
        '2': {'summary':  'Дубай', 'value': {
            'title': 'Отель 5 звезд',
            'location': 'Дубай, ул. Абдулы'
        }}}
)):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {'status': 'ok'}


@router.delete('/{hotel_id}',
               summary='Удаление отеля',
               description='Удаление отеля по его id в базе данных.')
def delete_hotel(hotel_id: int):
    global HOTELS
    HOTELS = [hotel for hotel in HOTELS if hotel['id'] != hotel_id]
    return {'status': 'ok'}


@router.put('/{hotel_id}',
            summary='Полное обновление данных по отелю',
            description='Полное обновление данных по отелю. Необходимые переменные title и name')
def edit_hotel(hotel_id: int,
               hotel_data: Hotel):
    global HOTELS
    if not any([hotel['id'] == hotel_id for hotel in HOTELS]):
        return {'error': 'No such hotel id'}

    for i, hotel in enumerate(HOTELS):
        if hotel['id'] == hotel_id:
            HOTELS[i]['title'] = hotel_data.title
            HOTELS[i]['name'] = hotel_data.name
            break
    return {'status': 'ok'}


@router.patch('/{hotel_id}', 
           summary='Частичное обновление данных об отеле',
           description='Частично обновляем данные об отеле. Необходимо предоставить значение хотя бы для одной переменной title или name, или сразу оба значения.')
def part_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    if not any([hotel['id'] == hotel_id for hotel in HOTELS]):
        return {'error': 'No such hotel id'}
    if hotel_data.title is None and hotel_data.name is None:
        return {'error': 'You must provide at least 1 value'}
    for i, hotel in enumerate(HOTELS):
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                HOTELS[i]['title'] = hotel_data.title
            if hotel_data.name:
                HOTELS[i]['name'] = hotel_data.name
            break
    return {'status': 'ok'}
  