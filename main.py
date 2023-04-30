
from data import db_session
from data.users import User
from data.projects import Project
from data import db_session, news_api, jobs_api
from data.team import Team

from forms.log import LoginForm
from forms.user import RegisterForm
from forms.project_create import ProjectForm
from forms.team_member_add import TeamForm

from flask_mqtt import Mqtt
from flask import render_template, redirect, Flask, request, abort, jsonify, make_response, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from web_config import apply_config


topic = "ev3/evrika"

app = Flask(__name__)
# инициализация
mqtt = Mqtt(app)
mqtt.init_app(app)
mqtt.on_message()

login_manager = LoginManager()
login_manager.init_app(app)

# настрйоки
apply_config(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route('/team')
def team():
    db_sess = db_session.create_session()
    team_members = db_sess.query(Team)
    return render_template("team.html", team=team_members)


@app.route('/team_add',  methods=['GET', 'POST'])
def team_add():
    form = TeamForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Team).filter(User.name == form.name.data).first():
            return render_template('team_add.html',
                                   form=form,
                                   message="Такой пользователь уже есть")

        team_user_id = db_sess.query(User.id).filter(User.name == form.name.data)
        tm = Team(
            name=form.name.data,
            role=form.role.data,
            user_id=team_user_id
        )
        db_sess.add(tm)
        db_sess.commit()
        return redirect('/team')
    return render_template('team_add.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
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


@app.route('/project_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def project_delete():
    db_sess = db_session.create_session()
    project = db_sess.query(Project).filter(Project.id == id).first()
    if project:
        db_sess.delete(project)
        db_sess.commit()
    else:
        abort(404)
        return redirect('/projects')


@app.route('/project', methods=['GET', 'POST'])
@login_required
def project_add():
    form = ProjectForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Project).filter(Project.name == form.name.data).first():
            return render_template('project.html',
                                   form=form,
                                   message="Такой проект уже есть")
        prj = Project(
            name=form.name.data,
            about=form.about.data,
        )
        db_sess.add(prj)
        db_sess.commit()
        return redirect('/projects')
    return render_template('project.html', title='Добавление проекта', form=form)


@app.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    db_sess = db_session.create_session()
    project = db_sess.query(Project)
    return render_template('projects.html', project=project)


@app.route('/projects/1',  methods=['GET', 'POST'])
@app.route('/projects/paper_machine',  methods=['GET', 'POST'])
def paper_machine():
    return render_template('paper_machine.html')


@app.route('/projects/smart_box-started',  methods=['GET', 'POST'])
def paper_machine_started():
    mqtt.publish('nergi/n', 'smart_box_start')
    mqtt.publish(topic, 'smart_box_start')
    mqtt.publish(topic, 'smart_box_start')
    mqtt.publish(topic, 'smart_box_start')
    print('posted')
    return render_template('paper_machine-started.html')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("/sensors/get")
    print("Connected with result code "+str(rc))
    mqtt.publish('/sensors/get')
    mqtt.publish('/sensors/get')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(message.paylode.decode('utf-8'))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def get_model_dict(model):
    return dict((column.name, getattr(model, column.name))
                for column in model.__table__.columns)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
