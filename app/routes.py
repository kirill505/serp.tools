from app import app, celery
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, Top10Form, RegistrationForm
from app.models import User
import uuid
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db
from datetime import datetime
from app.forms import EditProfileForm
import nltk
import os
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
@app.route('/', methods=['GET', 'POST'])
#@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    title ='Главная'
    h1 = {'h1': 'Инструменты для SEO-специалистов'}
    services = [
    {
        'title': 'Лемматизация',
        'description': 'С помощью инструмента можно быстро лемматизировать текст (приводит к именительному падежу единственному числу) и проверять на N-граммы в тексте.'
    },
    {
        'title': 'Парсинг подсветок',
        'description': 'Инструмент, который поможет по запросу спарсить подсветки (выделенные жирным) поисковой системы Google.'
    },
    {
        'title': 'Выгрузка ТОП-10',
        'description': 'Инструмент, который поможет быстро выгрузить топ-10 сайтов по заданным запросам, в поисковой системе Google.'
    },
    ]
    return render_template('index.html', title=title, h1=h1, services=services)

#('/top10/', methods=['GET', 'POST'])
#@celery.task
@app.route('/top10/')
def top10():
    #add.delay(3, 4)
    #top_10_res.apply_async([4])
    
    return render_template('top10.html')

#@celery.task(bind=True)
@app.route('/top10/res', methods=['POST', 'GET'])
def top_10_res():
    
    response_object = dict()
    if request.method == "POST":
        
        post_data = request.values.to_dict()

        #эти данные передаем XMLRiver
        response_object['keys'] = post_data['keys'].split('\n')
        response_object['loc'] = post_data['loc']
        response_object['groupby'] = int(post_data['groupby'])
        response_object['lr'] = post_data['lr']
        response_object['domain'] = post_data['domain']
        response_object['country'] = post_data['country']
        response_object['device'] = post_data['device']
        
        #тут нужно вызвать отложенный запрос к XMLRiver
        #id запроса к XMLRiver, TRUE или ошибку
        res2 = dict()
        for i in response_object['keys']:
            test = ya_search_xmlriver(i, response_object['loc'], response_object['groupby'], response_object['lr'], response_object['domain'], response_object['country'], response_object['device'])
            res2[i] = test.urls(response_object['groupby'])
        print(res2)
        #в аргументе передаем id заказа
    #    task = long_task.apply_async()        

    return jsonify(res2, {}, 202, {'Location': url_for('taskstatus', task_id=task.id)})

#@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    
    #удалить эту "красоту", вместо нее цикл while пока не получен успешный ответ от XMLRiver, 
    #через каждые 5 сек. делаем запрос к XMLRiver, получаем ответ
    #результаты ответа отправляем POST запросом к таске //status/a3df0d9b-c095-4491-949d-d8b49bf1d925
    #пример task = my_background_task.apply_async(args=[10, 20], countdown=60)

    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

#к ответу нужно добавить id отложенного запроса к XMLRiver
@app.route('/status/<task_id>')
def taskstatus(task_id):
    #task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

#@celery.task
def add(x, y):
    return x + y

@app.route('/top10/res2', methods=['POST', 'GET'])
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

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username']
    password = request.form['password']
    text = request.form['textik']
    return jsonify({'status':'OK','user':user,'pass':password,'text':text})

def count_and_save_words(url):

    errors = []

    try:
        r = requests.get(url)
    except:
        errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
        )
        return {"error": errors}

    # text processing
    raw = BeautifulSoup(r.text).get_text()
    nltk.data.path.append('./nltk_data/')  # set the path
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)

    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)

    # save the results
    try:
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )

        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}

stops = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
    'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
    'with', 'about', 'against', 'between', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
    'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
    't', 'can', 'will', 'just', 'don', 'should', 'now', 'id', 'var',
    'function', 'js', 'd', 'script', '\'script', 'fjs', 'document', 'r',
    'b', 'g', 'e', '\'s', 'c', 'f', 'h', 'l', 'k'
]

@app.route('/freq', methods=['GET', 'POST'])
def freq():
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        url = request.form['url']
        if 'http://' not in url[:7]:
            url = 'http://' + url
        job = q.enqueue_call(
            func=count_and_save_words, args=(url,), result_ttl=5000
        )
        print(job.get_id())

    return render_template('freq.html', results=results)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return "Nay!", 202

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/profile/<int:id>')
def profile(id):
    user = User()
    return "Hello world {}".format(id)

@app.route('/_add_numbers', methods=['POST'])
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify({'data': render_template('_add_numbers.html', result=a + b)})

#@app.route("/<any(plain, jquery, fetch):js>")
#def index(js):
 #   return render_template("{0}.html".format(js), js=js)

@app.route('/ping', methods=['GET'])
def ping_pong():
     return jsonify('pong!')
BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
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