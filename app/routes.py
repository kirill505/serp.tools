from app import app, celery
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, Top10Form, RegistrationForm
from app.models import User
#import uuid
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db
from datetime import datetime
from app.forms import EditProfileForm
#import nltk
#import os
import requests
import operator
import re
from collections import Counter
from bs4 import BeautifulSoup
import json
from werkzeug.datastructures import CombinedMultiDict, MultiDict
import random
import time
from .backlights import ya_search_xmlriver
from lxml import html
from .xmlriver import *

@app.route('/ru', methods=['GET', 'POST'])
#@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    title ='Главная'
    h1 = {'h1': 'Инструменты для SEO-специалистов'}
    services = [
    {
        'title': 'Выгрузка ТОП-10',
        'description': 'Инструмент, который поможет быстро выгрузить топ-10 сайтов по заданным запросам, в поисковой системе Google.',
        'url': 'ru/top10/'
    },
    {
        'title': 'Лемматизация',
        'description': 'С помощью инструмента можно быстро лемматизировать текст (приводит к именительному падежу единственному числу) и проверять на N-граммы в тексте.',
        'url': '#'
    },
    {
        'title': 'Парсинг подсветок',
        'description': 'Инструмент, который поможет по запросу спарсить подсветки (выделенные жирным) поисковой системы Google.',
        'url': '#'
    },
    ]
    return render_template('index.html', title=title, h1=h1, services=services)

#('/top10/', methods=['GET', 'POST'])
@app.route('/ru/top10/')
def top10():
    
    return render_template('top10.html')

@app.route('/ru/top10/res', methods=['POST', 'GET'])
def top_10_res():

    response_object = dict()
    if request.method == "POST":
        
        post_data = request.values.to_dict()

        #эти данные передаем XMLRiver
    
        
        #тут нужно вызвать отложенный запрос к XMLRiver
        #id запроса к XMLRiver, TRUE или ошибку
        res2 = dict()
        base_url = 'http://xmlriver.com/search/xml?user=798&key=c17a38a762f9f72d80d12489ee7b5d4b35dd2aff'
        for i in post_data['keys'].split('\n'):
            res2[i] = get_urls_in_xmlriver(base_url,
                query = i, 
                loc = post_data['loc'], 
                groupby = int(post_data['groupby']), 
                lr = post_data['lr'],
                domain = post_data['domain'],
                country = post_data['country'], 
                device = post_data['device'])
            #if resp[0] == "SUCCESS":
                #task = long_task.apply_async()
            #res2[i] = get_urls_in_xmlriver(resp[1])

        print(res2)
        #в аргументе передаем id заказа

    return jsonify(res2)
    #, {}, 202, {'Location': url_for('taskstatus', task_id=task.id)})

#тут надо добавить ф-ию получения id таски XMLRiver
def top10_task_id():
    
    return True

#ф-ия парсинга XML-ки 
def get_xml_data():
    
    return

#@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    
    #удалить эту "красоту", вместо нее цикл while пока не получен успешный ответ от XMLRiver, 
    #через каждые 5 сек. делаем запрос к XMLRiver, получаем ответ
    #результаты ответа отправляем POST запросом к таске //status/a3df0d9b-c095-4491-949d-d8b49bf1d925
    #пример task = my_background_task.apply_async(args=[10, 20], countdown=60)

    task_done = False
    while not task_done:
        self.update_state(state='PROGRESS',
                          meta={'id_task': 0,
                                'status': message})
        time.sleep(1)
    return {'id_task': id, 'status': 'Task completed!',
            'result': 42}

#к ответу нужно добавить id отложенного запроса к XMLRiver
@app.route('/ru/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'id_task': 0,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'id_task': task.info.get('id_task', 0),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'id_task': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

@app.route('/ru/top10/res2', methods=['POST', 'GET'])
def top_10_res2():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        #print (request.args) #500 ответ, has no attribute 'arg'
        #post_data = request.values.to_dict(flat=False)
        
        print (request.values) #400 ответ, CombinedMultiDict
        #print (request.json)  #400 ответ, NONE
        #print (request.get_json(force=True)) #400 ответ, пусто
        print (request.form) #200 ответ, null
        #print(post_data)
    return jsonify(response_object)

@app.route('/ru/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username']
    password = request.form['password']
    text = request.form['textik']
    return jsonify({'status':'OK','user':user,'pass':password,'text':text})

@app.route('/ru/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/ru/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/ru/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/ru/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/ru/profile/<int:id>')
def profile(id):
    user = User()
    return "Hello world {}".format(id)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/ru/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
                        
@app.route("/ru/robots.txt")
def robots_txt():
    return render_template("robots.txt")