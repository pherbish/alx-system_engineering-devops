#!/usr/bin/python3
"""
Returns to-do list information for a given employee ID.

This script takes an employee ID as a command-line argument and fetches
the corresponding user information and to-do list from the JSONPlaceholder API.
It then prints the tasks completed by the employee.
"""

import requests
import sys

if __name__ == "__main__":
        # Ensure the script is given exactly one argument
            if len(sys.argv) != 2:
                        print("Usage: {} <employee_id>".format(sys.argv[0]))
                                sys.exit(1)

                                    # Validate that the input is an integer
                                        try:
                                                    employee_id = int(sys.argv[1])
                                                        except ValueError:
                                                                    print("Error: Employee ID must be an integer.")
                                                                            sys.exit(1)

                                                                                # Base URL for the JSONPlaceholder API
                                                                                    url = "https://jsonplaceholder.typicode.com/"

                                                                                        # Get the employee information
                                                                                            user = requests.get(url + "users/{}".format(employee_id)).json()

                                                                                                # Check if the user exists
                                                                                                    if "name" not in user:
                                                                                                                print("Error: Employee ID {} not found.".format(employee_id))
                                                                                                                        sys.exit(1)

                                                                                                                            # Get the to-do list for the employee
                                                                                                                                todos = requests.get(url + "todos", params={"userId": employee_id}).json()

                                                                                                                                    # Filter completed tasks
                                                                                                                                        completed = [task["title"] for task in todos if task["completed"]]

                                                                                                                                            # Print the required output
                                                                                                                                                print("Employee {} is done with tasks({}/{}):".format(
                                                                                                                                                            user["name"], len(completed), len(todos)))

                                                                                                                                                    # Print each completed task with indentation
                                                                                                                                                        for task in completed:
                                                                                                                                                                    print("\t {}".format(task))

