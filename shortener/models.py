from . import db


class UrlsModel(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(200), nullable=True)
    original_url = db.Column(db.String(200), nullable=False)
    redirects = db.Column(db.Integer, nullable=False, default=0)
