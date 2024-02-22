from main import app
from flask import render_template, request, redirect, session, flash, url_for
from helpers.modules import recupera_imagem, deleta_arquivo, FormularioJogo
from models import Jogos
from models import Usuarios
from helpers.modules import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    
    if usuario is not None:
        senha_correta = check_password_hash(usuario.senha, form.senha.data)
        if senha_correta:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso', 'succes')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    
    flash('Credencias Inválidas', 'error')
    return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso', 'succes')
    return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('user')))
    
    page = request.args.get('page', 1, type=int)
    
    por_pagina = 10
    
    lista = Usuarios.query.order_by(Usuarios.id).paginate(page=page, per_page=por_pagina)
    
    return render_template('usuarios.html', titulo='Usuários', usuarios=lista)