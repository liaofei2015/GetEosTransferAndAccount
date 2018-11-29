# -*- coding: utf-8 -*-
from eosapp.Models import CreateAccount, Transfer, ConfTb
from eosapp import db
import json, subprocess
from subprocess import PIPE

cmd = "cleos -u cleos -u http://eos.greymass.com get block "


def get_account(json_info, create_time):
    add_account = CreateAccount(json_info['data']['creator'], json_info['data']['name'], json_info['data']['owner']['keys'][0]['key'],
                                json_info['data']['active']['keys'][0]['key'], create_time)
    db.session.add(add_account)
    db.session.commit()


def get_transfer(json_info, create_time):
    add_transfer = Transfer(json_info['data']['from'], json_info['data']['to'],json_info['data']['quantity'],
                            json_info['data']['memo'], create_time)
    db.session.add(add_transfer)
    db.session.commit()


def insert_info(block_json):
    for x in block_json['transactions']:
        create_time = x['trx']['transaction']['expiration'].replace('T', ' ')
        y = (x['trx']['transaction']['actions'])
        for i in y:
            if (i['name']) == "newaccount":
                get_account(i, create_time)
            if (i['name']) == "transfer":
                get_transfer(i, create_time)


def get_block_num():
    q = ConfTb.query.filter(ConfTb.config_name == 'block_num').first()
    return q.value


def update_block_num(num):
    q = ConfTb.query.filter(ConfTb.config_name == 'block_num').first()
    q.value = num
    db.session.commit()


def exe_insert():
    command = cmd + "%s" % get_block_num()
    print(command)
    update_block_num(str(long(get_block_num()) + 1))
    actions_output = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    transactions = json.loads(actions_output.stdout.read())
    if len(transactions['transactions']) !=0:
        insert_info(transactions)
