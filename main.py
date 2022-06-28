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
from geo_app.database import SessionLocal, engine, get_db
import geo_app.geo_db_manager as gmanager
from geo_app import crud

models.Base.metadata.create_all(bind=engine)


app = FastAPI()



# GET LIST ALL
@app.get("/geolist/", response_model=list[schemas.FieldBase])
async def get_geolist(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = await crud.read_all(db=db, skip=skip, limit=limit)
    logger.debug(f"CHECK___")
    return items


# GET ONE
@app.get("/get-json/{id}", status_code=status.HTTP_200_OK,
                response_model=schemas.FieldBase)
async def get_json(id: int, db: Session = Depends(get_db)):
    params = {'id': id}
    response = await crud.read_one(db, params)
    if response:
        print(response.gfield)
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# ADD CREATE
@app.post("/json/", status_code=status.HTTP_201_CREATED)
async def add_geo_json(new_json: dict, db: Session = Depends(get_db)):
    new_json = json.dumps(new_json)
    new_json_id: int = await gmanager.save_field(db=db, field=new_json)
    return new_json_id
    

# DELETE
@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_geo_json(id: int, db: Session = Depends(get_db)):
    await gmanager.delete_by_id(db=db, id=id)
    return


if __name__ == "__main__":
    app_settings = Settings()
    uvicorn.run("main:app",
                port=app_settings.server_port,
                host=app_settings.server_host,
                reload=True
                )
