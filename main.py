import random
import sqlite3
from faker import Faker
from datetime import datetime

author_num = 500
book_num = 1000

#  Create "authors" table
def create_authors_table(cursor):
    query = '''
    CREATE TABLE IF NOT EXISTS authors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birth_date TEXT,
            birth_place TEXT)'''
    cursor.execute(query)

#  Create "books" table
def create_books_table(cursor):
    query = '''
    CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            pages INTEGER NOT NULL,
            release_date TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY(author_id) REFERENCES authors(id)
            )'''
    cursor.execute(query)

#  Insert fake author data into the "authors" table
def insert_into_authors(cursor, fake, count: int = 500):
    for _ in range(count):
        fake_first_name = fake.first_name()
        fake_last_name = fake.last_name()
        fake_birthday = fake.date_of_birth(minimum_age=15, maximum_age=100).strftime("%Y-%m-%d")
        fake_birthplace = fake.country()
        insert_query = '''
            INSERT INTO authors (first_name, last_name, birth_date, birth_place) 
            VALUES (?, ?, ?, ?)
            '''
        cursor.execute(insert_query, (fake_first_name, fake_last_name, str(fake_birthday), fake_birthplace))


#  Insert fake book data into the "books" table
def insert_into_books(cursor, fake: Faker, count: int = 1000):
    # Random categories for books
    categories = ["Comedy", "Drama", "Horror", "Thriller", "Romance", "Fantasy",
                  "Mystery", "Adventure", "Science Fiction"]
    # loop that adds data into the table
    for _ in range(count):
        fake_book_title = fake.sentence(nb_words=4).replace('.', ' ').title()
        fake_category = random.choice(categories)
        fake_pages = random.randint(100, 300)
        fake_release_date = fake.date_between(start_date="-50y", end_date="-10y")
        fake_author_id = random.randint(1, 500)
        insert_query = '''
        INSERT INTO books (title, category, pages, release_date, author_id) 
        VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(insert_query,
                       (fake_book_title, fake_category, fake_pages, str(fake_release_date), fake_author_id))

# Select books with most pages
def fetch_books_with_most_pages(cursor):
    cursor.execute('''
    SELECT * 
    FROM books 
    WHERE pages = (SELECT MAX(pages) FROM books)
    ''')
    rows = cursor.fetchall()
    print("Books with most pages: \n")
    print(f"{'ID':<5}{'Title':<40}{'Category':<20}{'Pages':<10}{'Release Date':<15}{'Author ID':<10}")
    print("-" * 100)
    for row in rows:
        print(f"{row[0]:<5}{row[1]:<40}{row[2]:<20}{row[3]:<10}{row[4]:<15}{row[5]:<10}")

# Select average page amount in a book
def fetch_average_page_number(cursor):
    cursor.execute('''
    SELECT AVG(pages) 
    FROM books
    ''')
    print(f"\nAverage pages: {round(cursor.fetchall()[0][0])}\n")

# Select the youngest author
def fetch_youngest_author(cursor):
    cursor.execute('''
    SELECT first_name, last_name, birth_date 
    FROM authors 
    WHERE birth_date = (SELECT MAX(birth_date) FROM authors)
    ''')
    author = cursor.fetchall()[0]
    birth_date = datetime.strptime(author[2], "%Y-%m-%d")  # Convert birth_date string to datetime object
    current_date = datetime.today()  # Get current date
    age = current_date.year - birth_date.year - (
    (current_date.month, current_date.day) < (birth_date.month, birth_date.day))  # Age calculation
    print(f"Youngest Author - {author[0]} {author[1]}, aged {age}")


# Select 10 authors who have no books in the database
# Only 10 because there's just too many
def fetch_authors_with_no_books(cursor):
    cursor.execute('''
    SELECT first_name, last_name 
    FROM authors 
    WHERE id NOT IN (SELECT author_id FROM books)
    ''')
    print("\nAuthors with no books in the database: \n")
    for row in cursor.fetchmany(10):
        print(f"{row[0]} {row[1]}")

# Select 5 authors who have 3+ books

def fetch_more_than_3_book_authors(cursor):
    cursor.execute('''
    SELECT authors.first_name, authors.last_name, COUNT(books.id) as book_count
    FROM authors 
    JOIN books ON authors.id = books.author_id
    GROUP BY authors.id
    HAVING COUNT(books.id) > 3
    ''')
    print("\n5 Authors with more than 3 books: \n")
    for row in cursor.fetchmany(5):
        print(f"{row[0]} {row[1]} - {row[2]} books")

# Main function to connect to the SQLite database and run various data queries
def main():
    # Initialize a database connection
    conn = sqlite3.connect('books.sqlite3')

    # Create a Faker() Object
    fake = Faker()

    # Create a cursor() Object
    cursor = conn.cursor()

    try:

        # -- The following lines are commented out to avoid inserting new data every time the script is run.

        # create_authors_table(cursor)
        # create_books_table(cursor)

        # insert_into_authors(cursor, fake, author_num)
        # insert_into_books(cursor, fake, book_num)

        fetch_books_with_most_pages(cursor)
        fetch_average_page_number(cursor)
        fetch_youngest_author(cursor)
        fetch_authors_with_no_books(cursor)
        fetch_more_than_3_book_authors(cursor)

        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()

