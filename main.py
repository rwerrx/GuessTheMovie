from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.films import Films
from data.frames import Frames
from data.users import User
from forms.user import RegisterForm
import sqlite3
from random import shuffle, choices, choice
from forms.LoginForm import LoginForm
from forms.frames_form import AnswerForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')


@app.route("/soundtrack")
def soundtrack():
    return 'саундтрек'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/frames')
def frames():
    films_title = []
    filenames = []
    db_sess = db_session.create_session()
    all_films = db_sess.query(Films).all()
    # for film in db_sess.query(Films).all():
        # films_title.append(film.title)
    frames = choices(db_sess.query(Frames).all(), k=5)
        # filenames.append(filename.filename)

    form = AnswerForm()
    answers = [db_sess.query(Films).filter(Films.id == frames[0].film_id).first().title]
    while len(answers) != 4:
        film = choice(all_films).title
        if film not in answers:
            answers.append(film)
    shuffle(answers)
    form.answer1.choices = answers

    answers2 = [db_sess.query(Films).filter(Films.id == frames[1].film_id).first().title]
    while len(answers2) != 4:
        film = choice(all_films).title
        if film not in answers2:
            answers2.append(film)
    shuffle(answers2)
    form.answer2.choices = answers2

    answers3 = [db_sess.query(Films).filter(Films.id == frames[2].film_id).first().title]
    while len(answers3) != 4:
        film = choice(all_films).title
        if film not in answers3:
            answers3.append(film)
    shuffle(answers3)
    form.answer3.choices = answers3

    answers4 = [db_sess.query(Films).filter(Films.id == frames[3].film_id).first().title]
    while len(answers4) != 4:
        film = choice(all_films).title
        if film not in answers4:
            answers4.append(film)
    shuffle(answers4)
    form.answer4.choices = answers4

    answers5 = [db_sess.query(Films).filter(Films.id == frames[4].film_id).first().title]
    while len(answers5) != 4:
        film = choice(all_films).title
        if film not in answers5:
            answers5.append(film)
    shuffle(answers5)
    form.answer5.choices = answers5
    # shuffle(films_title)
    # form.answer2.choices = films_title[:len(filenames)]
    # shuffle(films_title)
    # form.answer3.choices = films_title[:len(filenames)]
    # shuffle(films_title)
    # form.answer4.choices = films_title[:len(filenames)]
    if form.validate_on_submit():
        return '...'
    return render_template('frames.html',
                           title='угадай по кадрам',
                           form=form,
                           filenames=[i.filename for i in frames])


@app.route('/location')
def location():
    return 'локация'


@app.route('/rules')
def rules():
    return render_template('rules.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация', form=form)


def main():
    db_session.global_init("db/base.sqlite")
    db_sess = db_session.create_session()

    user = db_sess.query(User).first()
    print(user.name)
    app.run()


if __name__ == '__main__':
    main()