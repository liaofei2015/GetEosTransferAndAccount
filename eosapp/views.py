from eosapp import app, scheduler, db
from flask import request, make_response
from sqlalchemy import func
from eosapp.Models import GameTb, RelTb
import requests
import EosTask
import time
from GetEosInfo import exe_insert
import gevent
from eosapp import scalping
from datetime import datetime, timedelta


import json


@app.route('/api/get_winners', methods=['GET'])
def get_winners():
    wins = db.session.query(func.sum(GameTb.payout).label('acount'),GameTb.player).filter(GameTb.is_win == 1).group_by(GameTb.player).order_by(db.desc('acount')).all()
    result = make_response(json.dumps({"code": 1, "message": "success", "result": EosTask.win_to_json(wins)}, ensure_ascii=False))
    result.headers["Access-Control-Allow-Origin"] = '*'
    return result


@app.route('/api/get_my_reward', methods=['GET'])
def get_reward():
    player = request.args.get('player')
    reward = RelTb.query.filter(RelTb.recipient == player).all()
    result = make_response(json.dumps({"code": 1, "message": "success", "result": EosTask.to_json(reward)}, ensure_ascii=False))
    result.headers["Access-Control-Allow-Origin"] = '*'
    return result


@app.route('/api/insert_game', methods=['GET'])
def insert_info():
    EosTask.get_actions()
    return "insert success"


@app.route('/api/check_attack', methods=['GET'])
def check_info():
    result = EosTask.check_attack()
    return "%s check success!" %(result)


def check_attack():
    result = requests.get("http://127.0.0.1:5000/api/check_attack")
    time.sleep(2)
    print result.text


def insert_game():
    result = requests.get("http://127.0.0.1:5000/api/insert_game")
    print(result.text)


@app.route('/addjob', methods=['POST', 'GET'])
def index1():
    #scheduler.add_job(func=insert_game, id='1', args=None, trigger='interval', seconds=2, replace_existing=True)
    scheduler.add_job(func=check_attack, id='2', args=(), trigger='interval', seconds=2, replace_existing=True)
    return 'Hello Flask'


@app.route('/api/get_eos_info', methods=['GET'])
def get_eos():
    exe_insert()
    return True


@app.route('/api/stop_get_eos', methods=['GET'])
def stop_get_eos():
    scheduler.pause_job('3')
    return 'True'


@app.route('/api/resume_get_eos', methods=['GET'])
def resume_get_eos():
    scheduler.resume_job('3')
    return "True"


def insert_eos():
    result = requests.get("http://127.0.0.1:5000/api/insert_game")
    print(result.text)


@app.route('/add_get_eos', methods=['GET'])
def add_get_eos():
    scheduler.add_job(func=insert_eos, id='3', args=(), trigger='interval', seconds=30, replace_existing=True)
    return 'exe get eos info'


@app.route('/add_scalping',methods=["GET"])
def add_scalping():
    scheduler.add_job(func=scalping.push_action, id='scalping', next_run_time=datetime.now() + timedelta(seconds=12), args=[])
    return 'start scalping'