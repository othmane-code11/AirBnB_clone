#!/usr/bin/python3
"""Module test_base_model

Contains a tests for Base Class
"""
import os
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test instantiation of the BaseModel class."""

    def setUp(self):
        """
        setup for temporary filepath
        """
        try:
            os.rename("file.json", "tmpt.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        """
        Tear down for temporary file path
        """
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmpt.json", "file.json")
        except FileNotFoundError:
            pass

    def test_init(self):
        my_modl = BaseModel()
        self.assertIsNotNone(my_modl.id)
        self.assertIsNotNone(my_modl.updated_at)
        self.assertIsNotNone(my_modl.created_at)

    def test_save_mtd(self):
        """test the save mthd"""
        my_modl = BaseModel()

        ini_tial_update_at = my_modl.updated_at
        the_current_updated_at = my_modl.save()
        self.assertNotEqual(ini_tial_update_at, the_current_updated_at)

    def test_to_dict_mtd(self):
        """test for to_dict mthd"""
        modl = BaseModel()

        modl_dict = modl.to_dict()
        self.assertIsInstance(modl_dict, dict)
        self.assertEqual(modl_dict["__class__"], 'BaseModel')
        self.assertEqual(modl_dict["id"], modl.id)
        self.assertEqual(modl_dict["updated_at"], modl.updated_at.isoformat())
        self.assertEqual(modl_dict["created_at"], modl.created_at.isoformat())
        self.assertEqual(str, type(modl_dict["created_at"]))
        self.assertEqual(str, type(modl_dict["updated_at"]))

    def test_str_mtd(self):
        """test the str mthd"""
        my_modl = BaseModel()
        self.assertIn(my_modl.id, str(my_modl))
        self.assertIn(str(my_modl.__dict__), str(my_modl))
        self.assertTrue(str(my_modl).startswith('[BaseModel]'))


if __name__ == "__main__":
    unittest.main()
