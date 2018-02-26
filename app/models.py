from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from flask_login import UserMixin

Base = declarative_base()

from app import db


class SerializerMixin:
    """Provide dict-like interface to db.Model subclasses."""

    def __getitem__(self, key):
        """Expose object attributes like dict values."""
        return getattr(self, key)

    def keys(self):
        """Identify what db columns we have."""
        return inspect(self).attrs.keys()


class CreatedUpdatedMixin(object):
    created = db.Column(db.DateTime, server_default=db.func.now(), index=True)
    updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), index=True)


class User(db.Model, UserMixin, CreatedUpdatedMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(32), db.ForeignKey('roles.title', ondelete='cascade'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def check_role(self):
        return self.roles.id


class Role(db.Model, CreatedUpdatedMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(32), nullable=False, unique=True)

    # Relationships
    roles = db.relationship('User', backref='roles')


class Invites(db.Model, CreatedUpdatedMixin):
    __tablename__ = "invites"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    invite_code = db.Column(db.String(36), nullable=False, unique=True)
    created_by = db.Column(db.String(32), db.ForeignKey('users.username', ondelete='cascade'), nullable=False)
    active = db.Column(db.Boolean, default=True)


class Nodes(db.Model, CreatedUpdatedMixin):
    __tablename__ = "nodes"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    unique_id = db.Column(db.String(32), nullable=False, unique=True)
    api_key = db.Column(db.String(40), nullable=True, unique=True)
    owner = db.Column(db.String(32), db.ForeignKey('users.username', ondelete='cascade'), nullable=False)
    active = db.Column(db.Boolean, default=True)
