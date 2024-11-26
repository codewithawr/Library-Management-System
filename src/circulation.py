import datetime
from utils import calculate_due_date, calculate_fine, print_book_details, generate_id
import pandas as pd

class Circulation:
    def __init__(self, book_manager, user_manager, data_file="data/circulation.csv"):
        self.book_manager = book_manager
        self.user_manager = user_manager
        self.circulation_data = []  # List to store circulation records
        self.data_file = data_file
        self.load_circulation_data()  # Load data from the CSV file

    def load_circulation_data(self):
        """
        Loads circulation data from the CSV file.
        """
        try:
            df = pd.read_csv(self.data_file)
            for index, row in df.iterrows():
                record = {
                    "circulation_id": row['circulation_id'],
                    "book_id": row['book_id'],
                    "user_id": row['user_id'],
                    "checkout_date": datetime.datetime.strptime(row['checkout_date'], '%Y-%m-%d').date(),
                    "due_date": datetime.datetime.strptime(row['due_date'], '%Y-%m-%d').date(),
                    "return_date": datetime.datetime.strptime(row['return_date'], '%Y-%m-%d').date() if pd.notna(row['return_date']) else None
                }
                self.circulation_data.append(record)
        except FileNotFoundError:
            pass  # Ignore if the file doesn't exist

    def save_circulation_data(self):
        """
        Saves circulation data to the CSV file.
        """
        circulation_records = []
        for record in self.circulation_data:
            record_data = record.copy()  # Create a copy to avoid modifying the original
            # Convert dates to strings for saving in CSV
            record_data['checkout_date'] = record_data['checkout_date'].strftime('%Y-%m-%d')
            record_data['due_date'] = record_data['due_date'].strftime('%Y-%m-%d')
            record_data['return_date'] = record_data['return_date'].strftime('%Y-%m-%d') if record_data['return_date'] else None
            circulation_records.append(record_data)
        df = pd.DataFrame(circulation_records)
        df.to_csv(self.data_file, index=False)

    def check_out_book(self, user_id=None):
        """
        Allows a user to check out a book.
        """
        book_id = input("Enter book ID to check out: ")
        book = self.book_manager.find_book_by_id(book_id)
        if book:
            if book.available_copies > 0:
                if not user_id:
                    user_id = input("Enter user ID: ")
                user = self.user_manager.find_user_by_id(user_id)
                if user:
                    circulation_id = generate_id()
                    checkout_date = datetime.date.today()
                    due_date = calculate_due_date(user.user_type, checkout_date)
                    record = {
                        "circulation_id": circulation_id,
                        "book_id": book_id,
                        "user_id": user_id,
                        "checkout_date": checkout_date,
                        "due_date": due_date,
                        "return_date": None  # Set to None initially
                    }
                    self.circulation_data.append(record)
                    book.available_copies -= 1
                    self.book_manager.save_books()
                    self.save_circulation_data()  # Save circulation data to CSV
                    print(f"Book checked out successfully! Due date: {due_date}")
                else:
                    print("User not found.")
            else:
                print("No available copies of this book.")
        else:
            print("Book not found.")

    def return_book(self):
        """
        Allows a user to return a book.
        """
        book_id = input("Enter book ID to return: ")
        user_id = input("Enter user ID: ")
        for record in self.circulation_data:
            if record["book_id"] == book_id and record["user_id"] == user_id and record["return_date"] is None:
                return_date = datetime.date.today()
                record["return_date"] = return_date
                book = self.book_manager.find_book_by_id(book_id)
                if book:
                    book.available_copies += 1
                    self.book_manager.save_books()
                    user = self.user_manager.find_user_by_id(user_id)
                    if user:
                        fine = calculate_fine(user.user_type, record["due_date"], return_date)
                        if fine > 0:
                            print(f"Overdue fine: ${fine:.2f}")
                            self.user_manager.add_fine(user_id, fine)
                        else:
                            print("Book returned successfully! No fine.")
                    else:
                        print("User not found.")  # This shouldn't happen, but handle it just in case
                else:
                    print("Book not found.")  # This also shouldn't happen
                self.save_circulation_data()  # Save circulation data to CSV
                return  # Exit the loop after finding the record
        print("No outstanding record found for this book and user.")

    def renew_book(self):
        """
        Allows a user to renew a book (extend the due date),
        with a limit on the number of renewals or a check for overdue status.
        """
        book_id = input("Enter book ID to renew: ")
        user_id = input("Enter user ID: ")
        user = self.user_manager.find_user_by_id(user_id)
        if user:
            for record in self.circulation_data:
                if record["book_id"] == book_id and record["user_id"] == user_id and record["return_date"] is None:
                    # Check for renewal limit or overdue status
                    if "renewals" not in record:
                        record["renewals"] = 0
                    if record["renewals"] < 2 and record["due_date"] >= datetime.date.today():  # Example: Limit 2 renewals, not overdue
                        due_date = calculate_due_date(user.user_type, record["checkout_date"], renew=True)
                        record["due_date"] = due_date
                        record["renewals"] += 1
                        self.save_circulation_data()  # Save circulation data to CSV
                        print(f"Book renewed successfully! New due date: {due_date}")
                    else:
                        print("Renewal limit reached or book is overdue.")
                    return
        else:
            print("User not found.")
        print("No outstanding record found for this book and user.")
        
    def view_borrowed_books(self, user_id=None):
        """
        Displays a all borrowed books.
        """
        if user_id == None:
            user_id = input("Enter user ID: ")
        for record in self.circulation_data:
            if record["return_date"] is None:
                book = self.book_manager.find_book_by_id(record["book_id"])
                if book:
                    user = self.user_manager.find_user_by_id(record["user_id"])
                    if user_id != "" and user_id != user.user_id:
                        continue
                    print_book_details(vars(book))
                    print(f"Borrower: {user.name} ({user.user_id})")
                    print("-" * 10)
                    print(f"Checkout Date: {record['checkout_date']}")
                    print(f"Due Date: {record['due_date']}")
                    print(f"Return Date: {record['return_date']}")
                    print("-" * 30)
                    
        print("End of borrowed books.")

    def add_borrow_record(self):
        """
        Allows an employee to manually add a borrow record.
        """
        circulation_id = generate_id()
        book_id = input("Enter book ID: ")
        user_id = input("Enter user ID: ")

        try:
            checkout_date_str = input("Enter checkout date (YYYY-MM-DD): ")
            checkout_date = datetime.datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
            due_date_str = input("Enter due date (YYYY-MM-DD): ")
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        record = {
            "circulation_id": circulation_id,
            "book_id": book_id,
            "user_id": user_id,
            "checkout_date": checkout_date,
            "due_date": due_date,
            "return_date": None
        }
        self.circulation_data.append(record)
        self.save_circulation_data()
        print("Borrow record added successfully!")

    def view_borrowing_history(self, user_id):
        """
        Displays a user's borrowing history.
        """
        for record in self.circulation_data:
            if record["user_id"] == user_id:
                book = self.book_manager.find_book_by_id(record["book_id"])
                if book:
                    print_book_details(book)
                    print(f"Checkout Date: {record['checkout_date']}")
                    print(f"Due Date: {record['due_date']}")
                    print(f"Return Date: {record['return_date']}")
                    print("-" * 20)
        print("End of borrowing history.")
    def view_total_fines(self, user_id):
        """
        Displays a user's total fines. use calculate_fine
        """
        total_fine = 0
        for record in self.circulation_data:
            if record["user_id"] == user_id and record["return_date"] is not None:
                user = self.user_manager.find_user_by_id(user_id)
                fine = calculate_fine(user.user_type, record["due_date"], record["return_date"])
                total_fine += fine
        user = self.user_manager.find_user_by_id(user_id)
        print(f"Total fines for {user.name}: ${total_fine:.2f}")