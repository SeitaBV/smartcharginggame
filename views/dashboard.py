from datetime import timedelta

from flask import request, session

from views import bvp_views
from views.utils import render_scc_template


# Dashboard and main landing page
@bvp_views.route('/')
@bvp_views.route('/dashboard')
def dashboard_view():
    """ Dashboard view.
    """

    variable = "hallo"
    turn = 1 # We start at turn 1
    transaction_costs = 5 # coins
    num_stations = 3
    num_turns = 7
    production = [1, 2, 3, 4, 3, 2, 1]
    consumption = [[0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 1, 1, 0, 0],
                   [0, 0, 0, 0, 1, 2, 0]]
    station_id = ["number_one", "number_two", "number_three"]
    max_capacity = [3, 1, 2]
    arrivals =   [[0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0]]
    departures = [[0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1]]
    target_consumption = [[0, 0, 0, 3, 0, 0, 0],
                          [0, 0, 0, 0, 5, 0, 0],
                          [0, 0, 0, 0, 0, 0, 1]]

    safe_js = "<script>"
    for i in range(num_stations):
        for j in range(num_turns):
            safe_js = safe_js + "$('#add_one_" + str(i) + "_" + str(j) + "').click(function() {" \
                                "$('#my_counter_" + str(i) + "_" + str(j) + "').html(function(i, val) { return +val+1 });" \
                                "$('#my_input_" + str(i) + "_" + str(j) + "').val(function(i, val) { return +val+1 });" \
                                "});" \
                                "$('#remove_one_" + str(i) + "_" + str(j) + "').click(function() {" \
                                "$('#my_counter_" + str(i) + "_" + str(j) + "').html(function(i, val) { return +val-1 });" \
                                "$('#my_input_" + str(i) + "_" + str(j) + "').val(function(i, val) { return +val-1 });" \
                     "});"
    safe_js = safe_js + "</script>"

    grid = [['solar', 'charging_station', 'charging_station', 'charging_station'],
            ['', '<!--<button>This is a button</button><button>This too</button>-->', '', '']]
    return render_scc_template('dashboard.html',
                               variable=variable,
                               grid=grid,
                               station_id=station_id,
                               safe_js=safe_js
                              )
