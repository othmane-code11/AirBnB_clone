#!/usr/bin/python3
"""
Module for testing Review class.
"""

import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.review import Review


class TestReview_inst(unittest.TestCase):
    """
    Unittests for testing instantiation of  Review class.
    """
    def test_no_args_inst(self):
        self.assertEqual(Review, type(Review()))

    def test_new_inst_stored_in_objs(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_created_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_a_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_id_is_a_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_place_id_is_a_public_class_attribute(self):
        rev_iew = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertNotIn("place_id", rev_iew.__dict__)
        self.assertIn("place_id", dir(rev_iew))

    def test_user_id_is_a_public_class_attribute(self):
        rev_iew = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rev_iew))
        self.assertNotIn("user_id", rev_iew.__dict__)

    def test_text_is_a_public_class_attribute(self):
        rev_iew = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rev_iew))
        self.assertNotIn("text", rev_iew.__dict__)

    def test_two_reviews_unique_ids(self):
        review_num1 = Review()
        review_num2 = Review()
        self.assertNotEqual(review_num1.id, review_num2.id)

    def test_two_reviews_different_created_at(self):
        review_num1 = Review()
        sleep(0.05)
        review_num2 = Review()
        self.assertLess(review_num1.created_at, review_num2.created_at)

    def test_two_reviews_different_updated_at(self):
        review_num1 = Review()
        sleep(0.05)
        review_num2 = Review()
        self.assertLess(review_num1.updated_at, review_num2.updated_at)

    def test_str_representation(self):
        ma_date = datetime.today()
        ma_date_repr = repr(ma_date)
        review = Review()
        review.id = "291102"
        review.created_at = review.updated_at = ma_date
        review_str = review.__str__()
        self.assertIn("[Review] (291102)", review_str)
        self.assertIn("'id': '291102'", review_str)
        self.assertIn("'created_at': " + ma_date_repr, review_str)
        self.assertIn("'updated_at': " + ma_date_repr, review_str)

    def test_arg_unused(self):
        rev_iew = Review(None)
        self.assertNotIn(None, rev_iew.__dict__.values())

    def test_inst_with_kwargs(self):
        ma_date = datetime.today()
        ma_date_iso = ma_date.isoformat()
        revw = Review(id="102", created_at=ma_date_iso, updated_at=ma_date_iso)
        self.assertEqual(revw.id, "102")
        self.assertEqual(revw.created_at, ma_date)
        self.assertEqual(revw.updated_at, ma_date)

    def test_inst_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of Review class."""

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
        rev_iew = Review()
        sleep(0.05)
        first_updated_at = rev_iew.updated_at
        rev_iew.save()
        self.assertLess(first_updated_at, rev_iew.updated_at)

    def test_two_saves(self):
        rev_iew = Review()
        sleep(0.05)
        first_updated_at = rev_iew.updated_at
        rev_iew.save()
        second_updated_at = rev_iew.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rev_iew.save()
        self.assertLess(second_updated_at, rev_iew.updated_at)

    def test_save_with_arg(self):
        rev_iew = Review()
        with self.assertRaises(TypeError):
            rev_iew.save(None)

    def test_save_updates_file(self):
        rev_iew = Review()
        rev_iew.save()
        rev_iew_id = "Review." + rev_iew.id
        with open("file.json", "r") as fl:
            self.assertIn(rev_iew_id, fl.read())


class TestReview_to_dict(unittest.TestCase):
    """
    Unittests for testing to_dict method of
    the Review class."""
    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        rev_iew = Review()
        self.assertIn("id", rev_iew.to_dict())
        self.assertIn("created_at", rev_iew.to_dict())
        self.assertIn("updated_at", rev_iew.to_dict())
        self.assertIn("__class__", rev_iew.to_dict())

    def test_to_dict_contains_added_attributes(self):
        rev_iew = Review()
        rev_iew.middle_name = "Othmane"
        rev_iew.my_number = 777
        self.assertEqual("Othmane", rev_iew.middle_name)
        self.assertIn("my_number", rev_iew.to_dict())

    def test_to_dict_datetime_attrs_are_strs(self):
        rev_iew = Review()
        rev_iew_dict = rev_iew.to_dict()
        self.assertEqual(str, type(rev_iew_dict["id"]))
        self.assertEqual(str, type(rev_iew_dict["created_at"]))
        self.assertEqual(str, type(rev_iew_dict["updated_at"]))

    def test_to_dict_output(self):
        ma_date = datetime.today()
        review = Review()
        review.id = "291102"
        review.created_at = review.updated_at = ma_date
        to_dict = {
            'id': '291102',
            '__class__': 'Review',
            'created_at': ma_date.isoformat(),
            'updated_at': ma_date.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), to_dict)

    def test_to_dict_with_arg(self):
        rev_iew = Review()
        with self.assertRaises(TypeError):
            rev_iew.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        rev_iew = Review()
        self.assertNotEqual(rev_iew.to_dict(), rev_iew.__dict__)


if __name__ == "__main__":
    unittest.main()
