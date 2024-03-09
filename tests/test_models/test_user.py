#!/usr/bin/python3
"""Module for the User  class"""

import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.user import User


class TestUser_inst(unittest.TestCase):
    """
    Unittests for testing instantiatioon of  User class.
    """
    def test_created_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_a_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_no_arg_insts(self):
        self.assertEqual(User, type(User()))

    def test_new_inst_stored_in_objs(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_a_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_last_name_is_a_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_password_is_a_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_a_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_two_users_unique_ids(self):
        user_num1 = User()
        user_num2 = User()
        self.assertNotEqual(user_num1.id, user_num2.id)

    def test_two_users_different_updated_at(self):
        u_num1 = User()
        sleep(0.05)
        u_num2 = User()
        self.assertLess(u_num1.updated_at, u_num2.updated_at)

    def test_two_users_different_created_at(self):
        u_num1 = User()
        sleep(0.05)
        u_num2 = User()
        self.assertLess(u_num1.created_at, u_num2.created_at)

    def test_str_repr(self):
        ma_date = datetime.today()
        ma_date_repr = repr(ma_date)
        u_num1 = User()
        u_num1.id = "291102"
        u_num1.created_at = u_num1.updated_at = ma_date
        u_num1_str = u_num1.__str__()
        self.assertIn("[User] (291102)", u_num1_str)
        self.assertIn("'id': '291102'", u_num1_str)
        self.assertIn("'created_at': " + ma_date_repr, u_num1_str)
        self.assertIn("'updated_at': " + ma_date_repr, u_num1_str)

    def test_args_unused(self):
        user_num1 = User(None)
        self.assertNotIn(None, user_num1.__dict__.values())

    def test_inst_tion_with_kwargs(self):
        ma_dt = datetime.today()
        ma_dt_iso = ma_dt.isoformat()
        u_1 = User(id="102", created_at=ma_dt_iso, updated_at=ma_dt_iso)
        self.assertEqual(u_1.id, "102")
        self.assertEqual(u_1.created_at, ma_dt)
        self.assertEqual(u_1.updated_at, ma_dt)

    def test_inst_tion_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save  method of  class user."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmpt.json")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmpt.json", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        us_er = User()
        sleep(0.05)
        first_updated_at = us_er.updated_at
        us_er.save()
        self.assertLess(first_updated_at, us_er.updated_at)

    def test_two_saves(self):
        us_er = User()
        sleep(0.05)
        first_updated_at = us_er.updated_at
        us_er.save()
        second_updated_at = us_er.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        us_er.save()
        self.assertLess(second_updated_at, us_er.updated_at)

    def test_save_with_args(self):
        us_er = User()
        with self.assertRaises(TypeError):
            us_er.save(None)

    def test_save_updates_file(self):
        us_er = User()
        us_er.save()
        us_er_id = "User." + us_er.id
        with open("file.json", "r") as fl:
            self.assertIn(us_er_id, fl.read())


class Test_User_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method   User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        us_er = User()
        self.assertIn("id", us_er.to_dict())
        self.assertIn("updated_at", us_er.to_dict())
        self.assertIn("__class__", us_er.to_dict())
        self.assertIn("created_at", us_er.to_dict())

    def test_to_dict_contains_added_attributes(self):
        us_er = User()
        us_er.middle_name = "Othmane"
        us_er.my_number = 98
        self.assertEqual("Othmane", us_er.middle_name)
        self.assertIn("my_number", us_er.to_dict())

    def test_to_dict_datetime_attrts_are_strs(self):
        us_er = User()
        us_er_dict = us_er.to_dict()
        self.assertEqual(str, type(us_er_dict["id"]))
        self.assertEqual(str, type(us_er_dict["created_at"]))
        self.assertEqual(str, type(us_er_dict["updated_at"]))

    def test_to_dict_output(self):
        ma_date = datetime.today()
        us_er = User()
        us_er.id = "291102"
        us_er.created_at = us_er.updated_at = ma_date
        the_dict = {
            'id': '291102',
            '__class__': 'User',
            'created_at': ma_date.isoformat(),
            'updated_at': ma_date.isoformat(),
        }
        self.assertDictEqual(us_er.to_dict(), the_dict)

    def test_to_dict_with_args(self):
        us_er = User()
        with self.assertRaises(TypeError):
            us_er.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        us_er = User()
        self.assertNotEqual(us_er.to_dict(), us_er.__dict__)


if __name__ == "__main__":
    unittest.main()
