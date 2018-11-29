from eosapp.Models import GameTb, RelTb, ConfTb,CreateAccount
from sqlalchemy import func
import json
import os
from eosapp import EosTask
from eosapp import db
from datetime import datetime
import time
t= "dasdfas"
cmd = "cleos -u http://junglehistory.cryptolions.io:18888 transfer %s eoswallet415 \"0.1 EOS\" \"2-sugarsugarbb\""

command = cmd % (t)

print(command)
def to_json(listobj):
    list_dic = []
    for x in listobj:
        list_dic.append(json.loads(str(x)))
    return list_dic


def check():
    q = GameTb.query.order_by(GameTb.game_id.desc()).limit(10).all()#.subquery()
    list_info =to_json(q)
    for x in list_info:
        if x['payout'] != "0.0000 EOS":
            return False
    return True

"""out = open('./3.txt')
print(out)
s = json.loads(out.read())
print(s)
for x in s['transactions']:
    create_time = x['trx']['transaction']['expiration'].replace('T', ' ')
    y = (x['trx']['transaction']['actions'])
    print(len(y))
    for i in y:
        if (i['name']) == "newaccount":
            print(create_time, i['data']['creator'], i['data']['name'], i['data']['owner']['keys'][0]['key'],
                  i['data']['active']['keys'][0]['key'])
            add_account = CreateAccount(i['data']['creator'],i['data']['name'],i['data']['owner']['keys'][0]['key'],i['data']['active']['keys'][0]['key'], create_time)
            db.session.add(add_account)
            db.session.commit()
        if (i['name']) == "transfer":
            print(i['data']['from'],i['data']['to'],i['data']['quantity'],i['data']['memo'])"""
q = GameTb.query.group_by(GameTb.player).limit(10).all()
list_info = to_json(q)
print(list_info)
#print(EosTask.get_action_seq())
#EosTask.update_action_seq('76030')
#test = GameTb.query(GameTb.player,GameTb.created_at,func.sum(GameTb.payout).label('acount')).filter(GameTb.is_win == 1)
#test1 = db.session.query(func.sum(GameTb.payout).label('acount'),GameTb.player).filter(GameTb.is_win == 1).group_by(GameTb.player).order_by(db.desc('acount')).all()
#print(test1)
"""a = 1538210756
b = time.localtime(a)
c=datetime.utcfromtimestamp(a)
print(c)
a = 11107
print(GameTb.query.filter(GameTb.game_id == a).first())
if GameTb.query.filter(GameTb.game_id == a).first() is None:
    game = GameTb(a,'languopeng1113','fairgamedive','0.1000 EOS',1,2,'0.1960 EOS','21ebfa04e021fa09b149403bb44951ec60c6a26a5830b2dcbf714efd02a39e46', 1538210756,1)
    db.session.add(game)
    db.session.commit()"""
#test1 = GameTb.query.filter(GameTb.is_win == 1).limit(5).all()
#print(test1)
#select sum(payout)as acount,player,created_at from game_tb group by player order by acount;