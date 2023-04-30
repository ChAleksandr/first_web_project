from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class TeamForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    role = StringField('Роль', validators=[DataRequired()])
    submit = SubmitField('Применить')