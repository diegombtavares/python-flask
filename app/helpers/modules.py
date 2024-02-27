import os 
from main import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from functools import wraps
from flask import redirect, flash, session, request, url_for
from models import Usuarios

class FormularioUsuario(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=50)])
    user = StringField('User', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    role = SelectField('Perfil', choices=[('admin', 'Admin'), ('user', 'Usuário')], validators=[DataRequired(message="Por favor, selecione um perfil.")])
    login = SubmitField('Entrar')
    salvar = SubmitField('Salvar')


def validar_sessao_usuario(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'usuario_logado' not in session or session['usuario_logado'] is None:
            flash('Faça login para acessar esta página', 'error')
            return redirect(url_for('login', proxima=request.url))

        usuario = Usuarios.query.filter_by(user=session['usuario_logado']).first()
        if not usuario:
            session.pop('usuario_logado', None)
            flash('Sua sessão expirou, faça o login novamente', 'error')
            return redirect(url_for('login', proxima=request.url))

        return route_function(*args, **kwargs)
    
    return wrapper