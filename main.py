from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from forms.user import RegisterForm
import sqlite3

from qwerty_2.qwerty.flask.forms.LoginForm import LoginForm
from qwerty_2.qwerty.flask.forms.frames_form import AnswerForm

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
    con = sqlite3.connect('db/base.sqlite')
    cursor = con.cursor()
    query1 = 'SELECT filename FROM frames WHERE film_id IN (SELECT id FROM films)'
    result = cursor.execute(query1)
    data = result.fetchall()
    con.close()
    print(data)
    form = AnswerForm()
    form.answer2.choices = ['1', '2']
    form.answer3.choices = [4, 5]
    if form.validate_on_submit():
        return '...'
    return render_template('frames.html', title='угадай по кадрам', data=[i[0] for i in data], form=form)


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
