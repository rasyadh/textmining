import datetime
from project.core import db
from project import app

class Artikel(db.Model):
    __tablename__ = 'artikel'

    id_artikel = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    judul = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    isi = db.Column(db.String, nullable=False)
    isMining = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<Artikel: {}>".format(self.judul)

class Keyword(db.Model):
    __tablename__ = 'keyword'

    id_key = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    judul = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    isi = db.Column(db.String, nullable=False)
    keyword = db.Column(db.String(20), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Keyword: {}>".format(self.judul)