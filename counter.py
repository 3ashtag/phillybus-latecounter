import csv
import logging
import json
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Route, Bus, Base
engine = create_engine('sqlite:///counter.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.WARN)

def load_routes():
    route_names = []
    with open('routes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            route_names.append(row[1])

    route_names = route_names[1:]
    db_routes = session.query(Route, Route.name).all()
    db_route_names = []

    for route in db_routes:
        db_route_names.append(route.name)

    for name in route_names:
        if name not in db_route_names:
            session.add(Route(name, 0))
        else:
            print '%s already in the database' % name
    session.commit()

def check_buses():
    db_routes = session.query(Route, Route.name, Route.total_late_time).all()
    base_url = 'http://www3.septa.org/hackathon/TransitView/trips.php?route=%s'

    db_buses = session.query(Bus).all()
    db_bus_ids = []
    for bus in db_buses:
        db_bus_ids.append(bus.vehicle_id)

    for route in db_routes:
        req = requests.get(base_url % (route.name))
        try:
            route_offset = 0
            bus_dict = req.json()
            for bus in bus_dict['bus']:
                bus_id = int(bus['VehicleID'])
                bus_offset = int(bus['Offset'])
                if bus_id not in db_bus_ids:
                    print bus_offset
                    db_bus = Bus(route.name, bus_id, bus['Direction'], bus_offset)
                    print 'adding'
                    session.add(db_bus)
                    session.commit()
                else:
                    db_bus = session.query(Bus).filter_by(vehicle_id=bus['VehicleID']).first() 
                    if db_bus.direction == bus['Direction']:
                        if db_bus.max_offset < bus_offset:
                            session.query(Bus).filter_by(vehicle_id=bus['VehicleID']).update({"max_offset": bus_offset})
                    else:
                        route_offset += db_bus.max_offset
                        db_bus.max_offset = 0
                        db_bus.direction = bus['Direction']
                        session.query(Bus).filter_by(vehicle_id=bus['VehicleID']).update({"direction": bus['Direction']})
                    session.commit()

            session.query(Route).filter_by(name=route.name).update({'total_late_time': route.total_late_time + route_offset})
            session.commit()

        except ValueError:
            print "No info"
if __name__ == '__main__':
    #load_routes()
    check_buses()
