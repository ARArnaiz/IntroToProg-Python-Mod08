# ------------------------------------------------------------------------------------ #
# Title: Employee Ratings Application — Entry Point
# Description: Orchestrates the Employee Ratings application by tying together
#              the data, processing, and presentation layers.
#              Reads employee data from JSON on startup, then enters a menu loop
#              that allows the user to view, enter, save, or exit.
# ChangeLog: (Who, When, What)
# RRoot, 1.5.2030, Created starter script
# Alfredo Arnaiz, 20260314, Split into layered modules; set up main.py as the
#                            sole entry point using the if __name__ == "__main__"
#                            guard to prevent execution on import
# Alfredo Arnaiz, 20260316, Added try/except block to handle also
#                           json.JSONDecodeError raised in
#                           read_employee_data_from_file()
# ------------------------------------------------------------------------------------ #

import data_classes as data
import presentation_classes as pres
import processing_classes as proc


if __name__ == "__main__":

    # Load existing employee data from the JSON file on startup.
    try:
        employees = proc.FileProcessor.read_employee_data_from_file(
            file_name=data.FILE_NAME,
            employee_data=data.employees,
            employee_type=data.Employee,
        )
    except Exception as e:
        pres.IO.output_error_messages(e)

    # Main menu loop — runs until the user chooses option 4 (Exit).
    while True:
        pres.IO.output_menu(menu=data.MENU)
        menu_choice = pres.IO.input_menu_choice()

        if menu_choice == "1":  # Display current employee data
            try:
                pres.IO.output_employee_data(employee_data=employees)
            except Exception as e:
                pres.IO.output_error_messages(e)
            continue

        elif menu_choice == "2":  # Add a new employee rating
            try:
                employees = pres.IO.input_employee_data(
                    employee_data=employees,
                    employee_type=data.Employee,
                )
                pres.IO.output_employee_data(employee_data=employees)
            except Exception as e:
                pres.IO.output_error_messages(e)
            continue

        elif menu_choice == "3":  # Save all data to the JSON file
            try:
                proc.FileProcessor.write_employee_data_to_file(
                    file_name=data.FILE_NAME,
                    employee_data=employees,
                )
                print(f"Data was saved to the {data.FILE_NAME} file.")
            except Exception as e:
                pres.IO.output_error_messages(e)
            continue

        elif menu_choice == "4":  # Exit
            break
