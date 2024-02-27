import os 
from main import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, validators
from wtforms.validators import DataRequired, Length

class FormularioUsuario(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=50)])
    user = StringField('User',[validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    role = SelectField('Perfil', choices=[('admin', 'Admin'), ('user', 'Usuário')], validators=[DataRequired()])
    login = SubmitField('Entrar')
    salvar = SubmitField('Salvar')