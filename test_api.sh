#!/bin/bash

# Ensure the Flask app is running before executing this script.
# You can run it with: source venv/bin/activate && python app.py

echo "Sending POST request to Flask API..."

curl -X POST -H "Content-Type: application/json" -d '{
    "nomeEmpresa": "Minha Empresa Teste",
    "ramoEmpresa": "Tecnologia",
    "emailContato": "contato@minhaempresa.com",
    "telefone": "11999998888",
    "assunto": "Dúvida sobre projeto",
    "descricaoDetalhada": "Esta é uma descrição detalhada da dúvida para o projeto de teste.",
    "prazo": "30 dias"
}' http://127.0.0.1:5000/

echo -e "\nRequest sent. Check the Flask terminal for output."
