from sqlalchemy.orm import sessionmaker
from src.models.base import Base

Session = sessionmaker()

class DBRepository:
    """Database Repository"""

    def __init__(self, db=None):
        """Initialize with a SQLAlchemy database session"""
        if db:
            Session.configure(bind=db.engine)
            self.session = Session()

    def get_all(self, model_name):
        """Get all objects of a given model"""
        return self.session.query(model_name).all()

    def get(self, model_name, obj_id):
        """Get an object by its ID"""
        return self.session.query(model_name).filter_by(id=obj_id).first()

    def save(self, obj):
        """Save an object to the database"""
        self.session.add(obj)
        self.session.commit()

    def update(self, obj):
        """Update an object in the database"""
        self.session.commit()
        return obj

    def delete(self, obj):
        """Delete an object from the database"""
        self.session.delete(obj)
        self.session.commit()
