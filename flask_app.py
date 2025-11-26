

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from data.database import db
from models.orcamento import Orcamento
from email_module import send_budget_email
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/orcamento.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST'])
def handle_form():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    
    new_orcamento = Orcamento(
        nomeEmpresa=data.get('nomeEmpresa'),
        ramoEmpresa=data.get('ramoEmpresa'),
        emailContato=data.get('emailContato'),
        telefone=data.get('telefone'),
        assunto=data.get('assunto'),
        descricaoDetalhada=data.get('descricaoDetalhada')
    )
    
    db.session.add(new_orcamento)
    db.session.commit()

    send_budget_email(new_orcamento)

    return jsonify({"msg": "Orçamento recebido e salvo com sucesso!"}), 201

@app.route('/orcamentos', methods=['GET'])
def get_orcamentos():
    orcamentos = Orcamento.query.all()
    return render_template('index.html', orcamentos=orcamentos)

if __name__ == '__main__':
    app.run(debug=True)