from random import shuffle, choice, sample

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.films import Films
from data.frames import Frames
from data.soundtracks import Soundtracks
from data.users import User
from forms.LoginForm import LoginForm
from forms.frames_form import FramesAnswerForm
from forms.soundtracks_form import SoundtrackAnswerForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

current_answers_frames = {}
current_answers_soundtracks = {}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')


@app.route("/soundtrack", methods=['GET', 'POST'])
@login_required
def soundtrack():
    form = SoundtrackAnswerForm()

    if form.validate_on_submit():
        cnt = 0
        for i, v in enumerate(list(form)[:-2]):
            if v.data == current_answers_soundtracks[current_user.id][i]:
                cnt += 1
                print(cnt)
        return render_template('points.html', title='количество правильных ответов', cnt=cnt)
    db_sess = db_session.create_session()
    all_films = db_sess.query(Films).all()

    soundtracks = sample(db_sess.query(Soundtracks).all(), k=5)
    answer_options = [db_sess.query(Films).filter(Films.id == soundtracks[0].film_id).first().title]
    answer_options2 = [db_sess.query(Films).filter(Films.id == soundtracks[1].film_id).first().title]
    answer_options3 = [db_sess.query(Films).filter(Films.id == soundtracks[2].film_id).first().title]
    answer_options4 = [db_sess.query(Films).filter(Films.id == soundtracks[3].film_id).first().title]
    answer_options5 = [db_sess.query(Films).filter(Films.id == soundtracks[4].film_id).first().title]
    list_of_answer_options = [answer_options, answer_options2, answer_options3, answer_options4, answer_options5]
    list_of_forms = [form.answer1, form.answer2, form.answer3, form.answer4, form.answer5]
    for i, answer in enumerate(list_of_answer_options):
        while len(answer) != 4:
            film = choice(all_films).title
            if film not in answer:
                answer.append(film)
        shuffle(answer)
        print(answer)
        print(list_of_forms[i])
        list_of_forms[i].choices = answer
    correct_films = []
    for elem in soundtracks:
        correct_soundtrack = db_sess.query(Soundtracks).filter(
            Soundtracks.filename == elem.filename).first()
        correct_films.append(
            db_sess.query(Films).filter(Films.id == correct_soundtrack.film_id).first().title)
    current_answers_soundtracks[current_user.id] = correct_films
    return render_template('soundtrack.html', title='угадай по саундтреку', form=form,
                           filenames=[i.filename for i in soundtracks])


@app.route('/frames', methods=['GET', 'POST'])
@login_required
def frames():
    form = FramesAnswerForm()
    if form.validate_on_submit():
        cnt = 0
        for i, v in enumerate(list(form)[:-2]):
            if v.data == current_answers_frames[current_user.id][i]:
                cnt += 1
                print(cnt)
        return render_template('points.html', title='количество правильных ответов', cnt=cnt)

    db_sess = db_session.create_session()
    all_films = db_sess.query(Films).all()
    frames = sample(db_sess.query(Frames).all(), k=5)

    answer_options = [db_sess.query(Films).filter(Films.id == frames[0].film_id).first().title]
    answer_options2 = [db_sess.query(Films).filter(Films.id == frames[1].film_id).first().title]
    answer_options3 = [db_sess.query(Films).filter(Films.id == frames[2].film_id).first().title]
    answer_options4 = [db_sess.query(Films).filter(Films.id == frames[3].film_id).first().title]
    answer_options5 = [db_sess.query(Films).filter(Films.id == frames[4].film_id).first().title]
    list_of_answer_options = [answer_options, answer_options2, answer_options3, answer_options4,answer_options5]

    list_of_forms = [form.answer1, form.answer2, form.answer3, form.answer4, form.answer5]
    for i, answers in enumerate(list_of_answer_options):

        while len(answers) != 4:
            film = choice(all_films).title
            if film not in answers:
                answers.append(film)
        shuffle(answers)
        print(answers)
        print(list_of_forms[i])
        list_of_forms[i].choices = answers
    correct_films = []
    for elem in frames:
        correct_frame = db_sess.query(Frames).filter(Frames.filename == elem.filename).first()
        correct_films.append(
            db_sess.query(Films).filter(Films.id == correct_frame.film_id).first().title)
    current_answers_frames[current_user.id] = correct_films
    return render_template('frames.html', title='угадай по кадрам', form=form,
                           filenames=[i.filename for i in frames])


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


@app.route('/play')
def play():
    return render_template('play.html')


@app.route('/location')
def location():
    return 'локация'


@app.route('/rules')
def rules():
    return render_template('rules.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
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
        user = User(name=form.name.data, email=form.email.data)
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
