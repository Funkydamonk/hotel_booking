from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('',
            summary='',
            description='')
async def get_facilities(db: DBDep):
    facilities = await db.facilities.get_all()
    return {'status': 'OK', 'data': facilities}


@router.post('',
             summary='',
             description='')
async def create_facility(db: DBDep,
                          facility_data: FacilityAdd):
    result = await db.facilities.add(data=facility_data)
    await db.commit()
    return {'status': 'OK', 'data': result}
