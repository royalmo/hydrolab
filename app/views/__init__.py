from flask import Blueprint, render_template, url_for, redirect, request, make_response, send_from_directory
from flask_login import current_user
from ..extensions import login_required
from flask_babel import gettext

from .users import app as users_view
from .servers import app as servers_view
from .monitors import app as monitors_view
from .api import app as api_view
from ..models import Server, SearchForm

app = Blueprint('main', __name__)
app.register_blueprint(users_view, url_prefix='')
app.register_blueprint(servers_view, url_prefix='')
app.register_blueprint(monitors_view, url_prefix='')

@app.route('/')
def index():
    return redirect(url_for('.map'))

@app.route('/map', methods=['GET'])
@login_required
def map():
    return render_template('pages/map.html.j2')
    

@app.route('/serviceworker.js')
def service_worker():
    response = make_response(send_from_directory('static/js/','serviceworker.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response
