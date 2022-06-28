from sqlalchemy.orm import Session

from .models import GeoField

# from fastapi import Depends
from geo_app.database import get_db

async def create(db: Session, field):
    new_field = GeoField(gfield=field)
    db.add(new_field)
    db.commit()
    db.refresh(new_field)
    return new_field.id


async def read_all(db: Session, limit: int = 100, skip: int = 0):
    response = db.query(GeoField).offset(skip).limit(limit).all()
    return response


async def read_one(db: Session, kwargs):
    response = db.query(GeoField).filter_by(**kwargs).one_or_none()
    # response = db.query(GeoField).filter(GeoField.id == id).first()
    return response


async def update(db: Session):
    ...


async def delete(db: Session, item):
    db.delete(item)
    db.commit()


def count():
    db = get_db().__next__()
    num_rows = db.query(GeoField).count()
    return num_rows
