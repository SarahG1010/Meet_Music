#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
## import migrate
from flask_migrate import Migrate
## import itertools
import itertools
##
from sqlalchemy import exc, and_


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
## define migrate
migrate = Migrate(app, db)



# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
    ## initialize venue model:
    def __init__(self, name, genres, city, state, address, phone,image_link, facebook_link,website,seeking_talent,seeking_description):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.facebook_link = facebook_link
        self.image_link = image_link
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description

    ## initiate __getitem__ method for easy access the venue object
    ## accessing items using square bracket notation ([]) on instances of a class
    def __getitem__(self, key):
        return getattr(self, key)


    ## initiate __repr__ method for define a string representation of an object
    ## debug prupose
    def __repr__(self):
        return f'<Venue name={self.name}, city={self.city}, state={self.state}, address={self.address}, past_shows_count={self.past_shows_count}, upcoming_shows_count={self.upcoming_shows_count}>'


    ## define show_template for venue model
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres.split(', '),
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': self.past_shows,
            'upcoming_shows': self.upcoming_shows,
            'past_shows_count': self.past_shows_count,
            'upcoming_shows_count': self.upcoming_shows_count
        }

    ## this method is inspired by Trivia_API_project
    ## define revisions for venue model:
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()   

    ## define upcoming shows and upcoming show counts
    @property
    def upcoming_shows(self):
        upcoming_shows = list(filter(lambda show: show.start_time > datetime.now(), self.shows))
        
        return [{'artist_name': show.artist.name,
                 'artist_id': show.artist.id,
                 'start_time': show.start_time.isoformat(),
                 'artist_image_link': show.artist.image_link
                } for show in upcoming_shows]
    
    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    ## define past shows and past show counts
    @property
    def past_shows(self):
        past_shows = list(filter(lambda show: show.start_time < datetime.now(), self.shows))
        
        return [{'artist_name': show.artist.name,
                 'artist_id': show.artist.id,
                 'start_time': show.start_time.isoformat(),
                 'artist_image_link': show.artist.image_link
                } for show in past_shows]

    @property
    def past_shows_count(self):
        return len(self.past_shows)
    

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    ## initialize artist model:
    def __init__(self, name, genres, city, state, phone, facebook_link,website,seeking_venue,seeking_description,image_link):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.phone = phone
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.image_link = image_link

    ## define show_template for artist model
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres.split(', '),
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': self.past_shows,
            'upcoming_shows': self.upcoming_shows,
            'past_shows_count': self.past_shows_count,
            'upcoming_shows_count': self.upcoming_shows_count
        }

    ## initiate __getitem__ method for easy access the venue object
    ## accessing items using square bracket notation ([]) on instances of a class
    def __getitem__(self, key):
        return getattr(self, key)


    ## initiate __repr__ method for define a string representation of an object
    def __repr__(self):
        return f'<Artist name={self.name}, city={self.city}, state={self.state}, genres={self.genres}, past_shows_count={self.past_shows_count}, upcoming_shows_count={self.upcoming_shows_count}>'    

    ## define revisions for artist model:
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    ## implement properties for artist model:
    @property
    def past_shows(self):
        past_shows = list(filter(lambda show: show.start_time < datetime.now(), self.shows))
        return [{'venue_id': show.venue.id,
                'venue_name': show.venue.name,
                'venue_image_link': show.venue.image_link,
                'start_time': show.start_time.isoformat()
            } for show in past_shows]

    @property
    def upcoming_shows(self):
        upcoming_shows = list(filter(lambda show: show.start_time > datetime.now(), self.shows))
        return [{'venue_id': show.venue.id,
                'venue_name': show.venue.name,
                'venue_image_link': show.venue.image_link,
                'start_time': show.start_time.isoformat()
            } for show in upcoming_shows]

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    venue = db.relationship('Venue', backref='shows', lazy=True)
    artist = db.relationship('Artist', backref='shows', lazy=True)
    
    ## initialize show model:
    def __init__(self, venue_id, artist_id, start_time):
      self.venue_id = venue_id
      self.artist_id = artist_id
      self.start_time = start_time

    ## initiate __getitem__ method for easy access the venue object
    ## accessing items using square bracket notation ([]) on instances of a class
    def __getitem__(self, key):
        return getattr(self, key)


    ## initiate __repr__ method for define a string representation of an object
    def __repr__(self):
      return f'<Show start_time={self.start_time}, venue={self.venue}, artist={self.artist}>'

    ## define revisions for show model:
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    ## define show_template for show model
    def format(self):
        return {
            'venue_id': self.venue.id,
            'venue_name': self.venue.name,
            'artist_id': self.artist.id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time.isoformat()
        }

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

## home page route
@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

## venue list page route
@app.route('/venues')
def venues():
    venues = Venue.query.all()

    sortby = lambda v: (v['city'], v['state'])
    sort_grouped_venues = itertools.groupby(sorted(venues, key=sortby), key=sortby)

    data = [
        {
            'city': city_state[0],
            'state': city_state[1],
            'venues': list(value)
        }
        for city_state, value in sort_grouped_venues]  
    
    return render_template('pages/venues.html', areas=data)


