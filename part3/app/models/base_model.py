import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def _store(cls):
        """Each concrete class gets its own list of instances."""
        if "_instances" not in cls.__dict__:
            cls._instances = []
        return cls._instances

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """Update attributes from a dictionary, then refresh updated_at."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def delete(self):
        """Remove this object from its class store."""
        store = type(self)._store()
        if self in store:
            store.remove(self)
