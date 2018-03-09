"""Utilities for views"""
import os
import datetime
from typing import List

from flask import render_template, request, session


def render_bvp_template(html_filename: str, **variables):
    """Render template and add all expected template variables, plus the ones given as **variables."""
    variables["test"] = "hey there"

    return render_template(html_filename, **variables)
