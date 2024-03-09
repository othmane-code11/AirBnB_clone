#!/usr/bin/python3
"""
unittests for the state class
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """
    Unittests for testing instantiation of  State class.
    """
    def test_no_arg_insts(self):
        self.assertEqual(State, type(State()))

    def test_created_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_new_inst_stored_in_objs(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_a_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_name_is_a_public_class_attribute(self):
        sta_te = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(sta_te))
        self.assertNotIn("name", sta_te.__dict__)

    def test_two_states_unique_ids(self):
        state_num1 = State()
        state_num2 = State()
        self.assertNotEqual(state_num1.id, state_num2.id)

    def test_two_states_different_created_at(self):
        state_num1 = State()
        sleep(0.05)
        state_num2 = State()
        self.assertLess(state_num1.created_at, state_num2.created_at)

    def test_two_states_different_updated_at(self):
        state_num1 = State()
        sleep(0.05)
        state_num2 = State()
        self.assertLess(state_num1.updated_at, state_num2.updated_at)

    def test_str_repr(self):
        ma_date = datetime.today()
        ma_date_repr = repr(ma_date)
        sta_te = State()
        sta_te.id = "291102"
        sta_te.created_at = sta_te.updated_at = ma_date
        sta_te_str = sta_te.__str__()
        self.assertIn("[State] (291102)", sta_te_str)
        self.assertIn("'id': '291102'", sta_te_str)
        self.assertIn("'created_at': " + ma_date_repr, sta_te_str)
        self.assertIn("'updated_at': " + ma_date_repr, sta_te_str)

    def test_arg_unused(self):
        sta_te = State(None)
        self.assertNotIn(None, sta_te.__dict__.values())

    def test_inst_with_kwargs(self):
        ma_date = datetime.today()
        ma_date_iso = ma_date.isoformat()
        stte = State(id="102", created_at=ma_date_iso, updated_at=ma_date_iso)
        self.assertEqual(stte.id, "102")
        self.assertEqual(stte.created_at, ma_date)
        self.assertEqual(stte.updated_at, ma_date)

    def test_inst_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """
    Unittests for testing save method of  State class.
    """
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
        sta_te = State()
        sleep(0.05)
        first_updated_at = sta_te.updated_at
        sta_te.save()
        self.assertLess(first_updated_at, sta_te.updated_at)

    def test_two_saves(self):
        sta_te = State()
        sleep(0.05)
        first_updated_at = sta_te.updated_at
        sta_te.save()
        second_updated_at = sta_te.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        sta_te.save()
        self.assertLess(second_updated_at, sta_te.updated_at)

    def test_save_with_arg(self):
        sta_te = State()
        with self.assertRaises(TypeError):
            sta_te.save(None)

    def test_save_updates_file(self):
        sta_te = State()
        sta_te.save()
        sta_te_id = "State." + sta_te.id
        with open("file.json", "r") as f:
            self.assertIn(sta_te_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of State class."""
    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        sta_te = State()
        self.assertIn("id", sta_te.to_dict())
        self.assertIn("created_at", sta_te.to_dict())
        self.assertIn("updated_at", sta_te.to_dict())
        self.assertIn("__class__", sta_te.to_dict())

    def test_to_dict_contains_added_attributes(self):
        sta_te = State()
        sta_te.middle_name = "Othmane"
        sta_te.my_number = 777
        self.assertEqual("Othmane", sta_te.middle_name)
        self.assertIn("my_number", sta_te.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        sta_te = State()
        sta_te_dict = sta_te.to_dict()
        self.assertEqual(str, type(sta_te_dict["id"]))
        self.assertEqual(str, type(sta_te_dict["created_at"]))
        self.assertEqual(str, type(sta_te_dict["updated_at"]))

    def test_to_dict_output(self):
        ma_date = datetime.today()
        sta_te = State()
        sta_te.id = "291102"
        sta_te.created_at = sta_te.updated_at = ma_date
        the_dict = {
            'id': '291102',
            '__class__': 'State',
            'created_at': ma_date.isoformat(),
            'updated_at': ma_date.isoformat(),
        }
        self.assertDictEqual(sta_te.to_dict(), the_dict)

    def test_to_dict_with_arg(self):
        sta_te = State()
        with self.assertRaises(TypeError):
            sta_te.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        sta_te = State()
        self.assertNotEqual(sta_te.to_dict(), sta_te.__dict__)


if __name__ == "__main__":
    unittest.main()
