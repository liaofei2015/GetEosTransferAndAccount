from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.types import INTEGER
from eosapp import db
import time


class GameTb(db.Model):
    __tablename__ = 'game_tb'
    id = db.Column(INTEGER, primary_key=True, unique=True)
    game_id = db.Column(db.BigInteger(), unique=True)
    player = db.Column(db.String(50))
    referrer = db.Column(db.String(100))
    amount = db.Column(db.String(50))
    roll_guess = db.Column(INTEGER)
    roll_random_result = db.Column(INTEGER)
    payout = db.Column(db.String(50))
    seed = db.Column(db.String(100))
    created_at = db.Column(db.BigInteger())
    is_win = db.Column(db.Boolean)

    def __init__(self, game_id, player, referrer,amount,roll_guess,roll_random_result,payout,seed,created_at,is_win):
        self.game_id = game_id
        self.player = player
        self.referrer = referrer
        self.amount = amount
        self.roll_guess = roll_guess
        self.roll_random_result = roll_random_result
        self.payout = payout
        self.seed = seed
        self.created_at = created_at
        self.is_win = is_win

    def __repr__(self):
        return '{"player":"%s","payout":"%s","created_at":"%s"}' % (self.player, self.payout, self.created_at)


class RelTb(db.Model):
    __tablename__ = 'rel_tb'
    id = db.Column(INTEGER, primary_key=True, unique=True)
    game_id = db.Column(db.BigInteger())
    bet_amount = db.Column(db.String(50))
    reward = db.Column(db.String(50))
    level = db.Column(INTEGER)
    created_at = db.Column(db.BigInteger())
    recipient = db.Column(db.String(50))

    def __init__(self, game_id, bet_amount, reward, level, create_at, recipient):
        self.game_id = game_id
        self.bet_amount = bet_amount
        self.reward = reward
        self.level = level
        self.created_at = create_at
        self.recipient = recipient

    def __repr__(self):
        return '{"gameId":"%s","award":"%s","date":"%s","level":"%s","rollNum":"%s"}' % \
               (self.game_id, self.reward, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.created_at)),self.level,self.bet_amount)


class ConfTb(db.Model):
    __tablename__ = 'config_tb'
    id = db.Column(INTEGER, primary_key=True, unique=True)
    config_name = db.Column(db.String(50))
    value = db.Column(db.String(50))

    def __init__(self, config_name, value):
        self.config_name = config_name
        self.value = value

    def __repr__(self):
        return '{"config_name":"%s","value":"%s",}' % (self.config_name, self.value)


class CreateAccount(db.Model):
    __tablename__ = "create_account"
    id = db.Column(INTEGER, primary_key=True, unique=True)
    account = db.Column(db.String(50))
    creator = db.Column(db.String(50))
    owner_key = db.Column(db.String(256))
    active_key = db.Column(db.String(256))
    create_time = db.Column(db.String(50))

    def __init__(self, creator, account, owner_key, active_key, create_time):
        self.creator = creator
        self.account = account
        self.owner_key = owner_key
        self.active_key = active_key
        self.create_time = create_time


class Transfer(db.Model):
    __tablename__ = "transfer"
    id = db.Column(INTEGER, primary_key=True, unique=True)
    from_ = db.Column(db.String(50))
    to_ = db.Column(db.String(50))
    value = db.Column(db.String(50))
    memo = db.Column(db.String(256))
    create_time = db.Column(db.String(50))

    def __init__(self, from_, to_, value, memo, create_time):
        self.from_ = from_
        self.to_ = to_
        self.value = value
        self.memo = memo
        self.create_time = create_time