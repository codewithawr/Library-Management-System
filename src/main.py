from book_management import BookManager
from user_management import UserManager
from employee_management import EmployeeManager
from circulation import Circulation
from data_loader import DataLoader
from utils import display_menu, clear_screen, check_password

def login(user_manager, employee_manager):
    """
    Handles the login process for both users and employees,
    allowing login with either email or ID.
    """
    while True:
        user_type = input("Are you a user (u) or an employee (e)? ").lower()
        if user_type in ('u', 'e'):
            break
        else:
            print("Invalid choice. Please enter 'u' for user or 'e' for employee.")

    username = input("Enter your ID or email: ")
    password = input("Enter your password: ")

    if user_type == 'u':
        user = user_manager.find_user_by_id(username) or user_manager.find_user_by_email(username)
        print(user)
        if user and check_password(password, user.hashed_password):
            return user, "user"
        else:
            print("Invalid user ID/email or password.")
            return None, None
    elif user_type == 'e':
        employee = employee_manager.find_employee_by_id(username) or employee_manager.find_employee_by_email(username)
        if employee and check_password(password, employee.hashed_password):
            return employee, "employee"
        else:
            print("Invalid employee ID/email or password.")
            return None, None

def main():
    """
    Main function to run the library management system.
    """
    data_loader = DataLoader()
    book_manager = BookManager(data_loader.load_books())
    user_manager = UserManager(data_loader.load_users())
    employee_manager = EmployeeManager(data_loader.load_employees())
    circulation_manager = Circulation(book_manager, user_manager)

    # Login
    user, user_type = login(user_manager, employee_manager)
    if not user:
        return  # Exit if login fails

    while True:
        clear_screen()
        print("\nLibrary Management System")
        print("-" * 25)

        if user_type == "user":
            main_menu_options = [
                "Book Search",
                "Borrow Book",
                "My Account",
                "Exit"
            ]
            choice = display_menu(main_menu_options)

            if choice == 1:
                book_manager.find_book()  # Allow users to search for books
                input("Press Enter to continue...")
            elif choice == 2:
                circulation_manager.check_out_book(user.user_id)  # User can borrow books
                input("Press Enter to continue...")
            elif choice == 3:
                # My Account functionality for users
                while True:
                    clear_screen()
                    print("\nMy Account")
                    print("-" * 20)
                    account_menu_options = [
                        "View Borrowed Books",
                        "View Borrowing History",  # New option
                        "Totel Fines",
                        "Update Account Information",  # New option
                        "Back to Main Menu"
                    ]
                    account_choice = display_menu(account_menu_options)

                    if account_choice == 1:
                        circulation_manager.view_borrowed_books(user.user_id)
                    elif account_choice == 2:
                        circulation_manager.view_borrowing_history(user.user_id)
                    elif account_choice == 3:
                        circulation_manager.view_total_fines(user.user_id)
                    elif account_choice == 4:
                        user_manager.update_user(user.user_id)  # Pass user_id here
                    elif account_choice == 5:
                        break
                    else:
                        print("Invalid choice.")
                    input("Press Enter to continue...")
            elif choice == 4:
                print("Exiting Library Management System...")
                break
            else:
                print("Invalid choice.")
            input("Press Enter to continue...")

        elif user_type == "employee":
            main_menu_options = [
                "Book Management",
                "User Management",
                "Employee Management",
                "Circulation Management",
                "Exit"
            ]
            choice = display_menu(main_menu_options)

            if choice == 1:
                # Book Management Menu
                while True:
                    clear_screen()
                    print("\nBook Management")
                    print("-" * 20)
                    book_menu_options = [
                        "Add Book",
                        "Find Book",
                        "Update Book",
                        "Delete Book",
                        "Back to Main Menu"
                    ]
                    book_choice = display_menu(book_menu_options)

                    if book_choice == 1:
                        book_manager.add_book()
                    elif book_choice == 2:
                        book_manager.find_book()
                    elif book_choice == 3:
                        book_manager.update_book()
                    elif book_choice == 4:
                        book_manager.delete_book()
                    elif book_choice == 5:
                        break
                    else:
                        print("Invalid choice.")
                    input("Press Enter to continue...")

            elif choice == 2:
                # User Management Menu
                while True:
                    clear_screen()
                    print("\nUser Management")
                    print("-" * 20)
                    user_menu_options = [
                        "Add User",
                        "Find User",
                        "Update User",
                        "Delete User",
                        "Pay Fine",
                        "Back to Main Menu"
                    ]
                    user_choice = display_menu(user_menu_options)

                    if user_choice == 1:
                        user_manager.add_user()
                    elif user_choice == 2:
                        user_manager.find_user()
                    elif user_choice == 3:
                        user_manager.update_user()
                    elif user_choice == 4:
                        user_manager.delete_user()
                    elif user_choice == 5:
                        user_manager.pay_fine()
                    elif user_choice == 6:
                        break
                    else:
                        print("Invalid choice.")
                    input("Press Enter to continue...")

            elif choice == 3:
                # Employee Management Menu
                while True:
                    clear_screen()
                    print("\nEmployee Management")
                    print("-" * 20)
                    employee_menu_options = [
                        "Add Employee",
                        "Find Employee",
                        "Update Employee",
                        "Delete Employee",
                        "Back to Main Menu"
                    ]
                    employee_choice = display_menu(employee_menu_options)

                    if employee_choice == 1:
                        employee_manager.add_employee()
                    elif employee_choice == 2:
                        employee_manager.find_employee()
                    elif employee_choice == 3:
                        employee_manager.update_employee()
                    elif employee_choice == 4:
                        employee_manager.delete_employee()
                    elif employee_choice == 5:
                        break
                    else:
                        print("Invalid choice.")
                    input("Press Enter to continue...")

            elif choice == 4:
                # Circulation Management Menu
                while True:
                    clear_screen()
                    print("\nCirculation Management")
                    print("-" * 20)
                    circulation_menu_options = [
                        "Check Out Book",
                        "Return Book",
                        "View Borrowed Books",
                        "Back to Main Menu"
                    ]
                    circulation_choice = display_menu(circulation_menu_options)

                    if circulation_choice == 1:
                        circulation_manager.check_out_book()
                    elif circulation_choice == 2:
                        circulation_manager.return_book()
                    elif circulation_choice == 3:
                        circulation_manager.view_borrowed_books() 
                    elif circulation_choice == 4:
                        break
                    else:
                        print("Invalid choice.")
                    input("Press Enter to continue...")
            elif choice == 5:
                print("Exiting Library Management System...")
                break
            else:
                print("Invalid choice.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()