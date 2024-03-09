#!/usr/bin/python3
"""
Module for Amenity class unittest
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.amenity import Amenity


class TestAmenity_inst(unittest.TestCase):
    """Unittests for testing instantiation  of  Amenity class."""
    def setUp(self):
        try:
            os.rename("file.json", "tmpt.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmpt.json", "file.json")
        except FileNotFoundError:
            pass

    def test_no_args_insts(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_inst_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_created_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_id_is_a_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_name_is_a_public_class_attribute(self):
        amenity_num1 = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenity_num1.__dict__)

    def test_two_amenities_unique_ids(self):
        amenity_num1 = Amenity()
        amenity_num2 = Amenity()
        self.assertNotEqual(amenity_num1.id, amenity_num2.id)

    def test_two_amenities_different_created_at(self):
        amenity_num1 = Amenity()
        sleep(0.05)
        amenity_num2 = Amenity()
        self.assertLess(amenity_num1.created_at, amenity_num2.created_at)

    def test_two_amenities_different_updated_at(self):
        amenity_num1 = Amenity()
        sleep(0.05)
        amenity_num2 = Amenity()
        self.assertLess(amenity_num1.updated_at, amenity_num2.updated_at)

    def test_str_representation(self):
        ma_date = datetime.today()
        ma_date_repr = repr(ma_date)
        amenity_num1 = Amenity()
        amenity_num1.id = "291102"
        amenity_num1.created_at = amenity_num1.updated_at = ma_date
        amenity_s = amenity_num1.__str__()
        self.assertIn("[Amenity] (291102)", amenity_s)
        self.assertIn("'id': '291102'", amenity_s)
        self.assertIn("'created_at': " + ma_date_repr, amenity_s)
        self.assertIn("'updated_at': " + ma_date_repr, amenity_s)

    def test_arg_unused(self):
        amenity_num1 = Amenity(None)
        self.assertNotIn(None, amenity_num1.__dict__.values())

    def test_inst_with_kwargs(self):
        """instantiation with kwargs test method."""
        ma_date = datetime.today()
        ma_date_iso = ma_date.isoformat()
        a_1 = Amenity(id="100", created_at=ma_date_iso, updated_at=ma_date_iso)
        self.assertEqual(a_1.id, "100")
        self.assertEqual(a_1.created_at, ma_date)
        self.assertEqual(a_1.updated_at, ma_date)

    def test_inst_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for save method of the Amenity class."""
    def setUp(self):
        try:
            os.rename("file.json", "tmpt.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmpt.json", "file.json")
        except FileNotFoundError:
            pass

    def test_one_save(self):
        amenity_num1 = Amenity()
        sleep(0.05)
        first_updated_at = amenity_num1.updated_at
        amenity_num1.save()
        self.assertLess(first_updated_at, amenity_num1.updated_at)

    def test_two_saves(self):
        amenity_num1 = Amenity()
        sleep(0.05)
        first_updated_at = amenity_num1.updated_at
        amenity_num1.save()
        second_updated_at = amenity_num1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity_num1.save()
        self.assertLess(second_updated_at, amenity_num1.updated_at)

    def test_save_with_arg(self):
        amenity_num1 = Amenity()
        with self.assertRaises(TypeError):
            amenity_num1.save(None)

    def test_save_updates_file(self):
        amenity_num1 = Amenity()
        amenity_num1.save()
        am_id = "Amenity." + amenity_num1.id
        with open("file.json", "r") as fl:
            self.assertIn(am_id, fl.read())


class TestAmenity_to_dict(unittest.TestCase):
    """
    Unittests for to_dict method  of Amenity class.
    """
    def setUp(self):
        try:
            os.rename("file.json", "tmpt.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmpt.json", "file.json")
        except FileNotFoundError:
            pass

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amenity_num1 = Amenity()
        self.assertIn("id", amenity_num1.to_dict())
        self.assertIn("created_at", amenity_num1.to_dict())
        self.assertIn("updated_at", amenity_num1.to_dict())
        self.assertIn("__class__", amenity_num1.to_dict())

    def test_to_dict_contains_added_atts(self):
        amenity_num1 = Amenity()
        amenity_num1.middle_name = "Othmane"
        amenity_num1.my_number = 777
        self.assertEqual("Othmane", amenity_num1.middle_name)
        self.assertIn("my_number", amenity_num1.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amenity_num1 = Amenity()
        amenity_dict = amenity_num1.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        ma_date = datetime.today()
        amenity_num1 = Amenity()
        amenity_num1.id = "291102"
        amenity_num1.created_at = amenity_num1.updated_at = ma_date
        to_dict = {
            'id': '291102',
            '__class__': 'Amenity',
            'created_at': ma_date.isoformat(),
            'updated_at': ma_date.isoformat(),
        }
        self.assertDictEqual(amenity_num1.to_dict(), to_dict)

    def test_to_dict_with_arg(self):
        amenity_num1 = Amenity()
        with self.assertRaises(TypeError):
            amenity_num1.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        amenity_num1 = Amenity()
        self.assertNotEqual(amenity_num1.to_dict(), amenity_num1.__dict__)


if __name__ == "__main__":
    unittest.main()
