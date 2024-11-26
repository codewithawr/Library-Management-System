import pandas as pd
from utils import validate_email, generate_id, print_employee_details, hash_password, clear_screen

class Employee:
    def __init__(self, employee_id, name, address, contact, email, position, hashed_password):
        self.employee_id = employee_id
        self.name = name
        self.address = address
        self.contact = contact
        self.email = email
        self.position = position 
        self.hashed_password = hashed_password

    def __str__(self):
        return f"Employee ID: {self.employee_id}, Name: {self.name}, Position: {self.position}"

class EmployeeManager:
    def __init__(self, employees=None, data_file="data/EmployeesDataset.csv"):  # Update __init__
        if employees is None:
            employees = []
        self.data_file = data_file
        self.employees = employees  # Initialize with the provided list of employees

    def load_employees(self):
        """
        Loads employee data from the CSV file, including hashed passwords.
        """
        try:
            df = pd.read_csv(self.data_file)
            employees = []
            for index, row in df.iterrows():
                employee = Employee(
                    row['employee_id'], row['name'], row['address'], 
                    row['contact'], row['email'], row['position'],
                    row['hashed_password'] 
                )
                employees.append(employee)
            return employees
        except FileNotFoundError:
            return []

    def save_employees(self):
        """
        Saves employee data to the CSV file, including hashed passwords.
        """
        df = pd.DataFrame([vars(employee) for employee in self.employees])
        df.to_csv(self.data_file, index=False)

    def add_employee(self):
        """
        Adds a new employee to the system, hashing the password.
        """
        employee_id = input("Enter employee ID (leave blank to auto-generate): ")
        if not employee_id:
            employee_id = generate_id()

        name = input("Enter employee name: ")
        address = input("Enter employee address: ")
        contact = input("Enter employee contact: ")
        email = input("Enter employee email: ")
        position = input("Enter employee position: ")
        password = input("Enter password: ")  # Get password input
        
        # Hash the password
        hashed_password = hash_password(password)

        if not validate_email(email):
            print("Invalid email format.")
            return

        employee = Employee(employee_id, name, address, contact, email, position, hashed_password)
        self.employees.append(employee)
        self.save_employees()
        print("Employee added successfully!")
    
    
    def find_employee(self):
        """
        Finds an employee by their ID or name.
        If the search term is empty, shows all employees with pagination.
        """
        search_term = input("Enter employee ID or name to search (leave blank to show all): ")
        if search_term == "":
            # Show all employees with pagination
            clear_screen()  # Clear the screen only once at the beginning
            print("\nAll Employees:")
            print("-" * 20)
            for i, employee in enumerate(self.employees):
                print_employee_details(vars(employee))

        else:
            # Search for employees based on the search term
            found_employees = [
                employee for employee in self.employees
                if search_term.lower() in str(employee.employee_id).lower()
                or search_term.lower() in str(employee.name).lower()
            ]
            if found_employees:
                for employee in found_employees:
                    print_employee_details(vars(employee))
            else:
                print("Employee not found.")
    def update_employee(self):
        """
        Updates an existing employee's information.
        """
        employee_id = input("Enter employee ID to update: ")
        employee = self.find_employee_by_id(employee_id)
        if employee:
            name = input("Enter updated name (leave blank to keep current): ")
            address = input(
                "Enter updated address (leave blank to keep current): ")
            contact = input(
                "Enter updated contact (leave blank to keep current): ")
            email = input("Enter updated email (leave blank to keep current): ")
            position = input("Enter updated position (leave blank to keep current): ")

            if email and not validate_email(email):
                print("Invalid email format.")
                return

            if name:
                employee.name = name
            if address:
                employee.address = address
            if contact:
                employee.contact = contact
            if email:
                employee.email = email
            if position:
                employee.position = position

            self.save_employees()
            print("Employee updated successfully!")
        else:
            print("Employee not found.")

    def delete_employee(self):
        """
        Deletes an employee from the system.
        """
        employee_id = input("Enter employee ID to delete: ")
        employee = self.find_employee_by_id(employee_id)
        if employee:
            self.employees.remove(employee)
            self.save_employees()
            print("Employee deleted successfully!")
        else:
            print("Employee not found.")

    def find_employee_by_id(self, employee_id):
        """
        Helper function to find an employee by their ID.
        """
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee
        return None
    def find_employee_by_email(self, email):
        """
        Finds an employee by their email address.
        """
        for employee in self.employees:
            if employee.email == email:
                return employee
        return None

# Example usage in main.py:
if __name__ == "__main__":
    employee_manager = EmployeeManager()
    employee_manager.add_employee()
    employee_manager.find_employee()
    employee_manager.update_employee()
    employee_manager.delete_employee()
