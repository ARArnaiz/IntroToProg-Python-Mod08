# ------------------------------------------------------------------------------------ #
# Title: Test Data Classes Module
# Description: Unit tests for the Person and Employee classes in data_classes.py
# ChangeLog: (Who, When, What)
# Alfredo Arnaiz, 20260314, Created module
# ------------------------------------------------------------------------------------ #

import unittest

import data_classes as data


class TestPerson(unittest.TestCase):
    """
    Tests for the Person class.

    ChangeLog:
    - Alfredo Arnaiz, 20260314: Created test class.
    """

    # Constructor tests

    def test_person_init(self):
        """Test that a Person instance is created correctly."""
        person = data.Person("John", "Doe")
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")

    # first_name tests

    def test_first_name_valid(self):
        """Test that a valid first name is stored and returned title-cased."""
        person = data.Person(first_name="john", last_name="Doe")
        self.assertEqual(person.first_name, "John")

    def test_first_name_empty(self):
        """Test that an empty first name is accepted."""
        person = data.Person(first_name="", last_name="Doe")
        self.assertEqual(person.first_name, "")

    def test_first_name_with_numbers_raises(self):
        """Test that a first name containing numbers raises ValueError."""
        with self.assertRaises(ValueError):
            data.Person(first_name="J0hn", last_name="Doe")

    def test_first_name_with_spaces_raises(self):
        """Test that a first name containing spaces raises ValueError."""
        with self.assertRaises(ValueError):
            data.Person(first_name="John Paul", last_name="Doe")

    # last_name tests

    def test_last_name_valid(self):
        """Test that a valid last name is stored and returned title-cased."""
        person = data.Person(first_name="John", last_name="doe")
        self.assertEqual(person.last_name, "Doe")

    def test_last_name_empty(self):
        """Test that an empty last name is accepted."""
        person = data.Person(first_name="John", last_name="")
        self.assertEqual(person.last_name, "")

    def test_last_name_with_numbers_raises(self):
        """Test that a last name containing numbers raises ValueError."""
        with self.assertRaises(ValueError):
            data.Person(first_name="John", last_name="D0e")

    def test_last_name_with_spaces_raises(self):
        """Test that a last name containing non-alphabetic chars raises ValueError."""
        with self.assertRaises(ValueError):
            data.Person(first_name="John", last_name="Doe-Williams")

    #  __str__ magic method tests

    def test_str(self):
        """Test that __str__ returns comma-separated first and last name."""
        person = data.Person(first_name="John", last_name="Doe")
        self.assertEqual(str(person), "John,Doe")


class TestEmployee(unittest.TestCase):
    """
    Tests for the Employee class.

    ChangeLog:
    - Alfredo Arnaiz, 20260314: Created test class.
    """

    # Constructor and inheritance tests

    def test_Employee_init(self):
        """Test that Employee creates a valid instance, inherits from Person,
        and correctly stores all four field values."""
        emp = data.Employee("Alice", "Smith", "2023-01-31", 4)
        self.assertIsInstance(emp, data.Employee)
        self.assertIsInstance(emp, data.Person)
        self.assertEqual(emp.first_name, "Alice")
        self.assertEqual(emp.last_name, "Smith")
        self.assertEqual(emp.review_date, "2023-01-31")
        self.assertEqual(emp.review_rating, 4)

    def test_default_values(self):
        """Test that Employee default constructor values are all set correctly."""
        emp = data.Employee()
        self.assertIsInstance(emp, data.Employee)
        self.assertEqual(emp.first_name, "")
        self.assertEqual(emp.last_name, "")
        self.assertEqual(emp.review_date, "1900-01-01")
        self.assertEqual(emp.review_rating, 3)

    def test_inherits_first_name_validation(self):
        """Test that Employee inherits first_name validation from Person."""
        with self.assertRaises(ValueError):
            data.Employee(first_name="J0hn")

    def test_inherits_last_name_validation(self):
        """Test that Employee inherits last_name validation from Person."""
        with self.assertRaises(ValueError):
            data.Employee(last_name="D0e")

    # review_date tests

    def test_review_date_valid(self):
        """Test that a valid ISO date string is accepted."""
        emp = data.Employee(review_date="2025-12-24")
        self.assertEqual(emp.review_date, "2025-12-24")

    def test_review_date_invalid_format_raises(self):
        """Test that an invalid date string raises ValueError."""
        with self.assertRaises(ValueError):
            data.Employee(review_date="12-24-2025")

    def test_review_date_invalid(self):
        """Test that an invalid but well ISO formatted date raises ValueError."""
        with self.assertRaises(ValueError):
            data.Employee(review_date="2025-02-31")

    def test_review_date_non_date_raises(self):
        """Test that a non-date string raises ValueError."""
        for non_date in ("not-a-date", "?-?-?", "0000000000", "9999-99-99"):
            with self.assertRaises(ValueError):
                data.Employee(review_date=non_date)

    def test_review_date_empty_string_raises(self):
        """Test that an empty string raises ValueError."""
        with self.assertRaises(ValueError):
            data.Employee(review_date="")

    def test_review_date_whitespace_raises(self):
        """Test that whitespace/padded strings raise ValueError."""
        with self.assertRaises(ValueError):
            data.Employee(review_date=" 2025-12-24")

    # review_rating tests

    def test_review_rating_valid_each(self):
        """Test that each valid rating (1-5) is accepted."""
        for rating in (1, 2, 3, 4, 5):
            emp = data.Employee(review_rating=rating)
            self.assertEqual(emp.review_rating, rating)

    def test_review_invalid_ratings(self):
        """Test that invalid ratings raises ValueError."""
        for rating in (0, 6, -1):
            with self.assertRaises(ValueError):
                data.Employee(review_rating=rating)

    # -- __str__ -- tests

    def test_str(self):
        """Test that __str__ returns all four fields comma-separated, combining
        Person and Employee data via super().__str__()."""
        emp = data.Employee(
            first_name="Sue",
            last_name="Jones",
            review_date="2025-12-24",
            review_rating=4
        )
        self.assertEqual(str(emp), "Sue,Jones,2025-12-24,4")

    def test_str_title_case_inheritance(self):
        """Test that __str__ inherits and applies title case formatting from Person."""
        emp = data.Employee(
            first_name="vic",
            last_name="vu",
            review_date="2026-03-14",
            review_rating=5
        )
        self.assertEqual(str(emp), "Vic,Vu,2026-03-14,5")


if __name__ == "__main__":
    unittest.main()
