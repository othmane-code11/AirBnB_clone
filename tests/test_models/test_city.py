#!/usr/bin/python3
"""
Module for City unittest
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """
    Unittests for instantiation of the City class.
    """
    def test_no_arg_inst(self):
        self.assertEqual(City, type(City()))

    def test_new_inst_stored_in_objs(self):
        self.assertIn(City(), models.storage.all().values())

    def test_created_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_id_is_a_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_state_id_is_a_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_name_is_a_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def test_two_cities_unique_ids(self):
        city_num1 = City()
        city_num2 = City()
        self.assertNotEqual(city_num1.id, city_num2.id)

    def test_two_cities_different_created_at(self):
        city_num1 = City()
        sleep(0.05)
        city_num2 = City()
        self.assertLess(city_num1.created_at, city_num2.created_at)

    def test_two_cities_different_updated_at(self):
        city_num1 = City()
        sleep(0.05)
        city_num2 = City()
        self.assertLess(city_num1.updated_at, city_num2.updated_at)

    def test_str_repr(self):
        ma_date = datetime.today()
        ma_date_repr = repr(ma_date)
        city = City()
        city.id = "291102"
        city.created_at = city.updated_at = ma_date
        city_str = city.__str__()
        self.assertIn("[City] (291102)", city_str)
        self.assertIn("'id': '291102'", city_str)
        self.assertIn("'created_at': " + ma_date_repr, city_str)
        self.assertIn("'updated_at': " + ma_date_repr, city_str)

    def test_arg_unused(self):
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_inst_with_kwargs(self):
        ma_date = datetime.today()
        ma_date_iso = ma_date.isoformat()
        city = City(id="102", created_at=ma_date_iso, updated_at=ma_date_iso)
        self.assertEqual(city.id, "102")
        self.assertEqual(city.created_at, ma_date)
        self.assertEqual(city.updated_at, ma_date)

    def test_inst_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method  of  City class."""

    @classmethod
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
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def test_two_saves(self):
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def test_save_with_arg(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self):
        city = City()
        city.save()
        city_id = "City." + city.id
        with open("file.json", "r") as fl:
            self.assertIn(city_id, fl.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method  of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_contains_added_attributes(self):
        city = City()
        city.middle_name = "Othmane"
        city.my_number = 777
        self.assertEqual("Othmane", city.middle_name)
        self.assertIn("my_number", city.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        ma_date = datetime.today()
        city = City()
        city.id = "291102"
        city.created_at = city.updated_at = ma_date
        to_dict = {
            'id': '291102',
            '__class__': 'City',
            'created_at': ma_date.isoformat(),
            'updated_at': ma_date.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), to_dict)

    def test_to_dict_with_args(self):
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)


if __name__ == "__main__":
    unittest.main()
