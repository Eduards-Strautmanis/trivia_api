# Correct setup found on this website:
# https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  address = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=False)
  genres = db.Column(db.ARRAY(db.String), nullable=False)
  image_link = db.Column(db.String(500), nullable=False)
  facebook_link = db.Column(db.String(120), nullable=False)
  website_link = db.Column(db.String(120), nullable=False)
  looking_for_talent = db.Column(db.Boolean, nullable=False, default=False)
  seeking_description = db.Column(db.String(500), nullable=False)
  shows = db.relationship('Show', backref='venue', lazy="joined")

class Artist(db.Model):
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=False)
  genres = db.Column(db.ARRAY(db.String), nullable=False)
  image_link = db.Column(db.String(500), nullable=False)
  facebook_link = db.Column(db.String(120), nullable=False)
  website_link = db.Column(db.String(120), nullable=False)
  looking_for_venues = db.Column(db.Boolean, nullable=False, default=False)
  seeking_description = db.Column(db.String(500), nullable=False)
  shows = db.relationship('Show', backref='artist', lazy="joined")

class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  date_time = db.Column(db.DateTime, nullable=False)
