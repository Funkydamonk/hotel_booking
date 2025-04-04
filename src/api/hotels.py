from fastapi import Query, Body

from fastapi.routing import APIRouter
from datetime import date

from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker


router = APIRouter(prefix='/hotels', tags=['Отели'])



@router.get('',
            summary='Получения списка отелей',
            description='Получение списка отелей по фильтрам id и title. Фильрацию можно делать как по одному фильтру, так и сразу по двум. При отправлке дефолтных значений для фильтров роутер отдаст весь список отелей.')
async def get_hotels(
                    pagination: PaginationDep,
                    db: DBDep,
                    title: str | None = Query(default=None, description="Hotel name"),
                    location: str | None = Query(default=None, description="Hotel location"),
                    date_from: date = Query(example='2025-03-31'),
                    date_to: date = Query(example='2025-04-15')
):
    per_page = pagination.per_page or 5 
    page = (pagination.page - 1) * per_page
    return await db.hotels.get_filtered_by_date(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=page
    )


@router.get('/{hotel_id}')
async def get_hotel(db: DBDep, hotel_id: int):
    result = await db.hotels.get_one_or_none(id=hotel_id)
    return result


@router.post('',
             summary='Добавление отеля',
             description='Добавление отеля в базу данных. Необходимо предоставить title и location в теле запроса.')
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(
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
    hotel = await db.hotels.add(data=hotel_data)
    await db.commit()
    return {'status': 'ok', 'data': hotel}


@router.delete('/{hotel_id}',
               summary='Удаление отеля',
               description='Удаление отеля по его id в базе данных.')
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'ok'}


@router.put('/{hotel_id}',
            summary='Полное обновление данных по отелю',
            description='Полное обновление данных по отелю. Необходимые переменные title и name')
async def edit_hotel(db: DBDep, 
                     hotel_id: int | None,
                     hotel_data: HotelAdd):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'ok'}


@router.patch('/{hotel_id}', 
           summary='Частичное обновление данных об отеле',
           description='Частично обновляем данные об отеле. Необходимо предоставить значение хотя бы для одной переменной title или name, или сразу оба значения.')
async def part_edit_hotel(db: DBDep, 
                          hotel_id: int, 
                          hotel_data: HotelPATCH):
    await db.hotels.edit(data=hotel_data, id=hotel_id, exclude_unset=True,)
    await db.commit()
    return {'status': 'ok'}
  