import datetime
import re
import bcrypt

def validate_isbn(isbn):
    """
    Checks if an ISBN-10 or ISBN-13 is valid.
    """
    isbn = isbn.replace("-", "").replace(" ", "")  # Remove hyphens and spaces
    if len(isbn) == 10:
        # ISBN-10 validation
        if not isbn[:-1].isdigit() or not (isbn[-1].isdigit() or isbn[-1] == 'X'):
            return False
        check_digit = 10 if isbn[-1] == 'X' else int(isbn[-1])
        total = sum((10 - i) * int(digit) for i, digit in enumerate(isbn[:-1]))
        return (total + check_digit) % 11 == 0
    elif len(isbn) == 13:
        # ISBN-13 validation
        if not isbn.isdigit():
            return False
        total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(isbn[:-1]))
        check_digit = (10 - (total % 10)) % 10
        return int(isbn[-1]) == check_digit
    return False


def validate_date(date_str):
    """
    Validates a date string in YYYY-MM-DD format.
    """
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_email(email):
    """
    Checks if an email address is in a valid format using a regular expression.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def format_date(date_obj):
    """
    Formats a date object as YYYY-MM-DD.
    """
    return date_obj.strftime("%Y-%m-%d")


def parse_date(date_str):
    """
    Parses a date string in YYYY-MM-DD format to a date object.
    """
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def search_list(data_list, search_term, key):
    """
    Searches a list of dictionaries or objects for a given search term.
    """
    results = []
    for item in data_list:
        if search_term.lower() in str(item[key]).lower():  # Case-insensitive search
            results.append(item)
    return results


def filter_list(data_list, filter_criteria):
    """
    Filters a list of items based on given criteria (a dictionary of key-value pairs).
    """
    results = []
    for item in data_list:
        match = True
        for key, value in filter_criteria.items():
            if item[key] != value:
                match = False
                break
        if match:
            results.append(item)
    return results


def generate_id():
    """
    Generates a unique ID (you might want to use a more robust method in a real system).
    """
    import uuid
    return str(uuid.uuid4())


def calculate_fine(due_date, return_date):
    """
    Calculates overdue fines (replace with your library's fine calculation logic).
    """
    # Example: Fine of $0.25 per day overdue
    days_overdue = (return_date - due_date).days
    if days_overdue > 0:
        return 0.25 * days_overdue
    return 0.0


def display_menu(options):
    """
    Displays a menu of options to the user and gets their choice.
    """
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def clear_screen():
    """
    Clears the console screen (OS-specific).
    """
    import os
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')


def calculate_due_date(borrower_type, checkout_date):
  """
  Calculates the due date for a book based on the borrower type.
  """
  if borrower_type == "faculty":
    due_date = checkout_date + datetime.timedelta(days=28)  # Faculty: 28 days
  elif borrower_type == "student":
    due_date = checkout_date + datetime.timedelta(days=14)  # Students: 14 days
  elif borrower_type == "outsider":
    due_date = checkout_date + datetime.timedelta(days=7)  # Outsiders: 7 days
  else:
    raise ValueError("Invalid borrower type.") 
  return due_date


def calculate_fine(borrower_type, due_date, return_date):
  """
  Calculates overdue fines based on borrower type and due date.
  """
  days_overdue = (return_date - due_date).days
  if days_overdue > 0:
    if borrower_type == "faculty":
      fine = 0.10 * days_overdue  # Faculty: $0.10 per day
    elif borrower_type == "student":
      fine = 0.25 * days_overdue  # Students: $0.25 per day
    elif borrower_type == "outsider":
      fine = 0.50 * days_overdue  # Outsiders: $0.50 per day
    else:
      raise ValueError("Invalid borrower type.")
    return fine
  return 0.0 


def print_book_details(book):
  """
  Prints book details in a consistent format.
  """
  print("-" * 30)
  try:
    print("Book ID:", book.book_id)
    print("Title:", book.title)
    print("Author(s):", book.author)
    print("ISBN:", book.isbn)
    print("Publication Year:", book.publication_year)
    print("Genre:", book.genre)
    print("Available Copies:", book.available_copies)
  except AttributeError:
    print("Book ID:", book["book_id"])
    print("Title:", book["title"])
    print("Author(s):", book["author"])
    print("ISBN:", book["isbn"])
    print("Publication Year:", book["publication_year"])
    print("Genre:", book["genre"])
    print("Available Copies:", book["available_copies"])


def print_user_details(user):
  """
  Prints user details in a consistent format.
  """
  print("-" * 30)

  try:
    print("User ID:", user["user_id"])
    print("Name:", user["name"])
    print("Address:", user["address"])
    print("Contact:", user["contact"])
    print("User Type:", user["user_type"])
    print("Fines:", user["total_fine"])  
  except:
    print("User ID:", user.user_id)
    print("Name:", user.name)
    print("Address:", user.address)
    print("Contact:", user.contact)
    print("User Type:", user.user_type)
    print("Fines:", user.total_fine)

  print("-" * 30)

def print_employee_details(employee):
  """
  Prints employee details in a consistent format with more information.
  """
  print("-" * 30)
  print("Employee ID:", employee["employee_id"])
  print("Name:", employee["name"])
  print("Address:", employee["address"])
  print("Contact:", employee["contact"])
  print("Email:", employee["email"])
  print("Position:", employee["position"])
  print("-" * 30)


def print_circulation_record(record):
  """
  Prints circulation record details in a consistent format.
  """
  print("-" * 30)
  print("Book Title:", record["book_title"])
  print("User Name:", record["user_name"])
  print("Checkout Date:", record["checkout_date"])
  print("Due Date:", record["due_date"])
  print("Return Date:", record["return_date"] if record["return_date"] else "Not returned")
  print("-" * 30)


def hash_password(password):
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def check_password(password, hashed_password=str): 
    """Checks if a password matches a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
