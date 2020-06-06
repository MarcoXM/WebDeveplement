#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import logging
import json
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
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
## Sub table to match the many to many sotuation
## subtable should initilize first 
venue_genre = db.Table('venue_genre',
                       db.Column('venue_id', db.Integer, db.ForeignKey(
                           'venue.id'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey(
                           'genre.id'), primary_key=True)
                       )
artist_genre = db.Table('artist_genre',
                        db.Column('artist_id', db.Integer, db.ForeignKey(
                            'artist.id'), primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey(
                            'genre.id'), primary_key=True)
                        )


class Venue(db.Model):

    ## Venue table in the sql
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String)

    ### did the show has been booked 
    # shows_booked = db.relationship('show', cascade='all, delete-orphan', backref='venueShow', lazy=True)
    # ### genres and venne is many to many 
    # genres = db.relationship('genre', secondary=venue_genre, backref=db.backref('venueGenres', lazy=True))
    createddatetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    shows = db.relationship('show', cascade="save-update, merge, delete")

    def __repr__(self):
        return '<Venue {} {} >'.format(self.id,self.name)

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    ## Looking for a place 
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String)

    ## relationship with the show table 
    # shows_booked = db.relationship("show",cascade='all, delete-orphan', backref = 'artistShow', lazy =True)
    # genres = db.relationship('genre', secondary=artist_genre, backref=db.backref('artistGenres', lazy=True))
    createddatetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    shows = db.relationship('show', cascade="save-update, merge, delete")

    def __repr__(self):
        return '<Artist {} {} >'.format(self.id,self.name)



class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(30))

    def __repr__(self):
        return "<Genre {} {}>".format(self.id,self.genre)


class Show(db.Model):
    __tablename__ = "show"
    # "Show is a fact tabe "
    
    id = db.Column(db.Integer, primary_key=True)

    starttime = db.Column(db.DateTime, nullable=False)
    endtime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)

    # name = db.Column(db.String) # name is the artist + venue + time,
    artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'),nullable=False)
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.id'),nullable=False)
    show_time = db.Column(db.DateTime, nullable=False)

    createddatetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return '<Show {} {} {}>'.format(self.id,self.show_time,self.artist_id)
###
# Totally we have 4 tables
###


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

### Translate the time into datetime    
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


def todate(str):
    return datetime.strptime(str, '%Y-%m-%d').date()


def gettime(str):
    return datetime.strptime(str, '%Y-%m-%d %H:%M:%S')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    ### get_artist
    ### get_venue 
    return render_template('pages/home.html')


def get_artist_venue(list_id):
    artist = Artist.query.all()
    venue = Venue.query.get(id)
    show = Show.query.filter_by(list_id=list_id).order_by('id').all()

    return render_template('pages/home.html', artist=artist, venue=venue, show=show)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    error = False
    try:
        body = []
        venue = Venue.query.order_by(Venue.city, Venue.state).all()
        for v in venue:
            if len(body) == 0 or (body[-1]['city'] != v.city) or (
                    body[-1]['city'] == v.city and body[-1]['state'] != v.state):
                data = {
                    "city": v.city,
                    "state": v.state,
                    "venues": [{
                        "id": v.id,
                        "name": v.name,
                        "num_upcoming_shows": Show.query.filter_by(venue_id=v.id).count()
                    }]
                }
                body.append(data)
            else:
                body[-1]['venues'].append({
                    "id": v.id,
                    "name": v.name,
                    "num_upcoming_shows": Show.query.filter_by(venue_id=v.id).count()
                })
    except:
        error = False
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return render_template('pages/venues.html', areas=body)
    else:
        return render_template('errors/500.html')

