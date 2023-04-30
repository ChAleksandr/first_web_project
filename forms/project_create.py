from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    name = StringField('имя проекта', validators=[DataRequired()])
    about = TextAreaField("Содержание")
    submit = SubmitField('Применить')