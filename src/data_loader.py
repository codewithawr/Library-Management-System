import pandas as pd
from book_management import Book  # Assuming you have a Book class in book_management.py
from user_management import User  # Assuming you have a User class in user_management.py
from employee_management import Employee  # Assuming you have an Employee class in employee_management.py

class DataLoader:
    def __init__(self, books_file="data/BooksDataset.csv", users_file="data/UserDataset.csv", employees_file="data/EmployeesDataset.csv"):
        self.books_file = books_file
        self.users_file = users_file
        self.employees_file = employees_file

    def load_books(self):
        """
        Loads book data from the CSV file into a list of Book objects.
        """
        try:
            df = pd.read_csv(self.books_file)
            books = []
            for index, row in df.iterrows():
                book = Book(
                    row['book_id'], row['title'], row['author'], row['isbn'],
                    row['publication_year'], row['genre'], row['total_copies'],
                    row['available_copies']
                )
                books.append(book)
            return books
        except FileNotFoundError:
            print(f"Error: Books dataset file not found at {self.books_file}")
            return []

    def load_users(self):
        """
        Loads user data from the CSV file into a list of User objects.
        """
        try:
            df = pd.read_csv(self.users_file)
            users = []
            for index, row in df.iterrows():
                user = User(
                    row['user_id'], row['name'], row['address'],
                    row['contact'], row['email'], row['user_type'],
                    row['hashed_password'], row['total_fine']  # Include total_fine
                )
                users.append(user)
            return users
        except FileNotFoundError:
            print(f"Error: Users dataset file not found at {self.users_file}")
            return []

    def load_employees(self):
        """
        Loads employee data from the CSV file into a list of Employee objects.
        """
        try:
            df = pd.read_csv(self.employees_file)
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
            print(f"Error: Employees dataset file not found at {self.employees_file}")
            return []