## venue search page route
@app.route('/venues/search', methods=['POST'])
def search_venues():

    ## get search term
    search_term = request.form.get('search_term', '')

    ## get search results
    venues_fromsearch = Venue.query.filter(Venue.name.match(f'%{search_term}%')).all()

    venues_response = [{'id': venue.id,
                        'name': venue.name,
                        'num_upcoming_shows': venue.upcoming_shows_count
                        }for venue in venues_fromsearch]
    response = {'data': list(venues_response), 'count': len(venues_fromsearch)}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

## venue details page route  
@app.route('/venues/<int:venue_id>')
def show_single_venue(venue_id):   
    venue = Venue.query.filter_by(id=venue_id).first()
    
    if not venue: return abort(404)
    data = venue.format()
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
#  ----------------------------------------------------------------

## create venue get blank form page route 
@app.route('/venues/create', methods=['GET'])
def get_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

## create venue submit form page route
@app.route('/venues/create', methods=['POST'])
def create_venue_submit():
    form = VenueForm(request.form)
   
    if not form.validate():
        print(form.errors) 
    else:
        try:
            venue_name = form.name.data
            ## check if venue exists
            exists = db.session.query(Venue.id).filter_by(name=venue_name).scalar() 

            if exists is not None:
                flash(f'Error: {venue_name} has been registered already!', 'danger')
            else:
                new_venue = Venue(name=venue_name,
                                  genres=', '.join(form.genres.data),
                                  city=form.city.data,
                                  state=form.state.data,
                                  address=form.address.data,
                                  phone=form.phone.data,
                                  image_link = form.image_link.data,
                                  facebook_link=form.facebook_link.data,
                                  website = form. website_link.data,
                                  seeking_talent = form.seeking_talent.data,
                                  seeking_description = form.seeking_description.data)
                new_venue.insert()

                ## if sucessful inserted, flash success message
                flash('Your venue is successfully added!', 'success')
                return redirect(url_for('show_single_venue', venue_id=new_venue.id))

        except:
            ## if error, print error and flash error message
            print(exc.SQLAlchemyError)
            flash('Error: This venue could not be added.', 'danger')

    return render_template('forms/new_venue.html', form=form)

## delete venue page route
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    
    ## check if the venue exists
    if not venue: return abort(404)

    try:
        venue.delete()
        ## if sucessful deleted, flash success message
        flash(f'{venue.name} has been deleted!', 'success')
        return redirect(url_for('index'))
    except:
        ## if error, print error and flash error message
        print(exc.SQLAlchemyError)
        flash(f'Error: {venue.name} cannot be deleted.', 'danger')

# BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
# clicking that button delete it from the db then redirect the user to the homepage

#  Update venues
#  ----------------------------------------------------------------
## edit venue get form page route
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def get_venue_toedit(venue_id):
    venue_toedit = Venue.query.filter_by(id=venue_id).first()
    
    if not venue_toedit: abort(404)

    venue = {
        'id': venue_toedit.id,
        'name': venue_toedit.name,
        'genres': venue_toedit.genres.split(', '),
        'address': venue_toedit.address,
        'city': venue_toedit.city,
        'state': venue_toedit.state,
        'phone': venue_toedit.phone,
        'website': venue_toedit.website,
        'facebook_link': venue_toedit.facebook_link,
        'seeking_talent': venue_toedit.seeking_talent,
        'seeking_description': venue_toedit.seeking_description,
        'image_link': venue_toedit.image_link
    }

    form = VenueForm(formdata=None, data=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)

## edit venue submit form page route
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def venue_edited_submit(venue_id):
    
    venue_edited = Venue.query.filter_by(id=venue_id).first()
    if not venue_edited: abort(404)

    form = VenueForm(request.form)

    if not form.validate():
        print(form.errors) 
    else:
        try:
            form.genres.data = ', '.join(form.genres.data)
            form.populate_obj(venue_edited)
            venue_edited.update()
            ## if sucessful deleted, flash success message
            flash('This venue has been updated!', 'success')
            return redirect(url_for('show_single_venue', venue_id=venue_id))
        except:
        ## if error, print error and flash error message
            print(exc.SQLAlchemyError)
            flash(f'Error: {venue_edited.name} cannot be edited.', 'danger')

    return render_template('forms/edit_venue.html', form=form, venue=venue_edited)

#  Artists
#  ----------------------------------------------------------------
## artist list page route
@app.route('/artists')
def artists():
    artists = Artist.query.order_by(Artist.name.asc()).all()
    data = [{'id': artist.id, 'name': artist.name} for artist in artists]

    return render_template('pages/artists.html', artists=data)

