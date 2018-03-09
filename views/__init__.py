"""This module hosts the views. This file registers blueprints and hosts some helpful functions"""

from flask import Blueprint


# We provide two blueprints under which views can be grouped. They are registered with the Flask app (see app.py)
bvp_views = Blueprint('a1_views', __name__,  static_folder='static', template_folder='templates')
bvp_error_views = Blueprint('a1_error_views', __name__)

# Now views can register
from views.dashboard import dashboard_view


