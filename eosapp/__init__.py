# -*- coding: utf-8 -*-
from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
#from eosapp.Models import db
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#job_defaults = {'max_instances': 10}
scheduler = APScheduler(scheduler=BackgroundScheduler({'max_instances': 30}))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + './test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
scheduler.init_app(app=app)
scheduler.start()

db = SQLAlchemy(app)
with app.app_context():
    from Models import GameTb, RelTb
    db.create_all()
app.app_context().push()