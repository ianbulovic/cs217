from fastapi import dependencies
from sqlalchemy.exc import IntegrityError
from webserver import db


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20))
    text = db.Column(db.String(100))

    def __repr__(self):
        return f"Entity('{self.id}', '{self.label}', '{self.text}')"

    @classmethod
    def add_entity(cls, label, text):
        try:
            new_entity = cls(label=label, text=text)
            db.session.add(new_entity)
            db.session.commit()
            return new_entity
        except IntegrityError as e:
            db.session.rollback()
            raise e


class Dependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.String(100))
    rel = db.Column(db.String(100))
    child = db.Column(db.String(100))
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"))
    entity = db.relationship("Entity", backref=db.backref("dependencies", lazy=True))

    def __repr__(self):
        return f"Dependency('{self.id}', '{self.parent}', '{self.rel}', '{self.child}')"

    @classmethod
    def add_dependency(cls, parent, rel, child, entity_id):
        try:
            new_dependency = cls(
                parent=parent, rel=rel, child=child, entity_id=entity_id
            )
            db.session.add(new_dependency)
            db.session.commit()
            return new_dependency
        except IntegrityError as e:
            db.session.rollback()
            raise e
