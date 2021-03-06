# -*- coding : utf-8 -*-

from flask import Flask, request, flash, url_for, \
    redirect, render_template, session, jsonify
from database import db_master
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adambaylin'

@app.route('/')
def homepage():
    a = db_master(mode='qall_cookies')
    return render_template('home.html', nick = a)

@app.route('/nick/<uid>', methods=['GET', 'POST'])
def do_nick(uid):
    now = datetime.datetime.now()
    a = now.strftime("%d/%m %H:%M:%S")
    db_master(mode='live_cookies',uid=uid, time=a)
    return ''
    
@app.route('/check/<uid>', methods=['GET', 'POST'])
def check_time(uid):
    a = db_master(mode='die_check', uid=uid)
    return str(a)

@app.route('/cookies/<uid>', methods=['GET', 'POST'])
def get_cookies(uid):
    cookies = db_master(mode='query_cookies', uid = uid)
    return str(cookies.cookies)

@app.route('/logic/<mode>', methods=['GET', 'POST'])
def do_logic(mode):
    if mode == 'add_uid':
        uidx = request.form['add_uid']
        uidx = eval(uidx)
        uidx = uidx.splitlines()
        i = 0
        for uid in uidx:
            i += 1
            db_master(mode='add_uid',uid=uid)
        i = '<p id="total_add">Had add {} uid to Database </p>'.format(i)
        return jsonify({'data': i})
    
    if mode == 'del_all':
        db_master(mode='del_all')
        i = '<p id="total_add">Had delete all uid to Database</p>'
        return jsonify({'data': i})

    if mode == 'check_status':
        now = datetime.datetime.now()
        a, b = db_master(mode='max_uid'), db_master(mode='min_uid')
        try:
            c = int(a) - int(b) + 1
        except:
            c = 0
        d = now.strftime("%H:%M:%S | %d-%m-%Y")
        f = len(db_master(mode='qall_cookies'))
        e = """<div class="status_uid">
            <ul id='status_main'>
                <li>Total UID: {}</li>
                <li>Last Update: {}</li>
                <li>Nick Facebook: {}</li>
            </ul></div>""".format(c, d, f)
        return e

    if mode == 'get_uid':
        return str(db_master(mode='get_uid'))

    if mode == 'add_cookies':
        cookies = request.form['add_cookies']
        cookies = eval(cookies)
        db_master(mode=mode,cookies=cookies)
        i = '<p id="total_add">Had add Cookies to Database </p>'
        return jsonify({'data': i})

    if mode == 'qall_cookies':
        a = db_master(mode='qall_cookies')
        return jsonify({'data': render_template('nick.html',nick = a)})

    if mode == 'del_nick':
        uid = request.form['del_nick']
        uid = eval(uid)
        db_master(mode='del_cookies',uid=uid)

    if mode == 'query_nick':
        a = db_master(mode='qall_cookies')
        b = []
        for c in a:
            d = {}
            d['uid'] = c.uid
            d['name'] = c.name
            b.append(d)
        return str(b)

    if mode == 'update_token':
        token = request.form['token']
        db_master(mode='add_token',token=token)
        return 'Done'

    if mode == 'check_token':
        a = db_master(mode='check_token')
        if a:
            i = '<div id="status_token"><div class="live"></div></div>'
        else:
            i = '<div id="status_token"><div class="die"></div></div>'
        return jsonify({'data': i})

    return ''

if __name__ == '__main__':
    app.run(debug=True)