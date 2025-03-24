from fastapi import Query, Body
from fastapi.routing import APIRouter
from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix='/hotels', tags=['Отели'])

HOTELS = [
    {'id': 1, 'title': 'Sochi', 'name': 'Sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'Dubai'}
]



@router.get('',
            summary='Получения списка отелей',
            description='Получение списка отелей по фильтрам id и title. Фильрацию можно делать как по одному фильтру, так и сразу по двум. При отправлке дефолтных значений для фильтров роутер отдаст весь список отелей.')
def get_hotels(
    id: int | None = Query(default=None, description="ID"),
    title: str | None = Query(default=None, description="Hotel name"),
) -> list[Hotel]:
    hotels_ = []
    for hotel in HOTELS:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post('',
             summary='Добавление отеля',
             description='Добавление отеля в базу данных. Необходимо предоставить title в теле запроса.')
def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={
        '1': {'summary':  'Сочи', 'value': {
                'title': 'Отель в Сочи 5 звезд',
                'name': 'Крутой отель алл ин казинузин'
        }},
        '2': {'summary':  'Дубай', 'value': {
            'title': 'Отель в Дубае 5 звезд',
            'name': 'Ред и Сон чиз блюа'
        }}}
)):
    global HOTELS
    HOTELS.append({
        'id': len(HOTELS) + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
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
  