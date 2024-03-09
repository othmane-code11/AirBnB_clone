#!/usr/bin/python3
"""
Module for the Place class unittest.
"""

import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.place import Place


class TestPlace_inst(unittest.TestCase):
    """
    Unittests for testing instantiation  of  Place class.
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

    def test_no_arg_insts(self):
        self.assertEqual(Place, type(Place()))

    def test_id_is_a_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_new_inst_stored_in_objs(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_created_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(ma_place))
        self.assertNotIn("city_id", ma_place.__dict__)

    def test_user_id_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(ma_place))
        self.assertNotIn("user_id", ma_place.__dict__)

    def test_name_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(ma_place))
        self.assertNotIn("name", ma_place.__dict__)

    def test_number_rooms_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(ma_place))
        self.assertNotIn("number_rooms", ma_place.__dict__)

    def test_description_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(ma_place))
        self.assertNotIn("desctiption", ma_place.__dict__)

    def test_number_bathrooms_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(ma_place))
        self.assertNotIn("number_bathrooms", ma_place.__dict__)

    def test_price_by_night_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(ma_place))
        self.assertNotIn("price_by_night", ma_place.__dict__)

    def test_max_guest_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(ma_place))
        self.assertNotIn("max_guest", ma_place.__dict__)

    def test_longitude_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(ma_place))
        self.assertNotIn("longitude", ma_place.__dict__)

    def test_amenity_ids_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(ma_place))
        self.assertNotIn("amenity_ids", ma_place.__dict__)

    def test_latitude_is_a_public_class_attribute(self):
        ma_place = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(ma_place))
        self.assertNotIn("latitude", ma_place.__dict__)

    def test_two_places_unique_ids(self):
        ma_place1 = Place()
        ma_place2 = Place()
        self.assertNotEqual(ma_place1.id, ma_place2.id)

    def test_two_places_different_created_at(self):
        ma_place1 = Place()
        sleep(0.05)
        ma_place2 = Place()
        self.assertLess(ma_place1.created_at, ma_place2.created_at)

    def test_two_places_different_updated_at(self):
        ma_place1 = Place()
        sleep(0.05)
        ma_place2 = Place()
        self.assertLess(ma_place1.updated_at, ma_place2.updated_at)

    def test_str_repr(self):
        ma_date = datetime.today()
        ma_date_repr = repr(ma_date)
        ma_place = Place()
        ma_place.id = "291102"
        ma_place.created_at = ma_place.updated_at = ma_date
        ma_place_str = ma_place.__str__()
        self.assertIn("[Place] (291102)", ma_place_str)
        self.assertIn("'id': '291102'", ma_place_str)
        self.assertIn("'created_at': " + ma_date_repr, ma_place_str)
        self.assertIn("'updated_at': " + ma_date_repr, ma_place_str)

    def test_arg_unused(self):
        ma_place = Place(None)
        self.assertNotIn(None, ma_place.__dict__.values())

    def test_inst_with_kwargs(self):
        ma_date = datetime.today()
        ma_date_iso = ma_date.isoformat()
        plce = Place(id="123", created_at=ma_date_iso, updated_at=ma_date_iso)
        self.assertEqual(plce.id, "123")
        self.assertEqual(plce.created_at, ma_date)
        self.assertEqual(plce.updated_at, ma_date)

    def test_inst_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """
    Unittests for testing save  method of Place class.
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

    def test_one_save(self):
        ma_place = Place()
        sleep(0.05)
        first_updated_at = ma_place.updated_at
        ma_place.save()
        self.assertLess(first_updated_at, ma_place.updated_at)

    def test_two_saves(self):
        ma_place = Place()
        sleep(0.05)
        first_updated_at = ma_place.updated_at
        ma_place.save()
        second_updated_at = ma_place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ma_place.save()
        self.assertLess(second_updated_at, ma_place.updated_at)

    def test_save_with_args(self):
        ma_place = Place()
        with self.assertRaises(TypeError):
            ma_place.save(None)

    def test_save_updates_file(self):
        ma_place = Place()
        ma_place.save()
        ma_place_id = "Place." + ma_place.id
        with open("file.json", "r") as fl:
            self.assertIn(ma_place_id, fl.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing  to_dict method of Place class."""

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
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ma_place = Place()
        self.assertIn("id", ma_place.to_dict())
        self.assertIn("created_at", ma_place.to_dict())
        self.assertIn("updated_at", ma_place.to_dict())
        self.assertIn("__class__", ma_place.to_dict())

    def test_to_dict_contains_added_attributes(self):
        ma_place = Place()
        ma_place.middle_name = "Othmane"
        ma_place.my_number = 777
        self.assertEqual("Othmane", ma_place.middle_name)
        self.assertIn("my_number", ma_place.to_dict())

    def test_to_dict_datetime_attrs_are_strs(self):
        ma_place = Place()
        ma_place_dict = ma_place.to_dict()
        self.assertEqual(str, type(ma_place_dict["id"]))
        self.assertEqual(str, type(ma_place_dict["created_at"]))
        self.assertEqual(str, type(ma_place_dict["updated_at"]))

    def test_to_dict_output(self):
        ma_date = datetime.today()
        ma_place = Place()
        ma_place.id = "291102"
        ma_place.created_at = ma_place.updated_at = ma_date
        to_dict = {
            'id': '291102',
            '__class__': 'Place',
            'created_at': ma_date.isoformat(),
            'updated_at': ma_date.isoformat(),
        }
        self.assertDictEqual(ma_place.to_dict(), to_dict)

    def test_to_dict_with_args(self):
        ma_place = Place()
        with self.assertRaises(TypeError):
            ma_place.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        ma_place = Place()
        self.assertNotEqual(ma_place.to_dict(), ma_place.__dict__)


if __name__ == "__main__":
    unittest.main()
