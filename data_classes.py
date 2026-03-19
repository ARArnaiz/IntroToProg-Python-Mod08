# ------------------------------------------------------------------------------------ #
# Title: Data Classes Module
# Description: Data layer for the Employee Ratings application.
#              Contains the Person and Employee classes, application constants,
#              and the shared runtime variables used across modules.
# ChangeLog: (Who, When, What)
# RRoot, 1.1.2030, Created Person and Employee classes
# Alfredo Arnaiz, 20260314, Created module; split classes from starter script;
#                            updated Employee.__str__() to delegate to super()
# ------------------------------------------------------------------------------------ #

from datetime import date

# -- Constants ------------------------------------------------------------------ #

FILE_NAME: str = 'EmployeeRatings.json'

MENU: str = '''
---- Employee Ratings ---------------------------
  Select from the following menu:
    1. Show current employee rating data.
    2. Enter new employee rating data.
    3. Save data to a file.
    4. Exit the program.
-------------------------------------------------
'''

# -- Shared runtime variables --------------------------------------------------- #
# These are initialized here and populated by main.py at startup.

employees: list = []  # table of Employee objects for the current session
menu_choice: str = ''


# -- Classes -------------------------------------------------------------------- #

class Person:
    """
    Represents a person with a first name and a last name.

    Both names are stored as private attributes and exposed through properties
    that validate and title-case their values.

    Properties:
        first_name (str): The person's first name. Must be alphabetic or empty.
        last_name  (str): The person's last name. Must be alphabetic or empty.

    ChangeLog: (Who, When, What)
    RRoot, 1.1.2030, Created class
    """

    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        """Return the first name in title case."""
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str) -> None:
        """Set the first name after validating that it contains only letters.

        :param value: Proposed first name string.
        :raises ValueError: If value contains non-alphabetic characters.
        """
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self) -> str:
        """Return the last name in title case."""
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str) -> None:
        """Set the last name after validating that it contains only letters.

        :param value: Proposed last name string.
        :raises ValueError: If value contains non-alphabetic characters.
        """
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self) -> str:
        """Return a comma-separated string of first and last name.

        :return: e.g. "Sue,Jones"
        """
        return f"{self.first_name},{self.last_name}"


class Employee(Person):
    """
    Represents an employee with performance review data.

    Extends Person by adding a review date and a review rating.  Property
    setters validate that the date is a valid ISO-format string and that
    the rating is an integer between 1 and 5 inclusive.

    Properties:
        first_name    (str)  : Inherited from Person.
        last_name     (str)  : Inherited from Person.
        review_date   (str)  : ISO-format date string (YYYY-MM-DD).
        review_rating (int)  : Performance rating, one of 1, 2, 3, 4, or 5.

    Defaults:
        first_name    = ""
        last_name     = ""
        review_date   = "1900-01-01"
        review_rating = 3

    ChangeLog: (Who, When, What)
    RRoot, 1.1.2030, Created class
    Alfredo Arnaiz, 20260314, Updated __str__() to call super().__str__()
                               instead of repeating first/last name fields
    """

    def __init__(
        self,
        first_name: str = "",
        last_name: str = "",
        review_date: str = "1900-01-01",
        review_rating: int = 3,
    ):
        super().__init__(first_name=first_name, last_name=last_name)
        self.review_date = review_date
        self.review_rating = review_rating

    @property
    def review_date(self) -> str:
        """Return the review date string."""
        return self.__review_date

    @review_date.setter
    def review_date(self, value: str) -> None:
        """Set the review date after validating ISO format (YYYY-MM-DD).

        :param value: Date string to validate.
        :raises ValueError: If value is not a valid ISO date.
        """
        try:
            date.fromisoformat(value)
            self.__review_date = value
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    @property
    def review_rating(self) -> int:
        """Return the review rating integer."""
        return self.__review_rating

    @review_rating.setter
    def review_rating(self, value: int) -> None:
        """Set the review rating after validating it is in the range 1–5.

        :param value: Integer rating to validate.
        :raises ValueError: If value is not one of 1, 2, 3, 4, or 5.
        """
        if value in (1, 2, 3, 4, 5):
            self.__review_rating = value
        else:
            raise ValueError("Please choose only values 1 through 5")

    def __str__(self) -> str:
        """Return a comma-separated string of all four employee fields.

        Delegates first_name and last_name formatting to Person.__str__()
        via super() to avoid duplicating title-case logic.

        :return: e.g. "Sue,Jones,2025-12-24,4"
        """
        return f"{super().__str__()},{self.review_date},{self.review_rating}"