@app.route('/venues/search', methods=['POST'])
def search_venues():
    error = False
    try:
        resp = ('%' + request.form['search_term'] + '%')
        venue_ = Venue.query.filter(Venue.name.ilike("%" + resp))
        venues_ = venue_.all()
        response = {
            "count": venue_.count(),
            "data": [{
                "id": v.id,
                "name": v.name,
                "num_upcoming_shows": (
                    Show.query.join(Venue, Venue.id == Show.venue_id).filter(Venue.id == v.id).filter(
                        Show.starttime > datetime.now()).count()),
            } for v in venues_]
        }
    except:
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        return render_template('pages/search_venues.html', results=response,
                               search_term=request.form.get('search_term', ''))
    else:
        return render_template('errors/500.html')

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):    
    error = False
    try:
        venue = Venue.query.get(venue_id)
        past_shows = list(filter(lambda x: x.starttime < datetime.today(), venue.shows))
        upcoming_shows = list(filter(lambda x: x.starttime >= datetime.today(), venue.shows))
        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres.split(", "),
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": ('+1 ' + venue.phone if len(venue.phone) > 10 else None),
            "website": '' if venue.website == 'NULL' else venue.website,
            "facebook_link": '' if venue.facebook_link == 'NULL' else venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": '' if venue.seeking_description == 'NULL' else venue.seeking_description,
            "image_link": '' if venue.image_link == 'NULL' else venue.image_link,

            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return render_template('pages/show_venue.html', venue=data)
    else:
        return render_template('errors/500.html')

    data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
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
    try:
        form = VenueForm()
        form.validate_on_submit()
        if 'phone' in form.errors:
            flash(form.errors['phone'][0])
            return create_venue_form()
        data = request.form
        venue = Venue(name=data['name'], city=data['city'], state=data['state'],
                      address=data['address'], phone=data['phone'],
                      genres=', '.join(data.getlist('genres')),
                      image_link='' if data['image_link'] == 'NULL' else data['image_link'],
                      facebook_link='' if data['facebook_link'] == 'NULL' else data['facebook_link'],
                      website='' if data['website'] == 'NULL' else data['website'],
                      seeking_talent=data['seeking_talent'] == 'Yes',
                      seeking_description='' if data['seeking_description'] == 'NULL' else data[
                          'seeking_description'])
        db.session.add(venue)
        db.session.commit()

    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
        
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        # on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')
    else:
        return render_template('errors/404.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        Venue.query.filter_by(id = venue_id).delete()
        Show.query.filter_by(venue_id = venue_id).delete()
        db.session.commit()
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        return jsonify({
            'success': True
        })
    else:
        return render_template('errors/500.html')
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    error = False
    try:
        artists = Artist.query.all()
        data = []
        for a in artists:
            data.append({
                'id': a.id,
                "name": a.name
            })
    except:
        error = True
        print(sys.exc_info())
    finally:
        db.session.rollback()
    
    if not error:
        return render_template('pages/artists.html', artists=data)

    else:
        return render_template('errors/500.html')

@app.route('/artists/search', methods=['POST'])
def search_artists():
    '''
    output data type
            "count": 1,
            "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
            }]
        }
        '''
    error = False
    try:
        artists_ = Artist.query.filter(Artist.name.ilike(('%' + request.form['search_term'] + '%'))).all()
        response={
            "count": len(artists_),
            "data": []
        }
        for a in artists_:
            response['data'].append({
            "id": a.id,
            "name": a.name,
            "num_upcoming_shows": Show.query.join(Artist, Artist.id == Show.artist_id).filter(Artist.id == a.id).filter(
                            Show.starttime > datetime.now()).count(),
            })
    except:
        error = True
        print(sys.exc_info())
    finally:
        db.session.commit()
    
    if not error:
        return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
    else:
        return render_template('errors/500.html')
    

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    
    error = False
    try:
        artist_ = Artist.query.get(id = artist_id)
        show_ = Show.query.with_entities(Venue.id.label('id') ,Venue.name.label('venue'),
                                        Venue.image_link.label('image_link'), Show.starttime.label('starttime')).join(
                                        Venue, Venue.id == Show.venue_id).filter(Show.artist_id == artist_id)
        past_show = list(filter(lambda x: x.starttime < datetime.today(), show_))
        upcoming_shows = list(filter(lambda x: x.starttime >= datetime.today(), show_))
        data = {
            "id": artist_id,
            "name": artists_.name,
            "genres": artists_.genres.split(", "),
            "city": artists_.city,
            "state": artists_.state,
            "phone": None if not artists_.phone else '+1 '+ artists_.phone,
            "website": '' if artists_.website == 'NULL' else artists_.website,
            "facebook_link": ' ' if artists_.facebook_link == 'NULL' else artists_.facebook_link,
            "seeking_venue": artists_.seeking_venue,
            "seeking_description": None if artists_.seeking_description is None else artists_.seeking_description,
            "availability": '' if artists_.availability is '' or artists_.availability is None else [
                d if datetime.strptime(d, '%Y-%m-%d').date() > datetime.now().date() else None
                for d in artists_.availability.split(',')],
            "image_link": '' if artists_.image_link == 'NULL' else artists_.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    except:
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return render_template('pages/show_artist.html', artist=data)
    else:
        return render_template('errors/500.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    ### get the row you need to modify 
    error = False
    try:
        artist = Artist.query.filter_by(id=artist_id).all()[0]
        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.genres.data = artist.genres.split(", ")
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
        form.availability.data = '' if artist.availability is None else artist.availability
        form.facebook_link.data = '' if artist.facebook_link == 'NULL' else artist.facebook_link
        form.image_link.data = '' if artist.image_link == 'NULL' else artist.image_link
        form.website.data = '' if artist.website == 'NULL' else artist.website
        db.session.commit()
    except:
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return render_template('forms/edit_artist.html', form=form, artist=artist)
    else:
        return render_template('errors/500.html')


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    try :
        form = ArtistForm()
        form.validate_on_submit()
        if 'phone' in form.errors:
            flash(form.errors['phone'][0])
            return edit_artist(artist_id)
        artist = Artist.query.filter_by(id=artist_id).all()[0]
        data = request.form
        artist.name = data['name']
        artist.city = data['city']
        artist.state = data['state']
        artist.phone = data['phone']
        artist.genres = ', '.join(data.getlist('genres'))
        artist.seeking_venue = data['seeking_venue'] == 'Yes'
        artist.seeking_description = '' if data['seeking_description'] == 'NULL' else data['seeking_description']
        artist.availability = '' if data['availability'] == 'NULL' else data['availability']
        artist.facebook_link = '' if data['facebook_link'] == 'NULL' else data['facebook_link']
        artist.website = '' if data['website'] == 'NULL' else data['website']
        artist.image_link = '' if data['image_link'] == 'NULL' else data['image_link']
        db.session.add(artist)
        db.session.commit()

    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        return render_template('errors/500.html')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    '''
    venue={
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    ## get the data and svae it on SQL
    '''
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id).all()[0]
        form = VenueForm()
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.phone.data = venue.phone
        form.genres.data = venue.genres.split(", ")
        form.seeking_talent.data = venue.seeking_venue
        form.seeking_description.data = venue.seeking_description
        form.facebook_link.data = '' if venue.facebook_link == 'NULL' else venue.facebook_link
        form.image_link.data = '' if artvenueist.image_link == 'NULL' else venue.image_link
        form.website.data = '' if venue.website == 'NULL' else venue.website
        db.session.commit()
    except:
        error =True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    else:
        return render_template('errors/500.html')


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    try:
        
        form = VenueForm()
        form.validate_on_submit()
        if 'phone' in form.errors:
            flash(form.errors['phone'][0])
            return edit_venue(venue_id)
        data = request.form
        venue = Venue.query.get(id = venue_id)
        venue.name = data['name']
        venue.city = data['city']
        venue.state = data['state']
        venue.address = data['address']
        venue.phone = data['phone']
        venue.genres = ', '.join(data.getlist('genres'))
        venue.seeking_description = '' if data['seeking_description'] == 'NULL' else data['seeking_description']
        venue.seeking_talent = data['seeking_talent'] == 'Yes'
        venue.facebook_link = '' if data['facebook_link'] == 'NULL' else data['facebook_link']
        venue.image_link = '' if data['image_link'] == 'NULL' else data['image_link']
        venue.website = '' if data['website'] == 'NULL' else data['website']
        db.session.commit()
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    
    finally:
        db.session.close
    
    if not error:
        return redirect(url_for('show_venue', venue_id=venue_id))
    else:
        return render_template('errors/500.html')

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    # Renders a Artist form to add a new artist into db
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    
    error = False
    try:
        form = ArtistForm()
        form.validate_on_submit()
        if 'phone' in form.errors:
            flash(form.errors['phone'][0])
        data = request.form
        artist = Artist(name=data['name'], city=data['city'], state=data['state'],
                        phone=data['phone'], genres=', '.join(data.getlist('genres')),
                        availability=data['availability'],
                        image_link='' if data['image_link'] == 'NULL' else data['image_link'],
                        facebook_link='' if data['facebook_link'] == 'NULL' else data['facebook_link'],
                        website='' if data['website'] == 'NULL' else data['website'],
                        seeking_venue=data['seeking_venue'] == 'Yes',
                        seeking_description=data['seeking_description'])

        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
     
    else:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        return render_template('errors/500.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
    error = False
    try:
        shows_ = Show.query.with_entities(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link,
                                        Show.starttime, Show.endtime).join(Artist, Artist.id == Show.artist_id).join(
            Venue,
            Venue.id == Show.venue_id).order_by(
            Show.starttime).all()

        data = []
        for s in show_:
            data.append({
                "venue_id": s[0],
                "venue_name": s[1],
                "artist_id": s[2],
                "artist_name": s[3],
                "artist_image_link": s[4],
                "start_time": str(s[5]),
                "endtime": str(s[6])
            })
    except:
        error = True
        print(sys.exc_info())

    finally:
        db.session.close()

    if not error:
        return render_template('pages/shows.html', shows=data)

    else:
        return render_template('errors/500.html') 

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
    form = ShowForm()
    artists_ = Artist.query.order_by(Artist.id).all()
    venues_ = Venue.query.order_by(Venue.id).all()
    artistid = request.args.get('artistid', 1, int)
    start_date = request.args.get('start_date', datetime.now(), todate)
    form.artists.choices = [(a.id, a.name) for a in artists_]
    form.venues.choices = [(v.id, v.name) for v in venues_]
    form.artists.data = artistid
    form.starttime.data = start_date
    form.endtime.data = start_date
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        data = request.form

        ## getting shows info and check for 
        shows = Show.query.filter(Show.artist_id == data['artists'], Show.venue_id == data['venues'])
        ## check data 
        for s in shows:
            t1 = s.starttime
            t2 = gettime(data['starttime'])
            t3 = gettime(data['endtime'])
            t4 = s.endtime
            if t1 <= t2 <= t4:
                flash('Start time overlaps with another show')
                return create_shows()
            elif t1 <= t3 <= t4:
                flash('End time overlaps with another show')
                return create_shows()

        ## get the artist info 
        artists_ = Artist.query.filter(Artist.id == data['artists']).one_or_none()
        ar = artists_.availability.split(", ")
        dt = data['starttime'][:10]
        ## check artist 
        if dt in ar: # if artist have update artist status
            ar.remove(dt)
            artists_.availability = ', '.join(ar)
            db.session.add(artists_)

        ## new show instance 
        show = Show(name=data['name'], artist_id=data['artists'], venue_id=data['venues'],
                    description=data['description'], starttime=data['starttime'], endtime=data['endtime'])
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        print(sys.exc_info())

    finally:
        db.session.close()

    if not error:
        flash('Show was successfully listed!')
        return render_template('pages/home.html')

    else:
        flash('An error occurred. Show could not be listed.')
        return render_template('errors/500.html')
  

@app.errorhandler(400)
def bad_request(error):
    flash('Error 400: Bad Request')
    return render_template('pages/home.html'), 400


@app.errorhandler(401)
def unauthorized(error):
    flash('Error 401: Unauthorized')
    return render_template('pages/home.html'), 401


@app.errorhandler(403)
def forbidden(error):
    flash('Error 403: Access Forbidden')
    return render_template('pages/home.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(405)
def invalid_method(error):
    flash('Error 405: Inavlid Method')
    return render_template('pages/home.html'), 405


@app.errorhandler(409)
def duplicte_resource(error):
    flash('Error 409: Duplicate Resource')
    return render_template('pages/home.html'), 409


@app.errorhandler(422)
def unprocessable(error):
    flash('Error 422: Unprocessable request')
    return render_template('pages/home.html'), 422


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

# {% ... %} for Statements

# {{ ... }} for Expressions to print to the template output

# {# ... #} for Comments not included in the template output

# #  ... ## for Line Statements