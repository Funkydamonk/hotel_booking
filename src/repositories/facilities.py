from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility


    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(query)
        current_facilities_ids = res.scalars().all()

        facilities_to_delete = list(set(current_facilities_ids) - set(facilities_ids))
        facilities_to_add = list(set(facilities_ids) - set(current_facilities_ids))
        facilities_to_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add]
        if facilities_to_delete:
            await self.delete(self.model.facility_id.in_(facilities_to_delete), room_id=room_id)
        if facilities_to_add:
            await self.add_bulk(facilities_to_add)
