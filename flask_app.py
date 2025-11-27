from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from data.database import db

load_dotenv()
from models.orcamento import Orcamento
from email_module import send_budget_email
from push_notifications import save_subscription, send_notification_to_all
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/orcamento.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/save-subscription', methods=['POST'])
def save_push_subscription():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    subscription_data = request.get_json()
    save_subscription(subscription_data)
    
    return jsonify({"msg": "Subscription saved."}), 201

@app.route('/api/orcamento', methods=['POST'])
def create_orcamento():
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
    
    # Envia notificação push para todos os inscritos
    push_message = {
        "title": "Novo Pedido de Orçamento!",
        "body": f"Um novo orçamento de {data.get('nomeEmpresa')} foi solicitado."
    }
    
    send_notification_to_all(json.dumps(push_message))

    return jsonify({"msg": "Orçamento recebido e salvo com sucesso!"}), 201

@app.route('/orcamentos', methods=['GET'])
def get_orcamentos():
    orcamentos = Orcamento.query.all()
    return render_template('index.html', orcamentos=orcamentos)

@app.route('/orcamento/confirmar/<int:id>', methods=['POST'])
def confirmar_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    prazo_str = request.form.get('prazo')
    
    if prazo_str:
        # Converte a data de YYYY-MM-DD para um objeto datetime
        date_obj = datetime.strptime(prazo_str, '%Y-%m-%d')
        # Formata o objeto datetime para DD/MM/YYYY
        formatted_prazo = date_obj.strftime('%d/%m/%Y')
        
        orcamento.prazo = formatted_prazo
        orcamento.confirmado = True
        db.session.commit()
    
    return redirect(url_for('get_orcamentos'))

if __name__ == '__main__':
    app.run(debug=True)