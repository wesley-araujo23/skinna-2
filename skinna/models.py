from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=True)        # cervejas, drinks, doses, combos, porcoes, nao_alcoolico
    subcategoria = db.Column(db.String(50), nullable=True)     # litrão, long neck, baldes, chopp, combos, garrafas, acompanhamentos
    imagem = db.Column(db.String(200), nullable=True)
    disponivel = db.Column(db.Boolean, default=True)


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    mesa = db.Column(db.String(10), nullable=False)
    comanda = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default="solicitado")  # solicitado, entregue, cancelado
    justificativa = db.Column(db.String(200), nullable=True)  # pode ficar vazio se não for cancelado
    data = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)


class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)

    produto = db.relationship("Produto", backref="itens_pedido")


class Programacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(50), nullable=False)
    evento = db.Column(db.String(200), nullable=False)
    imagem = db.Column(db.String(200), nullable=True)


class Promocao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    preco_promocional = db.Column(db.Float, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    
    produto = db.relationship("Produto", backref="promocoes")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)