#!/usr/bin/python3
"""Module test_file_storage

This Module contains a tests for FileStorage Class
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.review import Review


class TestFileStorage_methods(unittest.TestCase):
    """Testing methods of the FileStorage class."""
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmpt.json")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmpt.json", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_new(self):
        my_bm = BaseModel()
        my_amnt = Amenity()
        my_rvw = Review()
        my_plc = Place()
        my_cty = City()
        my_usr = User()
        my_stt = State()

        models.storage.new(my_bm)
        models.storage.new(my_cty)
        models.storage.new(my_stt)
        models.storage.new(my_usr)
        models.storage.new(my_plc)
        models.storage.new(my_rvw)
        models.storage.new(my_amnt)

        self.assertIn("BaseModel." + my_bm.id, models.storage.all().keys())
        self.assertIn(my_bm, models.storage.all().values())
        self.assertIn("User." + my_usr.id, models.storage.all().keys())
        self.assertIn(my_usr, models.storage.all().values())
        self.assertIn("Place." + my_plc.id, models.storage.all().keys())
        self.assertIn(my_plc, models.storage.all().values())
        self.assertIn("Amenity." + my_amnt.id, models.storage.all().keys())
        self.assertIn(my_amnt, models.storage.all().values())
        self.assertIn("State." + my_stt.id, models.storage.all().keys())
        self.assertIn(my_stt, models.storage.all().values())
        self.assertIn("Review." + my_rvw.id, models.storage.all().keys())
        self.assertIn(my_rvw, models.storage.all().values())
        self.assertIn("City." + my_cty.id, models.storage.all().keys())
        self.assertIn(my_cty, models.storage.all().values())

    def test_new_with_argss(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_wth_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_wth_args(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_save(self):
        my_bm = BaseModel()
        my_amnt = Amenity()
        my_rvw = Review()
        my_plc = Place()
        my_cty = City()
        my_usr = User()
        my_stt = State()

        models.storage.new(my_bm)
        models.storage.new(my_usr)
        models.storage.new(my_stt)
        models.storage.new(my_plc)
        models.storage.new(my_cty)
        models.storage.new(my_amnt)
        models.storage.new(my_rvw)
        models.storage.save()

        save_text = ""
        with open("file.json", "r") as fl:
            save_text = fl.read()
            self.assertIn("BaseModel." + my_bm.id, save_text)
            self.assertIn("User." + my_usr.id, save_text)
            self.assertIn("Review." + my_rvw.id, save_text)
            self.assertIn("Place." + my_plc.id, save_text)
            self.assertIn("Amenity." + my_amnt.id, save_text)
            self.assertIn("State." + my_stt.id, save_text)
            self.assertIn("City." + my_cty.id, save_text)

    def test_save_wth_args(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        my_bm = BaseModel()
        my_amnt = Amenity()
        my_rvw = Review()
        my_plc = Place()
        my_cty = City()
        my_usr = User()
        my_stt = State()

        models.storage.new(my_bm)
        models.storage.new(my_usr)
        models.storage.new(my_stt)
        models.storage.new(my_plc)
        models.storage.new(my_cty)
        models.storage.new(my_amnt)
        models.storage.new(my_rvw)
        models.storage.save()
        models.storage.reload()
        objcs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + my_bm.id, objcs)
        self.assertIn("User." + my_usr.id, objcs)
        self.assertIn("Place." + my_plc.id, objcs)
        self.assertIn("Amenity." + my_amnt.id, objcs)
        self.assertIn("Review." + my_rvw.id, objcs)
        self.assertIn("City." + my_cty.id, objcs)
        self.assertIn("State." + my_stt.id, objcs)

    def test_reload_wth_args(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


class TestFileStorage_inst(unittest.TestCase):
    """Testing instantiation of the FileStorage class."""

    def test_FileStorage_file_path_is_privatee_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_FileStorage_instantiation_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_storage_initialize(self):
        self.assertEqual(type(models.storage), FileStorage)

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))


if __name__ == "__main__":
    unittest.main()
