from sqlalchemy import select, func
from datetime import date
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.database import engine


def room_ids_for_booking(date_from: date,
                         date_to: date,
                         hotel_id: int | None = None):
    
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label('rooms_booked'))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from
        )
        .group_by(BookingsOrm.room_id)
        .cte(name='rooms_count')
    )
    rooms_availability = (
        select(
            RoomsOrm.id.label('room_id'), 
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('available_rooms'),
        ) 
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name='rooms_availability')
    )
    room_ids_for_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )
    if hotel_id is not None:
        room_ids_for_hotel = room_ids_for_hotel.filter_by(hotel_id=hotel_id)
    room_ids_for_hotel = (
        room_ids_for_hotel
        .subquery(name='room_ids_for_hotel')
    )
    room_ids = (
        select(rooms_availability.c.room_id)
        .select_from(rooms_availability)
        .filter(
            rooms_availability.c.available_rooms > 0,
            rooms_availability.c.room_id.in_(room_ids_for_hotel),
        )
    )

    # print(room_ids.compile(bind=engine, compile_kwargs={'literal_binds': True}))
    return room_ids

