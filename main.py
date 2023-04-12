from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.films import Films
from data.frames import Frames
from data.users import User
from forms.user import RegisterForm
import sqlite3
from random import shuffle
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
    for film in db_sess.query(Films).filter(Frames.film_id == Films.id):
        films_title.append(film.title)
    for filename in db_sess.query(Frames).filter(Frames.film_id == Films.id):
        filenames.append(filename.filename)

    form = AnswerForm()
    print(films_title)
    shuffle(films_title)
    form.answer2.choices = [films_title[:2]]
    shuffle(films_title)
    form.answer3.choices = [films_title[:2]]

    if form.validate_on_submit():
        return '...'
    return render_template('frames.html', title='угадай по кадрам', form=form, films=films_title, filenames=filenames)


@app.route('/location')
def location():
    return 'локация'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
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
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/base.sqlite")
    db_sess = db_session.create_session()

    user = db_sess.query(User).first()
    print(user.name)
    app.run()


if __name__ == '__main__':
    main()
