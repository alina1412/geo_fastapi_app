import json
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import uvicorn

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import geo_app.models as models, geo_app.schemas as schemas
from geo_app.settings import Settings
from geo_app.database import SessionLocal, engine
# from geo_db_manager import FieldManager
import geo_app.geo_db_manager as gmanager

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#########
from ee_app import register, earth_manager
url = earth_manager.example4()
logger.debug(f"CHECK___ {url}")
# register.google_register(Settings().DEBUG)
#########


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/geolist/", response_model=list[schemas.FieldBase])
async def get_geolist(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = await gmanager.get_all(db=db, skip=skip, limit=limit)
    logger.debug(f"CHECK___")
    return items


@app.get("/get-json/{geo_id}")  # response_model=Union[models.GeoField, None]
async def get_json(geo_id: int, db: Session = Depends(get_db)):
    # FM = FieldManager(db=db)
    response = await gmanager.get_by_id(db=db, id=geo_id)
    if type(response) == models.GeoField:
        print(response.gfield)
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/json/", status_code=status.HTTP_201_CREATED)
async def add_geo_json(new_json: dict, db: Session = Depends(get_db)):
    new_json = json.dumps(new_json)
    new_json_id: int = await gmanager.create(db=db, field=new_json)
    return new_json_id
    

@app.get("/delete/", status_code=status.HTTP_200_OK)
async def delete_geo_json(id: int, db: Session = Depends(get_db)):
    response: int = await gmanager.delete(db=db, id=id)
    if response != 200:
        if response == 404:
            raise HTTPException(status_code=404,
                                detail="Item not found")
        raise HTTPException(status_code=response)


if __name__ == "__main__":
    app_settings = Settings()
    uvicorn.run("main:app",
                port=app_settings.server_port,
                host=app_settings.server_host,
                # log_config=app_settings.LOGGING_CONFIG,
                # log_level="debug",
                reload=True)
