# book_management.py
import pandas as pd
from utils import clear_screen, validate_isbn, generate_id, print_book_details

class Node:
    def __init__(self, book):
        self.book = book
        self.prev = None
        self.next = None

class Book:
    def __init__(self, book_id, title, author, isbn, publication_year, genre, total_copies, available_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = available_copies

    def __str__(self):
        return f"Book ID: {self.book_id}, Title: {self.title}, Author: {self.author}"

class BookManager:
    def __init__(self, books=None, data_file="data/BooksDataset.csv"):
        self.data_file = data_file
        self.head = None
        self.tail = None
        if books is not None:
            for book in books:
                self.add_book_node(book)

    def load_books(self):
        """
        Loads book data from the CSV file.
        """
        try:
            df = pd.read_csv(self.data_file)
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
            return []

    def save_books(self):
        """
        Saves book data to the CSV file.
        """
        books = []
        current = self.head
        while current:
            books.append(vars(current.book))
            current = current.next
        df = pd.DataFrame(books)
        df.to_csv(self.data_file, index=False)

    def add_book_node(self, book):
        """
        Adds a new book node to the end of the linked list.
        """
        new_node = Node(book)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def add_book(self):
        """
        Adds a new book to the system.
        """
        book_id = input("Enter book ID (leave blank to auto-generate): ")
        if not book_id:
            book_id = generate_id()

        title = input("Enter title: ")
        author = input("Enter author: ")
        isbn = input("Enter ISBN: ")
        publication_year = input("Enter publication year: ")
        genre = input("Enter genre: ")

        while True:
            try:
                total_copies = int(input("Enter total copies: "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")

        available_copies = total_copies  # Initially, all copies are available

        if not validate_isbn(isbn):
            print("Invalid ISBN format.")
            return

        book = Book(book_id, title, author, isbn, publication_year, genre, total_copies, available_copies)
        self.add_book_node(book)
        self.save_books()
        print("Book added successfully!")

    def find_book(self):
        """
        Finds a book by its ID, title, or ISBN.
        """
        search_term = input("Enter book ID, title, or ISBN to search: ")
        found_books = []
        current = self.head
        while current:
            if (search_term.lower() in str(current.book.book_id).lower() or
                search_term.lower() in str(current.book.title).lower() or
                search_term.lower() in str(current.book.isbn).lower()):
                found_books.append(current.book)
            current = current.next

        if found_books:
            for book in found_books:
                print_book_details(vars(book))
        else:
            print("Book not found.")

    def update_book(self):
        """
        Updates an existing book's information.
        """
        book_id = input("Enter book ID to update: ")
        current = self.head
        while current:
            if current.book.book_id == book_id:
                title = input("Enter updated title (leave blank to keep current): ")
                author = input("Enter updated author (leave blank to keep current): ")
                isbn = input("Enter updated ISBN (leave blank to keep current): ")
                publication_year = input("Enter updated publication year (leave blank to keep current): ")
                genre = input("Enter updated genre (leave blank to keep current): ")

                if isbn and not validate_isbn(isbn):
                    print("Invalid ISBN format.")
                    return

                if title:
                    current.book.title = title
                if author:
                    current.book.author = author
                if isbn:
                    current.book.isbn = isbn
                if publication_year:
                    current.book.publication_year = publication_year
                if genre:
                    current.book.genre = genre

                self.save_books()
                print("Book updated successfully!")
                return
            current = current.next
        print("Book not found.")

    def delete_book(self):
        """
        Deletes a book from the system.
        """
        book_id = input("Enter book ID to delete: ")
        current = self.head
        while current:
            if current.book.book_id == book_id:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                # Set the next and prev pointers of the deleted node to None
                current.next = None  
                current.prev = None  

                self.save_books()
                print("Book deleted successfully!")
                return
            current = current.next
        print("Book not found.")

    def find_book_by_id(self, book_id):
        """
        Helper function to find a book by its ID.
        """
        current = self.head
        while current:
            if current.book.book_id == book_id:
                return current.book
            current = current.next
        return None

    def display_books(self):
        """
        Displays all books in the system.
        """
        current = self.head
        while current:
            print_book_details(vars(current.book))
            current = current.next
if __name__ == "__main__":
    book_manager = BookManager()
    book_manager.add_book()
    book_manager.find_book()
    book_manager.update_book()