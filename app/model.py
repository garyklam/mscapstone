from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class dbModel(db.Model):
    __tablename__ = 'my_table'

    Species = db.Column(db.String)
    Cap = db.Column(db.String)
    Gills = db.Column(db.String)
    Stem = db.Column(db.String)
    Spores = db.Column(db.String)
    SporePrint = db.Column(db.String)
    OdorTaste = db.Column(db.String)
    Habitat = db.Column(db.String)
    Season = db.Column(db.String)
    SimilarSpecies = db.Column(db.String)
    Id = db.Column(db.Integer, primary_key=True)

