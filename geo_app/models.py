from sqlalchemy import Column, Integer, String

from database import Base


class GeoField(Base):
    __tablename__ = 'fields'
    # metadata = meta
    id = Column(Integer, primary_key=True, index=True)
    gfield = Column(String)
    
    def __repr__(self) -> str:
        return self.gfield[:20] + "..."