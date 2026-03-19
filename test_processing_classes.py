# ------------------------------------------------------------------------------------ #
# Title: Test Processing Classes Module
# Description: Unit tests for the FileProcessor class in processing_classes.py
# ChangeLog: (Who, When, What)
# Alfredo Arnaiz, 20260314, Created module
# ------------------------------------------------------------------------------------ #

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import data_classes as data
from processing_classes import FileProcessor


class TestFileProcessor(unittest.TestCase):
    """
    Tests for the FileProcessor class.

    ChangeLog:
    - Alfredo Arnaiz, 20260314: Created test class.
    """

    def setUp(self):
        """Create a temporary JSON file and sample employee data before each test."""
        self.test_employees = [
            data.Employee(first_name="Sue", last_name="Jones",
                          review_date="2025-12-24", review_rating=4),
            data.Employee(first_name="Vu", last_name="Vic",
                          review_date="2025-06-01", review_rating=5),
        ]

        # Write a valid temp JSON file for read tests
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        json.dump([
            {"FirstName": "Sue", "LastName": "Jones",
             "ReviewDate": "2025-12-24", "ReviewRating": 4},
            {"FirstName": "Vu", "LastName": "Vic",
             "ReviewDate": "2025-06-01", "ReviewRating": 5},
        ], self.temp_file)
        self.temp_file.close()

    def tearDown(self):
        """Remove the temporary file after each test."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    # read_employee_data_from_file tests

    def test_read_returns_correct_number_of_employees(self):
        """Test that reading a valid file returns the correct number of Employee objects."""
        result = FileProcessor.read_employee_data_from_file(
            file_name=self.temp_file.name,
            employee_data=[],
            employee_type=data.Employee
        )
        self.assertEqual(len(result), 2)

    def test_read_returns_employee_objects(self):
        """Test that the returned list contains Employee instances."""
        result = FileProcessor.read_employee_data_from_file(
            file_name=self.temp_file.name,
            employee_data=[],
            employee_type=data.Employee
        )
        for emp in result:
            self.assertIsInstance(emp, data.Employee)

    def test_read_correct_field_values(self):
        """Test that employee fields are read and assigned correctly."""
        result = FileProcessor.read_employee_data_from_file(
            file_name=self.temp_file.name,
            employee_data=[],
            employee_type=data.Employee
        )
        self.assertEqual(result[0].first_name, "Sue")
        self.assertEqual(result[0].last_name, "Jones")
        self.assertEqual(result[0].review_date, "2025-12-24")
        self.assertEqual(result[0].review_rating, 4)

    def test_read_file_not_found_raises(self):
        """Test that a missing file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            FileProcessor.read_employee_data_from_file(
                file_name="nonexistent_file.json",
                employee_data=[],
                employee_type=data.Employee
            )

    def test_read_file_invalid_json_raises(self):
        """Test that a file containing invalid JSON raises Exception."""
        # Overwrite the temp file with invalid JSON content
        with open(self.temp_file.name, "w") as f:
            f.write("this is not valid json {{{")
        with self.assertRaises(Exception):
            FileProcessor.read_employee_data_from_file(
                file_name=self.temp_file.name,
                employee_data=[],
                employee_type=data.Employee
            )

    # write_employee_data_to_file tests

    def test_write_receives_invalid_file_raises(self):
        """Test that a PermissionError raised by open() is propagated correctly."""
        with patch("builtins.open", side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                FileProcessor.write_employee_data_to_file(
                    file_name="any_file.json",
                    employee_data=self.test_employees
                )

    def test_write_creates_valid_json(self):
        """Test that written data is valid JSON."""
        FileProcessor.write_employee_data_to_file(
            file_name=self.temp_file.name,
            employee_data=self.test_employees
        )
        with open(self.temp_file.name, "r") as f:
            result = json.load(f)
        self.assertIsInstance(result, list)

    def test_write_correct_number_of_records(self):
        """Test that the correct number of records is written to the file."""
        FileProcessor.write_employee_data_to_file(
            file_name=self.temp_file.name,
            employee_data=self.test_employees
        )
        with open(self.temp_file.name, "r") as f:
            result = json.load(f)
        self.assertEqual(len(result), 2)

    def test_write_correct_field_values(self):
        """Test that employee field values are written correctly to JSON."""
        FileProcessor.write_employee_data_to_file(
            file_name=self.temp_file.name,
            employee_data=self.test_employees
        )
        with open(self.temp_file.name, "r") as f:
            result = json.load(f)
        self.assertEqual(result[0]["FirstName"], "Sue")
        self.assertEqual(result[0]["LastName"], "Jones")
        self.assertEqual(result[0]["ReviewDate"], "2025-12-24")
        self.assertEqual(result[0]["ReviewRating"], 4)

    def test_write_then_read_roundtrip(self):
        """Test that data written to file can be read back correctly."""
        FileProcessor.write_employee_data_to_file(
            file_name=self.temp_file.name,
            employee_data=self.test_employees
        )
        result = FileProcessor.read_employee_data_from_file(
            file_name=self.temp_file.name,
            employee_data=[],
            employee_type=data.Employee
        )
        self.assertEqual(result[0].first_name, self.test_employees[0].first_name)
        self.assertEqual(result[0].review_rating, self.test_employees[0].review_rating)


if __name__ == "__main__":
    unittest.main()
