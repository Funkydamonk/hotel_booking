from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn


app = FastAPI()


HOTELS = [
    {'id': 1, 'title': 'Sochi', 'name': 'Sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'Dubai'}
]


@app.get('/hotels')
def get_hotels(
    id: int | None = Query(default=None, description="ID"),
    title: str | None = Query(default=None, description="Hotel name"),
):
    hotels_ = []
    for hotel in HOTELS:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post('/hotels')
def create_hotel(title: str = Body(embed=True)):
    global HOTELS
    HOTELS.append({
        'id': len(HOTELS) + 1,
        'title': title
    })
    return {'status': 'ok'}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global HOTELS
    HOTELS = [hotel for hotel in HOTELS if hotel['id'] != hotel_id]
    return {'status': 'ok'}


@app.put('/hotels/{hotel_id}')
def change_hotel(hotel_id: int,
                 title: str = Body(),
                 name: str = Body()):
    global HOTELS
    if not any([hotel['id'] == hotel_id for hotel in HOTELS]):
        return {'error': 'No such hotel id'}

    for i, hotel in enumerate(HOTELS):
        if hotel['id'] == hotel_id:
            HOTELS[i]['title'] = title
            HOTELS[i]['name'] = name
            break
    return {'status': 'ok'}


@app.patch('/hotels/{hotel_id}')
def alter_hotel(hotel_id: int,
                title: str | None = Body(default=None),
                name: str | None = Body(default=None)):
    if not any([hotel['id'] == hotel_id for hotel in HOTELS]):
        return {'error': 'No such hotel id'}
    if title is None and name is None:
        return {'error': 'You must provide at least 1 value'}
    for i, hotel in enumerate(HOTELS):
        if hotel['id'] == hotel_id:
            if title:
                HOTELS[i]['title'] = title
            if name:
                HOTELS[i]['name'] = name
            break
    return {'status': 'ok'}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
     return get_swagger_ui_html(
         openapi_url=app.openapi_url,
         title=app.title + " - Swagger UI",
         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
         swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
         swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
     )


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
