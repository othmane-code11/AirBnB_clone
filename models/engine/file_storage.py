#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State


class FileStorage:
    """FileStorage Class.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def new(self, obj):
        """Sets in __objects the  obj with key <obj_class_name>.id"""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        all_objcts = FileStorage.__objects
        obj_dict = {}
        for obj in all_objcts.keys():
            obj_dict[obj] = all_objcts[obj].to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as fl:
            json.dump(obj_dict, fl)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects if it exists"""
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                try:
                    obj_dict = json.load(f)
                    for key, val in obj_dict.items():
                        cls_name, obj_id = key.split('.')
                        cls = eval(cls_name)
                        ins = cls(**val)
                        FileStorage.__objects[key] = ins
                except Exception:
                    pass
