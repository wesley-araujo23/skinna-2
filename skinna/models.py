from skinna import db
from datetime import datetime


class Cardapio(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float)
    categoria = db.Column(db.String(50))

    imagem = db.Column(db.String(200))


class Programacao(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    dia = db.Column(db.String(50))
    evento = db.Column(db.String(200))

    imagem = db.Column(db.String(200))


class Promocao(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey("cardapio.id"))

    preco_promocional = db.Column(db.Float)

    data_fim = db.Column(db.DateTime)

    item = db.relationship("Cardapio")


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    usuario = db.Column(db.String(30), unique=True)

    email = db.Column(db.String(100), unique=True)

    senha = db.Column(db.String(60))