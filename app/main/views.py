from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..sendemail import send_email
from . import main
from .forms import NameForm
from datetime import datetime


@main.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())
