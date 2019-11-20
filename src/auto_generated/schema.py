import sqlalchemy
from sqlalchemy import text, Column, String, Integer, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# note: should we be worried about tracking actual IDs of vehicle position events and alerts? differential mode for gtfs doesn't seem to work so I'll ignore it.

class Route(Base):
	__tablename__ = 'routes'
	id = Column(String(5), primary_key=True)
	agency_id = Column(String)
	route_short_name = Column(String)
	route_long_name = Column(String)
	route_desc = Column(String)
	route_type = Column(Integer)
	route_url = Column(Integer)
	route_color = Column(String)
	route_text_color = Column(String)

	realtime_trips = relationship('RealtimeTrip')
	alerts = relationship('Alert')


class RealtimeTrip(Base):
	__tablename__ = 'realtime_trips'
	id = Column(String(30), primary_key=True)
	observed_at = Column(Integer)
	start_date = Column(String(10))
	route_id = Column(String(5),ForeignKey('routes.id'))
	direction = Column(String(10))
	is_assigned = Column(Boolean)
	train_description = Column(String(30))

	route = relationship('Route', back_populates='realtime_trips')
	vehicle_moved_events = relationship('RealtimeTrainMoved')
	alerts = relationship('Alert')
	
	def __repr__(self):
		return  'RealtimeTrip(%s, %s)' % (self.id, self.route_id)

class Stop(Base):
	__tablename__ = 'stops'
	id = Column(String(10), primary_key=True) # will be autoincrement
	stop_code = Column(String)
	stop_name = Column(String)
	stop_desc = Column(String)
	stop_lat = Column(Float)
	stop_lon = Column(Float)
	zone_id = Column(String)
	stop_url = Column(String)
	location_type = Column(Integer)
	parent_station = Column(String) # really should be foreign key into same table but that's complicated

	vehicle_updates = relationship('RealtimeTrainMoved')
	alerts = relationship('Alert')
	
class RealtimeTrainMoved(Base):
	__tablename__ = 'realtime_vehicle_moved'
	id = Column(Integer, primary_key=True) # will be autoincrement
	realtime_trip_id = Column(String(30), ForeignKey('realtime_trips.id'))
	stop_id = Column(String(10), ForeignKey('stops.id'))
	current_stop_sequence = Column(Integer)
	current_status = Column(String(20))
	last_moved_time = Column(Integer)

	realtime_trip = relationship('RealtimeTrip', back_populates='vehicle_moved_events')
	stop = relationship('Stop', back_populates='vehicle_updates')
	
	def __repr__(self):
		return  'RealtimeTrainMoved(%s, %s)' % (self.id, self.realtime_trip_id)

class Alert(Base):
	__tablename__ = 'alerts'
	id = Column(Integer, primary_key=True) # will be autoincrement
	# could be one of three types of alerts (only one will be non null)
	realtime_trip_id = Column(String(30), ForeignKey('realtime_trips.id'))
	route_id = Column(String(5), ForeignKey('routes.id'))
	stop_id = Column(String(10), ForeignKey('stops.id'))
	observed_at = Column(Integer)
	message = Column(String)

	realtime_trip = relationship('RealtimeTrip', back_populates='alerts')
	stop = relationship('Stop', back_populates='alerts')
	route = relationship('Route', back_populates='alerts')

	def __repr__(self):
		return  'Alert(%s, %s, %s, %s)' % (self.message, self.stop_id, self.route_id, self.realtime_trip_id)

