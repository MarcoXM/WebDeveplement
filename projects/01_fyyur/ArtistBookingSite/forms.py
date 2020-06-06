from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateField, DateTimeField
from wtforms.validators import DataRequired, ValidationError
import re

genres = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hard Rock', 'Hard Rock'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other')
]
state = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]


class ArtistForm(FlaskForm):
    def validate_phone(self, phone):
        us_phone_num1 = '^[0-9]{3}[-][0-9]{3}[ ][0-9]{4}$'
        us_phone_num2 = '^([0-9]{3})[-][0-9]{3}[-][0-9]{4}$'
        us_phone_num3 = '^[0-9]{10}$'
        us_phone_num4 = '^[0-9]{3}[-][0-9]{3}[-][0-9]{4}$'
        match = re.search(us_phone_num1, phone.data) or re.search(us_phone_num2, phone.data) or re.search(us_phone_num3, phone.data) or re.search(us_phone_num4, phone.data)
        if not match:
            raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', choices=state, validators=[DataRequired()])
    phone = StringField('phone', validators=[validate_phone])
    genres = SelectMultipleField('genres', validators=[DataRequired()], choices=genres)
    availability = StringField('availability')
    seeking_venue = SelectField('seeking_venue', choices=[(False, 'No'), (True, 'Yes')])
    seeking_description = StringField('seeking_description')
    facebook_link = StringField('facebook_link')
    image_link = StringField('image_link')
    website = StringField('website')


class VenueForm(FlaskForm):
    def validate_phone(self, phone):
        us_phone_num1 = '^[0-9]{3}[-][0-9]{3}[ ][0-9]{4}$'
        us_phone_num2 = '^([0-9]{3})[-][0-9]{3}[-][0-9]{4}$'
        us_phone_num3 = '^[0-9]{10}$'
        match = re.search(us_phone_num1, phone.data) or re.search(us_phone_num2, phone.data) or re.search(us_phone_num3, phone.data)
        if not match:
            raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')

    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    state = SelectField('state', choices=state, validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), validate_phone])
    genres = SelectMultipleField('genres', validators=[DataRequired()], choices=genres)
    seeking_talent = SelectField('seeking_talent', choices=[(False, 'No'), (True, 'Yes')])
    seeking_description = StringField('seeking_description')
    facebook_link = StringField('facebook_link')
    image_link = StringField('image_link')
    website = StringField('website')


class ShowForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    venues = SelectField('venue', choices=[], validators=[DataRequired()], coerce=int)
    artists = SelectField('artist', choices=[], validators=[DataRequired()], coerce=int)
    description = StringField('description')
    starttime = DateTimeField('starttime', validators=[DataRequired()])
    endtime = DateTimeField('endtime', validators=[DataRequired()])