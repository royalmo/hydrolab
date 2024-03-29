from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, IntegerField
from wtforms.validators import InputRequired, Length
from flask_babel import lazy_gettext as gettext

class SensorForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=3, max=80)], render_kw={"placeholder": gettext("Sensor name")})
    description = StringField(validators=[Length(max=80)], render_kw={"placeholder": gettext("About Sensor")})
    eui = StringField(validators=[Length(max=80)], render_kw={"placeholder": gettext("TTN ID")})

    time_between_waterings = IntegerField(render_kw={"placeholder": gettext("Time Between Waterings")})
    watering_time = IntegerField(render_kw={"placeholder": gettext("Watering Time")})
    watering_threshold = IntegerField(render_kw={"placeholder": gettext("Watering Threshold")})
    minutes_between_uplinks = IntegerField(render_kw={"placeholder": gettext("Minutes between uplinks")})

    hours_range = IntegerField()
    submit = SubmitField(gettext('Submit Sensor'))
