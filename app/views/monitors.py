from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import current_user
from flask_babel import gettext

from ..extensions import db, login_required, admin_required

app = Blueprint('monitors', __name__)

@app.route('/monitoring')
@login_required
def monitoring():
    # Get the time range from the query string, default to 24 hours
    data = Monitor.get_monitor_data(time_range=request.args.get('time_range', '24h'))

    return render_template('pages/monitoring.html.j2',
                           title=gettext("Monitoring"),
                           current_user=current_user,
                           navbar_highlight_monitoring=True,
                           monitors=data)

@app.route('/monitoring/raw')
@login_required
def monitoring_raw():
    data = Monitor.get_monitor_data(time_range=request.args.get('time_range', '24h'))

    return jsonify(data)
