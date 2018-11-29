import json, subprocess, time
from subprocess import PIPE
import logging
from eosapp.Models import GameTb, RelTb, ConfTb
from eosapp import db
import gevent


logging.basicConfig()
cmd = "cleos -u http://eos.greymass.com get actions gggggamedive "
stop_eos = "cleos push action ddddgamedive switching '[1]' -p gggamerecord"
unlock = "cleos wallet unlock --password 'PW5HrU4V9SXnwhF6555555555555555555555pEFz'"


def get_action_seq():
    q = ConfTb.query.filter(ConfTb.config_name == 'action_seq').first()
    return q.value


def update_action_seq(num):
    q = ConfTb.query.filter(ConfTb.config_name == 'action_seq').first()
    q.value = num
    db.session.commit()


def to_json(listobj):
    list_dic = []
    for x in listobj:
        list_dic.append(json.loads(str(x)))
    return list_dic


def win_to_json(listobj):
    lis_dic = []
    for index, x in enumerate(listobj):
        lis_dic.append({"number":index+1, "player": x[1], "amount":str(float('%.4f' % x[0]))+' EOS'})
    return lis_dic


def eos_seq(obj_json):
    return obj_json['account_action_seq']


def get_actions():
    value = get_action_seq()
    command = cmd+"%s 30 -j" % value
    actions_output = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    actions_info = json.loads(actions_output.stdout.read())
    actions_list = actions_info['actions']
    if len(actions_list) == 0:
        return
    exe_insert = []
    for act in actions_list:
        gevent.joinall(exe_insert.append(gevent.spawn(insert_action, act)))
    update_action_seq(str(eos_seq(actions_list[-1])))


def insert_action(dict_act):
    act_trace = dict_act['action_trace']['act']['data']
    if act_trace.has_key('result'):
        if GameTb.query.filter(GameTb.game_id == act_trace['result']['game_id']).first() is None:
            game_id = act_trace['result']['game_id']
            player = act_trace['result']['player']
            referrer = act_trace['result']['referrer']
            amount = act_trace['result']['amount']
            roll_guess = act_trace['result']['roll_guess']
            roll_random_result = act_trace['result']['roll_random_result']
            payout = act_trace['result']['payout']
            seed = act_trace['result']['seed']
            created_at = act_trace['result']['created_at']
            win = is_win(roll_guess, roll_random_result)
            game = GameTb(game_id, player, referrer, amount, roll_guess, roll_random_result, payout, seed, str(created_at),win)
            db.session.add(game)
            db.session.commit()
    if act_trace.has_key('referrer_log'):
            game_id = act_trace['referrer_log']['game_id']
            bet_amount = act_trace['referrer_log']['game_amount']
            reward = act_trace['referrer_log']['reward']
            level = act_trace['referrer_log']['level']
            #created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(act_trace['referrer_log']['created_at']))
            created_at = act_trace['referrer_log']['created_at']
            recipient = act_trace['referrer_log']['recipient']
            if RelTb.query.filter(RelTb.game_id == game_id and RelTb.recipient == recipient).first() is None:
                rel = RelTb(game_id, bet_amount, reward, level, created_at, recipient)
                db.session.add(rel)
                db.session.commit()


def is_win(roll_guess, roll_random_result):
    is_guess_under = roll_guess == 1
    if is_guess_under and roll_random_result < 4 or (not is_guess_under and roll_random_result > 3):
        return True
    else:
        return False


def check_attack():
    q = GameTb.query.order_by(GameTb.game_id.desc()).limit(10).all()
    list_info = to_json(q)
    if len(list_info) < 10:
        return False
    for x in list_info:
        if x['payout'] == "0.0000 EOS":
            return False
    subprocess.Popen(unlock, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output = subprocess.Popen(stop_eos, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    return output.stdout.read()
