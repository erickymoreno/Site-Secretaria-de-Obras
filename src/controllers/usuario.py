from src import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user, login_user, logout_user
from src.models.tables import Usuario, Endereco
import bcrypt, sys

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method =="GET":
        mensagem = request.args.get("mensagem")
        return render_template("cadastro.html")

    if request.method == "POST":
        nome = request.form["inputNome"]
        nome+= " " + request.form["inputSobrenome"]
        cpf = request.form["inputCpf"]
        data_de_nascimento = request.form["inputDataDeNascimento"]
        email = request.form["inputEmail"]

        if request.form["inputSenha"] == request.form["inputConfirmaSenha"]:
            senha = request.form["inputSenha"]
            senhaEcriptada = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())
        else:
            mensagem = "As senhas não correspondem"
            return render_template("cadastro.html", mensagem=mensagem)

        cep = request.form["inputCep"]
        rua = request.form["inputRua"]
        bairro = request.form["inputBairro"]
        numero = request.form["inputNumero"]
        referencia = request.form["inputReferencia"]
        telefone = request.form["inputTelefone"]

        usuario = Usuario(nome=nome, cpf=cpf, data_de_nascimento=data_de_nascimento, email=email, senha=senhaEcriptada, telefone=telefone)
        db.session.add(usuario)
        db.session.commit()
        
        endereco= Endereco(rua=rua, numero=numero, bairro=bairro, cep=cep, referencia=referencia, usuario_id=usuario.id)
        db.session.add(endereco)
        db.session.commit()
        return render_template("cadastro.html")


@login_manager.user_loader
def get_user(usuario_id):
    return Usuario.query.filter_by(id=usuario_id).first()

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("login.html", mensagem=mensagem)

    if request.method == "POST":
        email = request.form["inputEmail"]
        senha = request.form["inputSenha"]

        usuario = Usuario.query.filter_by(email=email).first()
        autozidado = False

        if usuario:
            autorizado = bcrypt.checkpw(
                senha.encode("utf8"), usuario.senha.encode("utf8")
            )

        if not usuario or not autorizado:
            mensagem = "Email ou senha incorreto"
            return render_template("login.html", mensagem=mensagem)
        else:
            login_user(usuario)
            return redirect("/home")

