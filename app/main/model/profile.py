from .. import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

class FriendshipInvitations(db.Model):
    """ FriendshipInvitations Model """
    __tablename__ = "friendshipinvitations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id=db.Column(db.Integer,  nullable=False)
    account_id_to = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime(timezone=True),  server_default=func.now())

    def __repr__(self):
        return "<FriendshipInvitations '{}'>".format(self.id)

class Friends(db.Model):
    """ Friends Model """
    __tablename__ = "friends"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    friends_profile_id = db.Column(db.Integer, nullable=True)

    profiles = relationship('Profile', secondary = 'profilefriendship')   

    def __repr__(self):
        return "<Friends '{}'>".format(self.name)
    
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
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    account = db.relationship('Account', foreign_keys=[account_id])
    skillset = db.relationship('Skillset', foreign_keys=[skillset_id])
  
    friends = relationship('Friends', secondary = 'profilefriendship')
    groups = db.relationship('Group', secondary='profilegroup')
    
    def __repr__(self) -> str:
        return "<Profile '{}'>".format(self.friendly_name)

class ProfileFriendship(db.Model):
    """ ProfileFriendship Model """
    __tablename__ = "profilefriendship"

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('friends.id'), primary_key=True)  

    def __repr__(self):
        return "<ProfileFriendship '{}'>".format(self.friend_id)
    
class Group(db.Model):
    """ Group Model """
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False) 
    description = db.Column(db.String(255), nullable=True)
    account_id  = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(db.DateTime(timezone=True), onupdate=func.now())
 
    profiles = relationship('Profile', secondary = 'profilegroup') 
    #groups = db.relationship('ProfileGroup', backref = backref('group', order_by = id), primaryjoin = "Group.id == ProfileGroup.group_id")  

    def __repr__(self):
        return "<Group '{}'>".format(self.name)
              
class ProfileGroup(db.Model):
    """ ProfileGroup Model """
    __tablename__ = "profilegroup"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id=db.Column(db.Integer, db.ForeignKey('profile.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    is_accepted = db.Column(db.Boolean)

    def __repr__(self):
        return "<ProfileGroup '{}'>".format(self.__tablename__)

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

