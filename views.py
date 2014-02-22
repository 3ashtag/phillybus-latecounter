from counter import session
from models import Route, Base

from flask import Flask
from flask import render_template
app = Flask(__name__)
app.debug = True

@app.route('/minutes_late')
def minutes_late():
    total_late = 0
    latest_routes = []
    db_routes = session.query(Route).all()
    for route in db_routes:
        total_late += route.total_late_time

    db_routes = session.query(Route).order_by(Route.total_late_time.desc()).slice(0, 9)
    for route in db_routes:
        latest_routes.append({'name': route.name, 'total_late_time': route.total_late_time})

    print total_late
    print latest_routes
    return render_template('minutes_late.html', total_late=total_late, routes=latest_routes)
    

if __name__ == '__main__':
    app.run()
