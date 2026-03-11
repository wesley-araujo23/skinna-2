from flask import render_template, redirect, request, session, url_for, jsonify
from skinna import app, db
from skinna.models import Produto, Pedido, ItemPedido, Programacao, Promocao
from datetime import datetime
import json
from functools import wraps

# ---------------- CONFIG ADMIN ----------------
ADMIN_USER = "admin@gmail.com"
ADMIN_PASS = "123"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- CARDAPIO ----------------
@app.route("/cardapio")
def cardapio():
    produtos = Produto.query.order_by(Produto.categoria, Produto.subcategoria).all()
    categorias = {}
    for p in produtos:
        categorias.setdefault(p.categoria, {}).setdefault(p.subcategoria or "principal", []).append(p)
    return render_template("cardapio.html", categorias=categorias)

# ---------------- PROGRAMACAO ----------------
@app.route("/programacao")
def programacao():
    eventos = Programacao.query.all()
    return render_template("programacao.html", eventos=eventos)

# ---------------- PROMOCOES ----------------
@app.route("/promocoes")
def promocoes():
    promocoes = Promocao.query.all()
    return render_template("promocoes.html", promocoes=promocoes)

# ---------------- FINALIZAR PEDIDO ----------------
@app.route("/finalizar")
def finalizar():
    itens_json = request.args.get("itens", "[]")
    itens = json.loads(itens_json)
    return render_template("finalizar.html", itens=itens)

# ---------------- ENVIAR PEDIDO ----------------
@app.route("/pedido", methods=["POST"])
def enviar_pedido():
    dados = request.get_json()
    if not dados:
        return jsonify({"status": "erro", "mensagem": "Dados inválidos"}), 400

    novo_pedido = Pedido(
        cliente=dados["cliente"],
        mesa=dados["mesa"],
        comanda=dados["comanda"],
        status="solicitado",
        data=datetime.now()
    )
    db.session.add(novo_pedido)
    db.session.commit()

    for item in dados["itens"]:
        produto = Produto.query.get(item["id"])
        if produto:
            db.session.add(ItemPedido(
                pedido_id=novo_pedido.id,
                produto_id=produto.id,
                quantidade=item.get("quantidade", 1)
            ))
    db.session.commit()

    return jsonify({"status": "ok"})

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == ADMIN_USER and senha == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("adm"))
        erro = "Usuário ou senha incorretos"
    return render_template("login.html", erro=erro)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

# ---------------- DECORATOR PARA ADMIN ----------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ---------------- PAINEL ADMIN ----------------
@app.route("/adm")
@admin_required
def adm():
    return render_template("adm/painel.html")

# ---------------- ADMIN CARDAPIO ----------------
@app.route("/adm/cardapio", methods=["GET", "POST"])
@admin_required
def adm_cardapio():
    if request.method == "POST":
        novo = Produto(
            nome=request.form.get("nome"),
            descricao=request.form.get("descricao"),
            preco=float(request.form.get("preco")),
            categoria=request.form.get("categoria"),
            subcategoria=request.form.get("subcategoria"),
            disponivel=True
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("adm_cardapio"))
    itens = Produto.query.all()
    return render_template("adm/editar_cardapio.html", itens=itens)

# ---------------- ADMIN PROGRAMACAO ----------------
@app.route("/adm/programacao", methods=["GET", "POST"])
@admin_required
def adm_programacao():
    if request.method == "POST":
        novo = Programacao(
            dia=request.form.get("dia"),
            evento=request.form.get("evento")
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("adm_programacao"))
    eventos = Programacao.query.all()
    return render_template("adm/editar_programacao.html", eventos=eventos)

@app.route("/adm/programacao/deletar/<int:id>")
@admin_required
def deletar_programacao(id):
    evento = Programacao.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for("adm_programacao"))

# ---------------- ADMIN PROMOCOES ----------------
@app.route("/adm/promocoes", methods=["GET", "POST"])
@admin_required
def adm_promocoes():
    if request.method == "POST":
        promo = Promocao(
            produto_id=request.form.get("item_id"),
            preco_promocional=float(request.form.get("preco")),
            data_fim=datetime.strptime(request.form.get("data_fim"), "%Y-%m-%d")
        )
        db.session.add(promo)
        db.session.commit()
        return redirect(url_for("adm_promocoes"))
    promocoes = Promocao.query.all()
    itens = Produto.query.all()
    return render_template("adm/editar_promocoes.html", promocoes=promocoes, itens=itens)

# ---------------- PEDIDOS ADMIN ----------------
@app.route("/adm/pedidos")
@admin_required
def adm_pedidos():
    pedidos = Pedido.query.order_by(Pedido.data.desc()).all()
    return render_template("adm/pedidos.html", pedidos=pedidos)

# ---------------- ENTREGAR ----------------
@app.route("/adm/entregar/<int:id>")
@admin_required
def entregar(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.status = "entregue"
    db.session.commit()
    return redirect(url_for("adm_pedidos"))

# ---------------- CANCELAR ----------------
@app.route("/adm/cancelar/<int:id>", methods=["POST"])
@admin_required
def cancelar(id):
    pedido = Pedido.query.get_or_404(id)
    justificativa = request.form.get("justificativa")
    pedido.status = "cancelado"
    pedido.justificativa = justificativa
    db.session.commit()
    return redirect(url_for("adm_pedidos"))