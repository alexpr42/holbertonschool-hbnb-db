from src.models.user import User
from src import db

class DataManager:
    def __init__(self):
        self.repo = None  # Initialize with appropriate repository based on configuration

    def reload(self) -> None:
        """Reload data to the repository"""
        pass

    def get_all(self, model_name: str) -> list:
        """Get all objects of a model"""
        if model_name == "User":
            return User.query.all()
        # Handle other models as needed

    def get(self, model_name: str, id: str) -> None:
        """Get an object by id"""
        if model_name == "User":
            return User.query.get(id)
        # Handle other models as needed

    def save(self, obj) -> None:
        """Save an object"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj) -> None:
        """Update an object"""
        db.session.commit()

    def delete(self, obj) -> bool:
        """Delete an object"""
        db.session.delete(obj)
        db.session.commit()
