#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
    format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
    format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  current_time = datetime.now()
  data = []
  all_areas = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  for area in all_areas:
    venue_data = []
    venues = Venue.query.all();
    for venue in venues:
      shows = Show.query.filter_by(venue_id=venue.id).filter(Show.date_time>current_time).all()
      if venue.city == area[0] and venue.state == area[1]:
        venue_data.append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(shows)
        })
    data.append({
      'city': area[0],
      'state': area[1],
      'venues': venue_data
    })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  data = []
  current_time = datetime.now()
  search = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike("%"+search+"%")).all()
  for venue in venues:
    shows = Show.query.filter_by(venue_id=venue.id).filter(Show.date_time>current_time).all()
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(shows)
    })
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data1 = []
  try:
    venues = Venue.query.all()
    current_time = datetime.now()
    for venue in venues:
      past_shows = []
      upcoming_shows = []
      # Join statement
      shows = venue.shows
      for show in shows:
        artist = Artist.query.filter_by(id=show.artist_id).first()
        if show.date_time > current_time:
          upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.date_time.strftime("%d/%m/%Y, %H:%M")
          })
        else:
          past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.date_time.strftime("%d/%m/%Y, %H:%M")
          })
      data1.append({
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.looking_for_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
      })
  except Exception as e:
    flash(e)
    pass
  data = list(filter(lambda d: d['id'] == venue_id, data1))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      venue = Venue(
        name=form.name.data,
        genres=form.genres.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        looking_for_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data)
      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    error = True
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
  if error == False:
    flash('Venue ' + form.name.data + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    db.session.delete(venue)
    db.session.commit()
  except Exception as e:
    flash(e)
    db.session.rollback()
    pass
  finally:
    db.session.close()
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  artists = Artist.query.all()
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  data = []
  current_time = datetime.now()
  search = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike("%"+search+"%")).all()
  for artist in artists:
    shows = Show.query.filter_by(artist_id=artist.id).filter(Show.date_time>current_time).all()
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": len(shows)
    })
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data1 = []
  try:
    artists = Artist.query.all()
    current_time = datetime.now()
    for artist in artists:
      past_shows = []
      upcoming_shows = []
      # Join statement
      shows = artist.shows
      for show in shows:
        venue = Venue.query.filter_by(id=show.venue_id).first()
        if show.date_time > current_time:
          upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.date_time.strftime("%d/%m/%Y, %H:%M")
          })
        else:
          past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.date_time.strftime("%d/%m/%Y, %H:%M")
          })
      data1.append({
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.looking_for_venues,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
      })
  except Exception as e:
    flash(e)
    pass
  data = list(filter(lambda d: d['id'] == artist_id, data1))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  try:
    artist = Artist.query.filter_by(id=artist_id).first()
    # Note, it seems redundant to create the artist_data dictionary. However,
    # it's passed through to the edit_artist_submission function, so I'll leave
    # it. It's not actually used there, so I'm not sure what the point of
    # passing it through is.
    artist_data = {
      "id": artist_id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website_link,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.looking_for_venues,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link
    }
    form.name.data = artist_data['name']
    form.genres.data = artist_data['genres']
    form.city.data = artist_data['city']
    form.state.data = artist_data['state']
    form.phone.data = artist_data['phone']
    form.website_link.data = artist_data['website']
    form.facebook_link.data = artist_data['facebook_link']
    form.image_link.data = artist_data['image_link']
    form.seeking_venue.data = artist_data['seeking_venue']
    form.seeking_description.data = artist_data['seeking_description']
  except Exception as e:
    flash(e)
    pass
  return render_template('forms/edit_artist.html', form=form, artist=artist_data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(meta={'csrf': False})
  if form.validate():
    try:
      artist = Artist.query.filter_by(id=artist_id).first()
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = form.genres.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.website_link = form.website_link.data
      artist.looking_for_venues = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      flash(e)
      pass
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    venue_data = {
      "id": venue_id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website_link,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.looking_for_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link
    }
    form.name.data = venue_data['name']
    form.genres.data = venue_data['genres']
    form.address.data = venue_data['address']
    form.city.data = venue_data['city']
    form.state.data = venue_data['state']
    form.phone.data = venue_data['phone']
    form.website_link.data = venue_data['website']
    form.facebook_link.data = venue_data['facebook_link']
    form.image_link.data = venue_data['image_link']
    form.seeking_talent.data = venue_data['seeking_talent']
    form.seeking_description.data = venue_data['seeking_description']
  except Exception as e:
    flash(e)
    pass
  return render_template('forms/edit_venue.html', form=form, venue=venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(meta={'csrf': False})
  if form.validate():
    try:
      venue = Venue.query.filter_by(id=venue_id).first()
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.genres = form.genres.data
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.website_link = form.website_link.data
      venue.looking_for_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      flash(e)
      pass
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form, meta={'csrf': False})
  error = False
  if form.validate():
    try:
      artist = Artist(
        name=form.name.data,
        genres=form.genres.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        looking_for_venues=form.seeking_venue.data,
        seeking_description=form.seeking_description.data)
      db.session.add(artist)
      db.session.commit()
    except Exception as e:
      error = True
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    error = True
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
  if error == False:
    flash('Artist ' + form.name.data + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  try:
    shows = Show.query.all()
    for show in shows:
      artist = Artist.query.filter_by(id=show.artist_id).first()
      venue = Venue.query.filter_by(id=show.venue_id).first()
      data.append({
        "venue_id": show.venue_id,
        "venue_name": venue.name,
        "artist_id": show.artist_id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.date_time.strftime("%d/%m/%Y, %H:%M")
      })
  except Exception as e:
    flash(e)
    pass
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  form = ShowForm(request.form)
  try:
    show = Show(artist_id=form.artist_id.data,
      venue_id=form.venue_id.data,
      date_time=form.start_time.data)
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  if error == False:
    flash('Show was successfully listed!')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
