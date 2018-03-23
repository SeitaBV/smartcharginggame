"""
Get plots to explain fundamentals of the game structure.
"""
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from bokeh.plotting import figure, Figure
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import Range1d, ColumnDataSource, BoxAnnotation

from models import World
from attendance import prob_arrival


def make_supply_demand_figure(world: World, tools: List[str]) -> Figure:
    start_time = datetime(2018, 3, 9, 9)
    x_range = Range1d(start=start_time, end=start_time + timedelta(hours=7))

    fig = figure(title="Supply versus Demand",
                 x_range=x_range,
                 height=250,
                 min_border=0,
                 toolbar_location="right",
                 tools=tools,
                 h_symmetry=False, v_symmetry=False,
                 sizing_mode='scale_width',
                 outline_line_color="#666666")

    x = pd.date_range(start=x_range.start, end=x_range.end, freq="1H")

    generation_source = ColumnDataSource(dict(x=x, y=world.solar_park.generation.values))
    fig.line(x='x', y='y', source=generation_source, legend="Supply", alpha=0.5, color="green", line_width=4)

    demand_source = ColumnDataSource(dict(x=x, y=world.demand))
    fig.line(x='x', y='y', source=demand_source, legend="Demand", alpha=0.5, color="blue", line_width=4)

    fig.xaxis.axis_label = "Hours"

    return fig


def make_prices_figure(world: World, tools: List[str]) -> Figure:
    x_range = Range1d(1, 8)

    fig = figure(title="Market prices",
                 x_range=x_range,
                 height=250,
                 min_border=0,
                 toolbar_location="right",
                 tools=tools,
                 h_symmetry=False, v_symmetry=False,
                 sizing_mode='scale_width',
                 outline_line_color="#666666")

    prices_source = ColumnDataSource(dict(x=range(1, 9), y=world.market_prices))
    fig.line(x='x', y='y', source=prices_source, legend="Price", alpha=0.5, color="black", line_width=4)

    fig.xaxis.axis_label = "Available energy tokens"

    ba = BoxAnnotation(left=3.95, right=4.05,
                       fill_alpha=0.1, line_color="green", fill_color="green")
    fig.add_layout(ba)

    return fig


def make_arrival_prob_figure(probabilities: List[float], tools: List[str]) -> Figure:
    start_time = datetime(2018, 3, 9, 9)
    x_range = Range1d(start=start_time, end=start_time + timedelta(hours=7))

    fig = figure(title="Car arrival Probabilities",
                 x_range=x_range,
                 height=250,
                 min_border=0,
                 toolbar_location="right",
                 tools=tools,
                 h_symmetry=False, v_symmetry=False,
                 sizing_mode='scale_width',
                 outline_line_color="#666666")

    x = pd.date_range(start=x_range.start, end=x_range.end, freq="1H")
    arrival_prob_source = ColumnDataSource(dict(x=x, y=probabilities))
    fig.line(x='x', y='y', source=arrival_prob_source, legend="Probability of arrival",
             alpha=0.5, color="red", line_width=4)

    fig.xaxis.axis_label = "Hour"

    return fig


def build_game_data_plots(world: World):
    tools = ["box_zoom", "reset"]
    supply_demand_fig = make_supply_demand_figure(world, tools)
    prices_fig = make_prices_figure(world, tools)
    arrival_prob_fig = make_arrival_prob_figure(prob_arrival, tools)
    return components(gridplot([[supply_demand_fig, prices_fig, arrival_prob_fig]],
                               toolbar_options={'logo': None},
                               sizing_mode='scale_width'))

