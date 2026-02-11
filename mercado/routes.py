from mercado import app
from flask import render_template
from mercado.models import Item

@app.route('/')
def page_home():
    return render_template("home.html")

@app.route('/produtos')
def page_produto():
    itens=Item.query.all()

    return render_template("produtos.html", itens = itens)