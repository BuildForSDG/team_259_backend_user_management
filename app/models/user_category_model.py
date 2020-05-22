from datetime import datetime

from marshmallow import Schema, fields

from . import db, ma
from user_model import User
from category_model import Category

class UserCategory(db.Model):
    __tablename__ = 'user_categories'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("user_categories", single_parent=True, lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref("user_categories", single_parent=True, lazy=True))

    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    def insert_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def fetch_all(cls):
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_by_id(cls, id):
        return cls.query.get(id)

    @classmethod  
    def update(cls, id, user_id=None, category_id=None):
        record = cls.fetch_by_id(id)
        if user_id:
            record.user_id = user_id
        if category_id:
            record.category_id = category_id
        db.session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        record = cls.fetch_by_id(id)
        record.delete()
        db.session.commit()
        return True

class UserCategorySchema(ma.ModelSchema):
    class Meta:
        model = UserCategory