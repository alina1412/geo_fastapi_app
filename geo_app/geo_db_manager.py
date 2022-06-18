from databases import Database
from fastapi import HTTPException
import psycopg2
from pydantic import Json
from sqlalchemy.orm import Session


from .models import GeoField


class BaseRepository:
    def __init__(self, database: Database):
        self.database = database


# class FieldManager(BaseRepository):

async def get_all(db: Session, limit: int = 100, skip: int = 0):
    res = db.query(GeoField).offset(skip).limit(limit).all()
    return res


async def get_by_id(db: Session, id: int):
    response = db.query(GeoField).filter(GeoField.id == id).first()
    # print(type(response))
    return response


async def get_by_gfield(db: Session, field: Json):
    response = db.query(GeoField).filter(GeoField.gfield == field).first()
    if response is None:
        return None
    return response


async def ifexists_raise_error(db, field):
    was_in_db = await get_by_gfield(db=db, field=field)
    if was_in_db is not None:
        raise HTTPException(status_code=400, 
                            detail="data is already in db."+
                            f" id={was_in_db.id}")


async def create(db: Session, field: Json):
    await ifexists_raise_error(db=db, field=field)
    try:
        new_field = GeoField(gfield=field)
        db.add(new_field)
        db.commit()
        db.refresh(new_field)
        return new_field.id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail=f"Error: {type(e).__name__}")

    

# async def get_by_name(self, name: str):
#     return

async def delete(db: Session, id: int):
    try:
        _field = await get_by_id(db, id)
        if _field == None:
            return 404
        db.delete(_field)
        db.commit()
        return 200
    except:
        return 400
