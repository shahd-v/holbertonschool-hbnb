import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @classmethod
    def _store(cls):
        """Each concrete class gets its own list of instances."""
        if "_instances" not in cls.__dict__:
            cls._instances = []
        return cls._instances

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
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
