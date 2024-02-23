from main import app, db
from flask import render_template, request, redirect, session, flash, url_for
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
    search_query = request.args.get('q', '') 
    
    por_pagina = 10
    
    if search_query:
        lista = Usuarios.query.filter((Usuarios.nome.ilike(f"%{search_query}%")) | (Usuarios.nickname.ilike(f"%{search_query}%"))) \
                              .order_by(Usuarios.id) \
                              .paginate(page=page, per_page=por_pagina)
    else:
        lista = Usuarios.query.order_by(Usuarios.id).paginate(page=page, per_page=por_pagina)
    
    return render_template('user/usuarios.html', titulo='Usuários', usuarios=lista)

@app.route('/deletar-user/<int:id>')
def deletar_user(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))    
    
    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário deletado com sucesso')

    previous_page = request.referrer
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect(url_for('index'))

@app.route('/editar-user/<int:id>')
def editar_user(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar-user')))
    
    usuario = Usuarios.query.filter_by(id=id). first()
    form = FormularioUsuario()
    form.nickname.data = usuario.nickname
    form.nome.data = usuario.nome
    return render_template('user/editar-user.html', titulo='Editando Usuário', id=id, form=form)

@app.route('/atualizar-user', methods=['POST',])
def atualizar_user():
    usuario_id = request.form.get('id')
    usuario = Usuarios.query.get(usuario_id) 

    if usuario is None:
        
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('user'))

    form = FormularioUsuario(obj=usuario)

    if form.validate_on_submit():
        form.populate_obj(usuario)

        db.session.commit()

        flash('Usuário atualizado com sucesso.', 'success')
        return redirect(url_for('user'))

    flash('Erro ao atualizar o usuário. Por favor, corrija os erros no formulário.', 'error')
    return render_template('user/editar-user.html', titulo='Editando Usuário', id=usuario_id, form=form)
