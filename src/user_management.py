from utils import hash_password, validate_email, generate_id, print_user_details, calculate_fine, calculate_due_date
import pandas as pd

class User:
    def __init__(self, user_id, name, address, contact, email, user_type, hashed_password, total_fine=0.0):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.contact = contact
        self.email = email
        self.user_type = user_type  # Add user_type attribute
        self.total_fine = total_fine
        self.hashed_password = hashed_password

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Type: {self.user_type}, Total Fine: {self.total_fine}"

class UserManager:
    def __init__(self, users=None, data_file="data/UserDataset.csv"):  # Update __init__
        if users is None:
            users = []
        self.data_file = data_file
        self.users = users  # Initialize with the provided list of users
        self.valid_user_types = ("student", "faculty", "outsider")

    def load_users(self):
        """
        Loads user data from the CSV file, including user_type.
        """
        try:
            df = pd.read_csv(self.data_file)
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
            return []

    def save_users(self):
        """
        Saves user data to the CSV file, including user_type.
        """
        df = pd.DataFrame([vars(user) for user in self.users])
        df.to_csv(self.data_file, index=False)

    def pay_fine(self, user_id=None): 
        """
        Allows a user to pay their fine.
        """
        if not user_id:
            user_id = input("Enter user ID to pay fine: ")
        user = self.find_user_by_id(user_id)
        if user:
            if user.total_fine > 0:
                print(f"Current fine: ${user.total_fine:.2f}")
                while True:
                    try:
                        amount = float(input("Enter amount to pay: $"))
                        if 0 < amount <= user.total_fine:
                            user.total_fine -= amount
                            self.save_users()
                            print(f"Payment successful! Remaining fine: ${user.total_fine:.2f}")
                            break
                        else:
                            print("Invalid amount. Please enter an amount between 0 and your total fine.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print("You have no outstanding fines.")
        else:
            print("User not found.")

    def add_fine(self, user_id, amount):
        """
        Adds a fine to the user's total_fine.
        """
        user = self.find_user_by_id(user_id)
        if user:
            user.total_fine += amount
            self.save_users()
            print(f"Fine added. New total fine for {user.name}: ${user.total_fine:.2f}")
        else:
            print("User not found.")

    def add_user(self):
        """
        Adds a new user to the system. 
        Asks for user ID and auto-fills only if it's empty.
        """
        user_id = input("Enter user ID (leave blank to auto-generate): ")
        if not user_id:
            user_id = generate_id() 

        name = input("Enter user name: ")
        address = input("Enter user address: ")
        contact = input("Enter user contact: ")
        email = input("Enter user email: ")
        password = input("Enter password: ")  # Get password input
        hashed_password = hash_password(password)

        while True:
            user_type = input("Enter user type (student, faculty, outsider): ").lower()
            if user_type in self.valid_user_types:
                break
            else:
                print("Invalid user type. Please choose from: student, faculty, outsider")

        if not validate_email(email):
            print("Invalid email format.")
            return

        user = User(user_id, name, address, contact, email, user_type, 
                    hashed_password, total_fine=0.0)
        self.users.append(user)
        self.save_users()
        print("User added successfully!")

    def find_user(self):
        """
        Finds a user by their ID or name. and if blank returns all users.
        """
        search_query = input("Enter user ID or name to search (leave blank to show all users): ")
        if not search_query:
            for user in self.users:
                print_user_details(user)
        else:
            user = self.find_user_by_id(search_query)
            if not user:
                user = self.find_user_by_name(search_query)
            if user:
                print_user_details(user)
            else:
                print("User not found.")

    def update_user(self, user_id=None):  # Add user_id as parameter
        """
        Updates an existing user's information.
        Handles the case where the email is not provided.
        """
        if not user_id:
            user_id = input("Enter user ID to update: ")
        user = self.find_user_by_id(user_id)
        if user:
            name = input("Enter updated name (leave blank to keep current): ")
            address = input("Enter updated address (leave blank to keep current): ")
            contact = input("Enter updated contact (leave blank to keep current): ")
            email = input("Enter updated email (leave blank to keep current): ")

            if email and not validate_email(email):  # Validate only if email is provided
                print("Invalid email format.")
                return

            # Update user information only if new values are provided
            if name:
                user.name = name
            if address:
                user.address = address
            if contact:
                user.contact = contact
            if email:
                user.email = email

            self.save_users()
            print("User updated successfully!")
        else:
            print("User not found.")

    def delete_user(self):
        """
        Deletes a user from the system.
        """
        user_id = input("Enter user ID to delete: ")
        user = self.find_user_by_id(user_id)
        if user:
            self.users.remove(user)
            self.save_users()
            print("User deleted successfully!")
        else:
            print("User not found.")

    def find_user_by_id(self, user_id):
        """
        Helper function to find a user by their ID.
        """
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def find_user_by_email(self, email):
        """
        Finds a user by their email address.
        """
        for user in self.users:
            if user.email == email:
                return user
        return None

# Example usage in main.py:
if __name__ == "__main__":
    user_manager = UserManager(data_file="../data/UserDataset.csv")
    user_manager.add_user()
    user_manager.find_user()
    user_manager.update_user()
    user_manager.delete_user()