from src import db, bcrypt

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.email})>"

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(user_data: dict) -> "User":
        new_user = User(
            email=user_data["email"],
            is_admin=user_data.get("is_admin", False)
        )
        new_user.set_password(user_data["password"])
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get(user_id: str) -> "User | None":
        return User.query.get(user_id)

    def update(self, data: dict) -> None:
        if "email" in data:
            self.email = data["email"]
        if "password" in data:
            self.set_password(data["password"])
        if "is_admin" in data:
            self.is_admin = data["is_admin"]
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all() -> list["User"]:
        return User.query.all()
