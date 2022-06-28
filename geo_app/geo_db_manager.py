from fastapi import HTTPException
from pydantic import Json
from sqlalchemy.orm import Session

from geo_app import crud


async def save_field(db: Session, field: Json):
    params = {"gfield": field}
    was_in_db = await crud.read_one(db, params)
    if was_in_db is None:
        new_id = await crud.create(db, field)
        return new_id

    raise HTTPException(status_code=400, 
                        detail="data is already in db."+
                        f" id={was_in_db.id}")


async def delete_by_id(db: Session, id: int):
    try:
        params = {"id": id}
        item = await crud.read_one(db, params)
        if item:
            await crud.delete(db, item)
            return
        raise HTTPException(status_code=404,
                            detail="Item not found")
    except Exception as ex:
        raise ex
