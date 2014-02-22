from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey


Base = declarative_base()

class Route(Base):
    __tablename__ = 'routes'
    def __init__(self, name=None, total_late_time=None):
        self.name = name
        self.total_late_time = total_late_time

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    total_late_time = Column(Integer)


class Bus(Base):
    __tablename__ = 'buses'
    def __init__(self, route_name=None, vehicle_id=None, direction = None, max_offset = None):
        self.route_name = route_name
        self.vehicle_id = vehicle_id
        self.direction = direction
        self.max_offset = max_offset

    id = Column(Integer, primary_key=True)
    route_name = Column(String(50))
    vehicle_id = Column(Integer, unique=True)
    direction =  Column(String(100))
    max_offset = Column(Integer)

