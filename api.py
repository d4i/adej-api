#!/usr/bin/env python

import json
import sqlite3
from bottle import route, run

conn = sqlite3.connect('adej.sqlite3')
cur = conn.cursor()


meta = {
    'disclaimer': 'Adej is a beta research project and not for clinical use.',
    'terms_of_data_service': 'http://www.info.pmda.go.jp/fukusayou/consentDownLoad.html',
    'last_updated': '2014-08-06'
}


def table_to_dict(cl, tab):
  len_cl = len(cl)

  if type(tab) == tuple:
    param = dict()
    for i in range(0, len_cl):
      param[cl[i]] = tab[i]
  elif type(tab) == list:
    param = list()
    for r in tab:
      p = dict()
      for i in range(0, len_cl):
        p[cl[i]] = r[i]
      param.append(p)

  return param


@route('/case/:case_id')
def case(case_id):
  param = {
      'meta': meta,
      'results': dict()
  }
  cls = {
      'demo': ('case_id', 'freq', 'sex', 'age', 'weight', 'height', 'quarter', 'status', 'report', 'reporter'),
      'drug': ('case_id', 'freq', 'sn', 'association', 'name', 'brand', 'route', 'start_date', 'end_date', 'dosage', 'unit', 'fraction', 'reason', 'fix', 'relapse'),
      'reac': ('case_id', 'freq', 'sn', 'event', 'outcome', 'onset_date'),
      'hist': ('case_id', 'freq', 'sn', 'disease')
  }

  for tab in cls:
    cur.execute('SELECT ' + ', '.join(cls[tab]) + ' FROM ' + tab + ' WHERE case_id == ?;', (str(case_id),))
    if tab == 'demo':
      res = cur.fetchone()
    else:
      res = cur.fetchall()
    param['results'][tab] = table_to_dict(cls[tab], res)

  return json.dumps(param, ensure_ascii=False)


@route('/')
def index():
  return 'root'


run(host='localhost', port=8000, debug=True, reloader=True)
