# ------------------------------------------------------------------------------------ #
# Title: Test Presentation Classes Module
# Description: Unit tests for the IO class in presentation_classes.py
# ChangeLog: (Who, When, What)
# Alfredo Arnaiz, 20260314, Created module
# ------------------------------------------------------------------------------------ #

import unittest
from unittest.mock import patch
import io
import data_classes as data
from presentation_classes import IO


class TestIO(unittest.TestCase):
    """
    Tests for the IO class.

    ChangeLog:
    - Alfredo Arnaiz, 20260314: Created test class.
    """

    # output_error_messages tests

    def test_output_error_messages_message_only(self):
        """Test that a message is printed when no error object is provided."""
        with patch('builtins.print') as mock_print:
            IO.output_error_messages("Something went wrong")
            mock_print.assert_called_with("Something went wrong", end="\n\n")

    def test_output_error_messages_with_error(self):
        """Test that technical error details are printed when an error is provided."""
        error = ValueError("bad value")
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_error_messages("Something went wrong", error)
            output = mock_stdout.getvalue()
        self.assertIn("Something went wrong", output)
        self.assertIn("Technical Error Message", output)

    # output_menu tests

    def test_output_menu_contains_menu_text(self):
        """Test that the menu string is printed to stdout."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_menu(menu=data.MENU)
            output = mock_stdout.getvalue()
        self.assertIn("Employee Ratings", output)

    # input_menu_choice tests

    def test_input_menu_choice_valid(self):
        """Test that a valid menu choice is returned as a string."""
        for choice in ("1", "2", "3", "4"):
            with patch('builtins.input', return_value=choice):
                result = IO.input_menu_choice()
            self.assertEqual(result, choice)

    def test_input_menu_choice_retry_until_valid(self):
        """Test that the loop continues after invalid input until a valid choice is entered."""
        #Simulate the user entering "9" (invalid), then "A" (invalid), then "2" (valid)
        inputs = ["9", "A", "2"]

        with patch('builtins.input', side_effect=inputs):
            # Patch output_error_messages so the test console stays clean
            with patch('presentation_classes.IO.output_error_messages') as mock_error:
                result = IO.input_menu_choice()
        # 1. Verify it eventually returned the valid choice
        self.assertEqual(result, "2")
        # 2. Verify that the error message was triggered twice (for "9" and "A")
        self.assertEqual(mock_error.call_count, 2)

    # output_employee_data tests

    def test_output_employee_data_rating_5(self):
        """Test that a rating of 5 displays 'Leading'."""
        emp = data.Employee("Mary", "Morrison", "2025-01-01", 5)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data([emp])
            output = mock_stdout.getvalue()
        self.assertIn("Leading", output)

    def test_output_employee_data_rating_4(self):
        """Test that a rating of 4 displays 'Strong'."""
        emp = data.Employee("Sue", "Jones", "2025-12-24", 4)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data([emp])
            output = mock_stdout.getvalue()
        self.assertIn("Strong", output)

    def test_output_employee_data_rating_3(self):
        """Test that a rating of 3 displays 'Solid'."""
        emp = data.Employee("Bob", "Barker", "2025-06-01", 3)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data([emp])
            output = mock_stdout.getvalue()
        self.assertIn("Solid", output)

    def test_output_employee_data_rating_2(self):
        """Test that a rating of 2 displays 'Building'."""
        emp = data.Employee("Tom", "Thompson", "2025-06-01", 2)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data([emp])
            output = mock_stdout.getvalue()
        self.assertIn("Building", output)

    def test_output_employee_data_rating_1(self):
        """Test that a rating of 1 displays 'Not Meeting Expectations'."""
        emp = data.Employee("John", "Johnson", "2025-06-01", 1)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data([emp])
            output = mock_stdout.getvalue()
        self.assertIn("Not Meeting Expectations", output)

    def test_output_employee_data_shows_name(self):
        """Test that the employee's name appears in the output."""
        emp = data.Employee("Sue", "Jones", "2025-12-24", 4)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data([emp])
            output = mock_stdout.getvalue()
        self.assertIn("Sue", output)
        self.assertIn("Jones", output)

    def test_output_employee_data_shows_all_fields(self):
        """Test that the employee's name, review date, and rating label all appear in output."""
        emp = data.Employee("Sue", "Jones", "2025-12-24", 4)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data([emp])
            output = mock_stdout.getvalue()
        self.assertIn("Sue", output)
        self.assertIn("Jones", output)
        self.assertIn("2025-12-24", output)
        self.assertIn("Strong", output)

    def test_output_employee_data_multiple(self):
        """Test that multiple employees are all displayed."""
        employees = [
            data.Employee("Sue", "Jones", "2025-12-24", 4),
            data.Employee("Vu", "Vic", "2025-06-01", 5),
        ]
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            IO.output_employee_data(employees)
            output = mock_stdout.getvalue()
        self.assertIn("Sue", output)
        self.assertIn("Vu", output)

    # input_employee_data tests

    def test_input_employee_data_returns_list(self):
        """Test that input_employee_data returns a list."""
        inputs = ["Sue", "Jones", "2025-12-24", "4"]
        with patch('builtins.input', side_effect=inputs):
            result = IO.input_employee_data([], data.Employee)
        self.assertIsInstance(result, list)

    def test_input_employee_data_appends_employee(self):
        """Test that a new Employee object is appended to the list."""
        inputs = ["Sue", "Jones", "2025-12-24", "4"]
        with patch('builtins.input', side_effect=inputs):
            result = IO.input_employee_data([], data.Employee)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], data.Employee)

    def test_input_employee_data_correct_values(self):
        """Test that the Employee object has the correct field values."""
        inputs = ["Sue", "Jones", "2025-12-24", "4"]
        with patch('builtins.input', side_effect=inputs):
            result = IO.input_employee_data([], data.Employee)
        self.assertEqual(result[0].first_name, "Sue")
        self.assertEqual(result[0].last_name, "Jones")
        self.assertEqual(result[0].review_date, "2025-12-24")
        self.assertEqual(result[0].review_rating, 4)

    def test_input_employee_data_multiple_entries(self):
        """Test that multiple employees can be entered and appended to the list."""
        existing = [data.Employee("Vu", "Vic", "2025-06-01", 5)]
        inputs = ["Sue", "Jones", "2025-12-24", "4"]
        with patch('builtins.input', side_effect=inputs):
            result = IO.input_employee_data(existing, data.Employee)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].first_name, "Sue")

    def test_input_employee_data_invalid_first_name_returns_empty_list(self):
        """Test that an invalid first name (with numbers) does not append to the list."""
        inputs = ["Su3", "Jones", "2025-12-24", "4"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=io.StringIO):
                result = IO.input_employee_data([], data.Employee)
        self.assertEqual(len(result), 0)

    def test_input_employee_data_invalid_last_name_returns_empty_list(self):
        """Test that an invalid last name (with numbers) does not append to the list."""
        inputs = ["Sue", "Jon3s", "2025-12-24", "4"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=io.StringIO):
                result = IO.input_employee_data([], data.Employee)
        self.assertEqual(len(result), 0)

    def test_input_employee_data_invalid_rating_returns_empty_list(self):
        """Test that an invalid rating (not 1-5) does not append to the list."""
        inputs = ["Sue", "Jones", "2025-12-24", "9"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=io.StringIO):
                result = IO.input_employee_data([], data.Employee)
        self.assertEqual(len(result), 0)

    def test_input_employee_data_invalid_date_returns_empty_list(self):
        """Test that an invalid date format does not append to the list."""
        inputs = ["Sue", "Jones", "24-12-2025", "4"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=io.StringIO):
                result = IO.input_employee_data([], data.Employee)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
