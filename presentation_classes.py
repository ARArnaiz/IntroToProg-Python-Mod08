# ------------------------------------------------------------------------------------ #
# Title: Presentation Classes Module
# Description: A collection of presentation layer classes for managing user
#              input and output in the Employee Ratings application.
# ChangeLog: (Who, When, What)
# RRoot, 1.1.2030, Created module
# Alfredo Arnaiz, 20260314, Created IO module
# Alfredo Arnaiz, 20260315, Modified input_menu_choice() to use a while loop
#                           that forces valid input before returning
# Alfredo Arnaiz, 20260316, Fixed NameError: added TYPE_CHECKING import guard
#                           so Employee type hint resolves at runtime
# ------------------------------------------------------------------------------------ #

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_classes import Employee


class IO:
    """
    A collection of static presentation layer methods that manage user input and output.

    ChangeLog: (Who, When, What)
    RRoot, 1.1.2030, Created class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None) -> None:
        """Display a user-friendly error message, with optional technical details.

        When an Exception object is supplied the method prints the exception text,
        its docstring, and its type on separate lines so that debugging information
        is visible without interrupting normal program flow.

        ChangeLog: (Who, When, What)
        RRoot, 1.3.2030, Created function

        :param message: User-facing description of the error.
        :param error: Optional Exception object whose technical details are appended.
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str) -> None:
        """Display the application menu string surrounded by blank lines.

        ChangeLog: (Who, When, What)
        RRoot, 1.1.2030, Created function

        :param menu: The multi-line menu string to display.
        :return: None
        """
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice() -> str:
        """Prompt the user for a menu selection and return it only when valid.

        Loops indefinitely, displaying an error message on each invalid entry,
        until the user types one of "1", "2", "3", or "4".

        ChangeLog: (Who, When, What)
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260315, Replaced single try/except with a while True
                                   loop so invalid input triggers a re-prompt
                                   rather than returning a bad value.

        :return: A single-character string: "1", "2", "3", or "4".
        """
        while True:
            try:
                choice = input("What would you like to do? ")
                if choice not in ("1", "2", "3", "4"):
                    raise ValueError("Please choose only options 1, 2, 3, or 4.")
                return choice
            except Exception as e:
                IO.output_error_messages(e.__str__())

    @staticmethod
    def output_employee_data(employee_data: list) -> None:
        """Display all employee records with their name, review date, rating number,
        and corresponding rating label.

        Rating labels are looked up from a dictionary rather than a chain of
        if/elif statements, making the mapping explicit and easy to extend.

        ChangeLog: (Who, When, What)
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260314, Added review_date to the output line; moved
                                   rating descriptions to a dictionary.
                                   Replaced the message variable + .format() pattern
                                   with an f-string directly inside print() which
                                   removes the extra variable.

        :param employee_data: List of Employee objects to display.
        :return: None
        """
        rating_descriptions = {
            5: "(Leading)",
            4: "(Strong)",
            3: "(Solid)",
            2: "(Building)",
            1: "(Not Meeting Expectations)",
        }
        print()
        print("-" * 75)
        for employee in employee_data:
            rating_description = rating_descriptions.get(employee.review_rating, "Unknown")
            print(
                f" {employee.first_name} {employee.last_name} "
                f"reviewed on {employee.review_date} "
                f"is rated as {employee.review_rating} {rating_description}"
            )
        print("-" * 75)
        print()

    @staticmethod
    def input_employee_data(employee_data: list, employee_type: type) -> list:
        """Collect a new employee record from the user and append it to employee_data.

        Prompts for first name, last name, review date (YYYY-MM-DD), and review
        rating (1–5). Property setters on the Employee class perform validation;
        any ValueError is caught here and reported via output_error_messages()
        without adding a partial record to the list.

        ChangeLog: (Who, When, What)
        RRoot, 1.1.2030, Created function
        Alfredo Arnaiz, 20260314, Corrected docstring to match actual parameters
                                   and describe validation behavior.
        Alfredo Arnaiz, 20260316, Changed employee_type annotation from Employee
                                   to 'type' to remove the NameError that occurred
                                   when the module was imported without data_classes.
                                   Updated two of the input prompts to show the user
                                   the expected format.

        :param employee_data: Existing list of Employee objects to append to.
        :param employee_type: The Employee class (passed in to avoid a direct import).
        :return: The updated list of Employee objects.
        """
        try:
            employee_object = employee_type()
            employee_object.first_name = input("What is the employee's first name? ")
            employee_object.last_name = input("What is the employee's last name? ")
            employee_object.review_date = input("What is their review date (YYYY-MM-DD)? ")
            employee_object.review_rating = int(input("What is their review rating (1-5)? "))
            employee_data.append(employee_object)
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)

        return employee_data
