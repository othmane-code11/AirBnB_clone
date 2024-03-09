#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Represents the BaseModel class."""
    def __init__(self, *args, **kwargs):
        """Initialize a new  BaseModel

        Args:
            *args.
            **kwargs (dict): Key/value pairs of attributes
        """
        tim_frmat = "%Y-%m-%dT%H:%M:%S.%f"
        # have a unique id for each BaseModel
        self.id = str(uuid.uuid4())
        # assign the current datetime when an instance is created
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs is not None and len(kwargs) > 0:
            for key, val in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(val, tim_frmat))
                else:
                    setattr(self, key, val)
        models.storage.new(self)

    def save(self):
        """Update the pub inst attr updated_at with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Containing all key/value pair __class__ representing
        the class name of the object.
        """
        ins_dict = self.__dict__.copy()
        ins_dict["__class__"] = self.__class__.__name__
        ins_dict["created_at"] = self.created_at.isoformat()
        ins_dict["updated_at"] = self.updated_at.isoformat()
        return ins_dict

    def __str__(self):
        """return the print/str representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
