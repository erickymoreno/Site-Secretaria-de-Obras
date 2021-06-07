from src import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    __tablename__ ="usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    data_de_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(255), nullable=False)

    def _repr_(self):
        return "<Usuario %d>" % self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome


class OrdemDeServico(db.Model):
    __tablename__ ="ordem_de_serviço"
    id = db.Column(db.Integer, primary_key = True)
    data_solicitacao = db.Column(db.Date, nullable=False)
    data_conclusao = db.Column(db.Date, nullable=True)
    descricao = db.Column(db.String(511), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    tipo_de_servico_id = db.Column(db.Integer, db.ForeignKey("tipo_de_servico.id"))
    status = db.Column(db.Integer, db.ForeignKey("status.id"))

    def _repr_(self):
        return "<OrdemDeServico %d>" % self.id


class TipoDeServico(db.Model):
    __tablename__="tipo_de_servico"
    id = db.Column(db.Integer, primary_key=True)
    nome_servico = db.Column(db.String(255), nullable=False)

    def _repr_(self):
        return "<TipoDeServico %d>" % self.id

class Endereco(db.Model):
    __tablename__ ="endereco"
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(11), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(11), nullable=False)
    referencia = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    def _repr_(self):
        return "<Endereco %d>" % self.id

class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(55), nullable=False)

    def _repr_(self):
        return "<Status %d>" % self.id