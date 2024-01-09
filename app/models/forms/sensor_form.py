from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, IntegerField
from wtforms.validators import InputRequired, Length
from flask_babel import gettext

class SensorForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=3, max=80)], render_kw={"placeholder": gettext("Sensor name")})
    description = StringField(validators=[Length(max=80)], render_kw={"placeholder": gettext("About Sensor")})
    status = "On"
    location = {
        "latitude": 41.2,
        "longitude": 2.0
    }
    eui = StringField(validators=[Length(max=80)], render_kw={"placeholder": gettext("TTN ID")})
    hours_range = IntegerField()
    submit = SubmitField(gettext('Submit Sensor'))
