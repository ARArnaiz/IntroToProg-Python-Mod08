# ------------------------------------------------------------------------------------ #
# Title: Processing Classes Module
# Description: Processing layer for the Employee Ratings application.
#              Contains FileProcessor, which handles all JSON read and write
#              operations for persisting employee data.
# ChangeLog: (Who, When, What)
# RRoot, 1.1.2030, Created FileProcessor class
# Alfredo Arnaiz, 20260314, Created module; split class from starter script;
#                            preserved original exception message in the
#                            general except clause via f-string interpolation
# ------------------------------------------------------------------------------------ #

import json
import data_classes as data


class FileProcessor:
    """
    A collection of static methods that read and write employee data as JSON.

    ChangeLog: (Who, When, What)
    RRoot, 1.1.2030, Created class
    """

    @staticmethod
    def read_employee_data_from_file(
        file_name: str,
        employee_data: list,
        employee_type: data.Employee,
    ) -> list:
        """Read employee records from a JSON file and return them as Employee objects.

        Each JSON object in the file is expected to have the keys "FirstName",
        "LastName", "ReviewDate", and "ReviewRating".  A new instance of
        employee_type is created for each record and appended to employee_data.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Alfredo Arnaiz, 20260314, Added exception handler for a json.JSONDecodeError.
                                   Added f-string to general except so the
                                   original exception message is not silently
                                   discarded.

        :param file_name: Path to the JSON file to read.
        :param employee_data: List to populate with Employee objects.
        :param employee_type: The Employee class used to instantiate records.
        :raises FileNotFoundError: If the specified file does not exist.
        :raises json.JSONDecodeError: If JSON file is malformed.
        :raises Exception: For any other error encountered during reading.
        :return: The populated list of Employee objects.
        """
        try:
            with open(file_name, "r") as file:
                list_of_dictionary_data = json.load(file)  # the load function returns a list of dictionary rows.
                for employee in list_of_dictionary_data:
                    employee_object = employee_type()
                    employee_object.first_name = employee["FirstName"]
                    employee_object.last_name = employee["LastName"]
                    employee_object.review_date = employee["ReviewDate"]
                    employee_object.review_rating = employee["ReviewRating"]
                    employee_data.append(employee_object)
        except FileNotFoundError:
            raise FileNotFoundError("JSON file must exist before running this script!")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON file is malformed! Check the file for syntax errors.\n{e}")
        except Exception as e:
            raise Exception(f"There was a non-specific error! {e}")
        return employee_data

    @staticmethod
    def write_employee_data_to_file(file_name: str, employee_data: list) -> None:
        """Write the list of Employee objects to a JSON file.

        Each Employee object is converted to a dictionary with the keys
        "FirstName", "LastName", "ReviewDate", and "ReviewRating" before
        being serialized to JSON with two-space indentation.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param file_name: string data with name of file to write to
        :param employee_data: list of dictionary rows to be writen to the file

        :return: None
        """
        try:
            list_of_dictionary_data: list = []
            for employee in employee_data:
                employee_json: dict = {
                    "FirstName": employee.first_name,
                    "LastName": employee.last_name,
                    "ReviewDate": employee.review_date,
                    "ReviewRating": employee.review_rating,
                }
                list_of_dictionary_data.append(employee_json)

            with open(file_name, "w") as file:
                json.dump(list_of_dictionary_data, file, indent=2)
        except TypeError:
            raise TypeError("Please check that the data is a valid JSON format")
        except PermissionError:
            raise PermissionError("Please check the data file's read/write permission")
        except Exception as e:
            raise Exception(f"There was a non-specific error! {e}")
