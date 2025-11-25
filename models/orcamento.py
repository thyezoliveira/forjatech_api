from database import db

class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomeEmpresa = db.Column(db.String(100), nullable=False)
    ramoEmpresa = db.Column(db.String(100), nullable=False)
    emailContato = db.Column(db.String(100), nullable=False)
    assunto = db.Column(db.String(100), nullable=False)
    descricaoDetalhada = db.Column(db.Text, nullable=False)
    confirmado = db.Column(db.Boolean, default=False, nullable=False)
    prazo = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Orcamento {self.id}>"
