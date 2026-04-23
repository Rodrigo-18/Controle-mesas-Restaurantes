from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Estrutura para armazenar pedidos por mesa
mesas = {i: [] for i in range(1, 31)}

# 🔹 Página inicial (SEM total agora)
@app.route('/')
def index():
    return render_template('index.html', mesas=mesas)

# 🔹 Adicionar item
@app.route('/add', methods=['POST'])
def add_item():
    mesa = int(request.form['mesa'])
    nome = request.form['nome']
    valor = float(request.form['valor'])

    mesas[mesa].append({
        'nome': nome,
        'valor': valor
    })

    return redirect(url_for('index'))

# 🔹 Nova página para ver detalhes da mesa
@app.route('/mesa/<int:mesa>')
def ver_mesa(mesa):
    itens = mesas[mesa]
    total = sum(item['valor'] for item in itens)
    return render_template('mesa.html', mesa=mesa, itens=itens, total=total)

# 🔹 Limpar mesa
@app.route('/limpar/<int:mesa>')
def limpar_mesa(mesa):
    mesas[mesa] = []
    return redirect(url_for('index'))

@app.route('/remover/<int:mesa>/<int:index>')
def remover_item(mesa, index):
    if 0 <= index < len(mesas[mesa]):
        mesas[mesa].pop(index)
    return redirect(url_for('ver_mesa', mesa=mesa))

@app.route('/fechar/<int:mesa>')
def fechar_conta(mesa):
    itens = mesas[mesa]
    total = sum(item['valor'] for item in itens)

    # copia os dados antes de limpar
    resumo = itens.copy()

    # limpa a mesa
    mesas[mesa] = []

    return render_template('fechar.html', mesa=mesa, itens=resumo, total=total)

# 🔹 Rodar servidor
if __name__ == '__main__':
    app.run(debug=True)