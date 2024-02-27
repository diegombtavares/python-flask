from main import app, db
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Usuarios
from helpers.modules import FormularioUsuario, validar_sessao_usuario
from flask_bcrypt import generate_password_hash

@app.route('/user')
@validar_sessao_usuario
def user():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '') 
    
    por_pagina = 10
    
    if search_query:
        lista = Usuarios.query.filter((Usuarios.nome.ilike(f"%{search_query}%")) | (Usuarios.user.ilike(f"%{search_query}%"))) \
                              .order_by(Usuarios.id) \
                              .paginate(page=page, per_page=por_pagina)
    else:
        lista = Usuarios.query.order_by(Usuarios.id).paginate(page=page, per_page=por_pagina)
    
    return render_template('user/usuarios.html', titulo='Usuários', usuarios=lista)

@app.route('/deletar-user/<int:id>')
@validar_sessao_usuario
def deletar_user(id):
    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário deletado com sucesso')

    previous_page = request.referrer
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect(url_for('index'))

@app.route('/editar-user/<int:id>')
@validar_sessao_usuario
def editar_user(id): 
    usuario = Usuarios.query.filter_by(id=id). first()
    form = FormularioUsuario()
    form.user.data = usuario.user
    form.nome.data = usuario.nome
    form.senha.data = usuario.senha

    return render_template('user/editar-user.html', titulo='Editando Usuário', id=id, form=form)

@app.route('/')
@validar_sessao_usuario
def index():
    return redirect(url_for('user'))

@app.route('/atualizar-user', methods=['POST',])
@validar_sessao_usuario
def atualizar_user():
    usuario_id = request.form.get('id')
    usuario = Usuarios.query.get(usuario_id) 

    if usuario is None:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('user'))

    form = FormularioUsuario(obj=usuario)

    if form.validate_on_submit():
        form.populate_obj(usuario)

        nova_senha = request.form.get('senha')
        if nova_senha:
            usuario.senha = generate_password_hash(nova_senha).decode('utf-8')

        db.session.commit()

        flash('Usuário atualizado com sucesso.', 'success')
        return redirect(url_for('user'))

    flash('Erro ao atualizar o usuário. Por favor, corrija os erros no formulário.', 'error')
    return render_template('user/editar-user.html', titulo='Editando Usuário', id=usuario_id, form=form)

@app.route('/novo-user')
@validar_sessao_usuario
def novo_user():
    form = FormularioUsuario()
    return render_template('user/new-user.html', titulo='Novo Usuário', form=form)

@app.route('/criar-user', methods=['POST'])
@validar_sessao_usuario
def criar_user():
    form = FormularioUsuario(request.form)

    if form.validate_on_submit():
        nome = form.nome.data
        user = form.user.data
        senha = form.senha.data
        profile = form.role.data

        usuario = Usuarios.query.filter_by(nome=nome).first()

        if usuario:
            flash('Usuário já existente')
            return redirect(url_for('user'))

        senha_hash = generate_password_hash(senha).decode('utf-8')

        novo_user = Usuarios(nome=nome, user=user, senha=senha_hash, profile=profile)
        db.session.add(novo_user)
        db.session.commit()
        flash('Usuário criado com sucesso')

        return redirect(url_for('user'))
    else:
        flash('Por favor, preencha todos os campos corretamente.', 'error')
        return render_template('user/new-user.html', titulo='Novo Usuário', form=form)

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('public', nome_arquivo)
