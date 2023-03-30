from .. import db

class Profile(db.Model):
    """ Profile Model for storing profile related details """
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False) 
    last_name = db.Column(db.String(100), nullable=False)
    friendly_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    date_of_birth = db.Column(db.String(25), nullable=False)
    skillset_id = db.Column(db.Integer, db.ForeignKey('skillset.id'))
    gender = db.Column(db.String(10), nullable=True)

    # Relationships
    account = db.relationship('Account', foreign_keys=[account_id])
    skillset = db.relationship('Skillset', foreign_keys=[skillset_id])

    def __repr__(self) -> str:
        return "<Profile '{}'>".format(self.friendly_name)
    
class Skillset(db.Model):
    """ Skillset Model for storing skillset related details """
    __tablename__ = "skillset"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Skillset '{}'>".format(self.name)

class BartleQuotient(db.Model):
    """ BartleQuotient Model for storing bartle test related details """
    __tablename__ = "bartlequotient"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    achiever_pct = db.Column(db.Double, nullable=False) 
    explorer_pct = db.Column(db.Double, nullable=False) 
    killer_pct = db.Column(db.Double, nullable=False) 
    socializer_pct = db.Column(db.Double, nullable=False) 

    #Relationships
    profile = db.relationship('Profile', foreign_keys=[profile_id])
    
    def __repr__(self):
        return "<BartleQuotient '{}'>".format(self.id)