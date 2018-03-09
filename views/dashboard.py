from datetime import timedelta

from flask import request, session

from views import bvp_views
from views.utils import render_bvp_template


# Dashboard and main landing page
@bvp_views.route('/')
@bvp_views.route('/dashboard')
def dashboard_view():
    """ Dashboard view.
    """

    variable = "hallo"
    return render_bvp_template('dashboard.html', variable=variable)
