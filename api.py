#!/usr/bin/env python

import json
import sqlite3
from bottle import route, run

conn = sqlite3.connect('adej.sqlite3')
cur = conn.cursor()


def table_to_json(clm, tab):
  len_clm = len(clm)

  if type(tab) == tuple:
    param = dict()
    for i in range(0, len_clm):
      param[clm[i]] = tab[i]
  elif type(tab) == list:
    param = list()
    for r in tab:
      p = dict()
      for i in range(0, len_clm):
        p[clm[i]] = r[i]
      param.append(p)

  return json.dumps(param, ensure_ascii=False)


@route('/')
def index():
  return 'root'


@route('/demo/:case_id')
def demo(case_id):
  clm = ('case_id', 'freq', 'sex', 'age', 'weight', 'height', 'quarter', 'status', 'report', 'reporter')
  cur.execute('SELECT ' + ', '.join(clm) + ' FROM demo WHERE case_id == ?;', (str(case_id),))
  return table_to_json(clm, cur.fetchone())


@route('/drug/:case_id')
def drug(case_id):
  clm = ('case_id', 'freq', 'sn', 'association', 'name', 'brand', 'route', 'start_date', 'end_date', 'dosage', 'unit', 'fraction', 'reason', 'fix', 'relapse')
  cur.execute('SELECT * FROM drug WHERE case_id == ?;', (str(case_id),))
  return table_to_json(clm, cur.fetchall())


@route('/hist/:case_id')
def reac(case_id):
  clm = ('case_id', 'freq', 'sn', 'event', 'outcome', 'onset_date')
  cur.execute('SELECT ' + ', '.join(clm) + ' FROM reac WHERE case_id == ?;', (str(case_id),))
  return table_to_json(clm, cur.fetchall())


@route('/reac/:case_id')
def hist(case_id):
  clm = ('case_id', 'freq', 'sn', 'disease')
  cur.execute('SELECT ' + ', '.join(clm) + ' FROM hist WHERE case_id == ?;', (str(case_id),))
  return table_to_json(clm, cur.fetchall())


run(host='localhost', port=8000, debug=True, reloader=True)
