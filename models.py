from app import db
from sqlalchemy.dialects.postgresql import JSON

class Country_soccer(db.Model):
    __tablename__ = 'country_soccer'

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String())
    world_cup_wins = db.Column(db.Integer)
    match_wins = db.Column(db.Integer)
    match_ties = db.Column(db.Integer)
    match_losses = db.Column(db.Integer)
    tournament_appearances = db.Column(db.Integer)

    def __init__(self, country_name, world_cup_wins, match_wins, match_ties, match_losses, tournament_appearances):
        self.country_name = country_name
        self.world_cup_wins = world_cup_wins
        self.match_wins = match_wins
        self.match_ties = match_ties
        self.match_losses = match_losses
        self.tournament_appearances = tournament_appearances

    def __repr__(self):
        return '<id {}>'.format(self.id)