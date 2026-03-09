from flask import render_template, redirect, request, session, url_for
from skinna import app, db
from skinna.models import Cardapio, Programacao, Promocao
from datetime import datetime
import os

# Usuário e senha admin fixos
ADMIN_USER = "admin@gmail.com"
ADMIN_PASS = "123"

# PASTA DE UPLOADS
UPLOAD_FOLDER = os.path.join("skinna", "static", "img")

# --------------------- ROTAS PÚBLICAS ---------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cardapio")
def cardapio():
    itens = Cardapio.query.all()
    return render_template("cardapio.html", itens=itens)


@app.route("/programacao")
def programacao():
    eventos = Programacao.query.all()
    return render_template("programacao.html", eventos=eventos)


@app.route("/promocoes")
def promocoes():
    promocoes = Promocao.query.filter(Promocao.data_fim > datetime.now()).all()
    return render_template("promocoes.html", promocoes=promocoes)


# --------------------- LOGIN ADMIN ---------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == ADMIN_USER and senha == ADMIN_PASS:
            session["admin"] = True
            return redirect("/adm")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# --------------------- PAINEL ADMIN ---------------------

@app.route("/adm")
def adm():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("adm/painel.html")


# --------------------- ADMIN CARDÁPIO ---------------------

@app.route("/adm/cardapio", methods=["GET", "POST"])
def adm_cardapio():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        preco = request.form.get("preco")
        categoria = request.form.get("categoria")
        imagem = request.files.get("imagem")
        nome_imagem = None
        if imagem:
            caminho = os.path.join(UPLOAD_FOLDER, imagem.filename)
            imagem.save(caminho)
            nome_imagem = imagem.filename

        item = Cardapio(nome=nome, descricao=descricao, preco=preco, categoria=categoria, imagem=nome_imagem)
        db.session.add(item)
        db.session.commit()
        return redirect("/adm/cardapio")

    itens = Cardapio.query.all()
    return render_template("adm/editar_cardapio.html", itens=itens)


# --------------------- ADMIN PROGRAMAÇÃO ---------------------

@app.route("/adm/programacao", methods=["GET", "POST"])
def adm_programacao():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        dia = request.form.get("dia")
        evento = request.form.get("evento")
        imagem = request.files.get("imagem")
        nome_imagem = None
        if imagem:
            caminho = os.path.join(UPLOAD_FOLDER, imagem.filename)
            imagem.save(caminho)
            nome_imagem = imagem.filename

        prog = Programacao(dia=dia, evento=evento, imagem=nome_imagem)
        db.session.add(prog)
        db.session.commit()
        return redirect("/adm/programacao")

    eventos = Programacao.query.all()
    return render_template("adm/editar_programacao.html", eventos=eventos)


# --------------------- ADMIN PROMOÇÕES ---------------------

@app.route("/adm/promocoes", methods=["GET", "POST"])
def adm_promocoes():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        item_id = request.form.get("item_id")
        preco = request.form.get("preco")
        data_string = request.form.get("data_fim")
        data_fim = datetime.strptime(data_string, "%Y-%m-%d")

        promo = Promocao(item_id=item_id, preco_promocional=preco, data_fim=data_fim)
        db.session.add(promo)
        db.session.commit()
        return redirect("/adm/promocoes")

    itens = Cardapio.query.all()
    promocoes = Promocao.query.all()
    return render_template("adm/promocoes.html", itens=itens, promocoes=promocoes)