## artist search page route
@app.route('/artists/search', methods=['POST'])
def search_artists():
    ## get search term 
    search_term = request.form.get('search_term', '')

    ## filter out the search result
    artists_fromsearch = Artist.query.filter(Artist.name.match(f'%{search_term}%')).all()

    artist_response = [{'id': artist.id,
                        'name': artist.name,
                        'num_upcoming_shows': artist.upcoming_shows_count
                        }for artist in artists_fromsearch]
    response = {'data': list(artist_response),
                'count': len(artists_fromsearch)}

    return render_template('pages/search_artists.html', search_term=search_term, results=response)

## artist detail page route
@app.route('/artists/<int:artist_id>')
def show_single_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()

    if not artist: return abort(404)

    data = artist.format()
    return render_template('pages/show_artist.html', artist=data)

#  Update artist
#  ----------------------------------------------------------------
## edit artist get form page route
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist_toedit = Artist.query.filter_by(id=artist_id).first()

    if not artist_toedit: return abort(404)

    artist = {
        'id': artist_toedit.id,
        'name': artist_toedit.name,
        'genres': artist_toedit.genres.split(', '),
        'city': artist_toedit.city,
        'state': artist_toedit.state,
        'phone': artist_toedit.phone,
        'website': artist_toedit.website,
        'facebook_link': artist_toedit.facebook_link,
        'seeking_venue': artist_toedit.seeking_venue,
        'seeking_description': artist_toedit.seeking_description,
        'image_link': artist_toedit.image_link}

    form = ArtistForm(formdata=None, data=artist)

    return render_template('forms/edit_artist.html', artist=artist, form=form)

## edit artist submit form page route
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submit(artist_id):

    artist_edited = Artist.query.filter_by(id=artist_id).first()

    if not artist_edited: abort(404)

    form = ArtistForm(request.form)
    
    if not form.validate():
        print(form.errors) 
    else:
        try:
            form.genres.data = ', '.join(form.genres.data)
            form.populate_obj(artist_edited)
            artist_edited.update()
            ## if sucessful deleted, flash success message
            flash('This artist has been updated!', 'success')
            return redirect(url_for('show_single_artist', artist_id=artist_id))
        except:
        ## if error, print error and flash error message
            print(exc.SQLAlchemyError)
            flash(f'Error: {artist_edited.name} cannot be edited.', 'danger')

    return render_template('forms/edit_artist.html', artist=artist_edited, form=form)


#  Create Artist
#  ----------------------------------------------------------------

## create artist get blank form page route
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

## create artist submit form page route
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    
    ## check is the form is valid or not
    if not form.validate():
        print(form.errors) 
    else:
        try:
            artist_name = form.name.data
            exists = db.session.query(Artist.id).filter_by(name=artist_name).scalar() 

            if exists is not None:
                flash(f'Error: {artist_name} has been registered already!', 'danger')
            else:
                new_artist = Artist(
                    name=form.name.data,
                    genres=', '.join(form.genres.data),
                    city=form.city.data,
                    state=form.state.data,
                    phone=form.phone.data,
                    website = form. website_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_venue = form.seeking_venue.data,
                    seeking_description = form.seeking_description.data,
                    image_link = form.image_link.data
                )
                new_artist.insert()

                ## sucessful flash
                flash('The artist has been added', 'success')
                return redirect(url_for('show_single_artist', artist_id=new_artist.id))

        except:
            ## error flash
            print(exc.SQLAlchemyError)
            flash('Error: The artist could not be added.', 'danger')

    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------
## show list page route
@app.route('/shows')
def shows():
    shows = Show.query.order_by(Show.start_time.desc()).all()
    data = [show.format() for show in shows]

    return render_template('pages/shows.html', shows=data)

## create show get blank form page route
@app.route('/shows/create', methods=['GET'])
def create_shows():
    # renders form. do not touch. (--> nyah nyah!  I touched it!)
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

## create show submit form page route
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)

    if not form.validate():
        print(form.errors)
    else:
        try:
            artist_id = form.artist_id.data
            venue_id = form.venue_id.data
            start_time = form.start_time.data

            ## check if venue exist or not
            venue_exists = db.session.query(Venue.id).filter_by(id=venue_id).scalar() 
            ## check if artist exist or not
            artist_exists = db.session.query(Artist.id).filter_by(id=artist_id).scalar() 
            ## check if show exist or not
            exists = db.session.query(Show.id).filter(and_((Show.artist_id == artist_id) &
                                                                (Show.venue_id == venue_id) &
                                                                (Show.start_time == start_time))).scalar() 

            if not venue_exists:
                flash('Error: The venue has not been registered.', 'danger')

            elif not artist_exists:
                flash('Error: The artist has not been registered.', 'danger')

            elif exists is not None:
                flash('Error: The show has been registered already.', 'danger')
            
            else:
                new_show = Show(venue_id, artist_id, start_time)
                new_show.insert()
                flash('The show has been added', 'success')
                return redirect(url_for('shows'))

        except:
            print(exc.SQLAlchemyError)
            flash(f'Error: This show cannot be added.', 'danger')

    return render_template('forms/new_show.html', form=form)


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
