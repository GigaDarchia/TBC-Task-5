import random
import sqlite3
from faker import Faker

# Initialize a database connection
conn = sqlite3.connect('books.sqlite3')

# Create a Faker() Object
fake = Faker()

# Create a cursor() Object
cursor = conn.cursor()

# A query that creates "authors" table
create_authors_table = '''
CREATE TABLE IF NOT EXISTS authors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_date TEXT,
        birth_place TEXT)'''

# A query that creates "books" table
create_books_table = '''
CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        pages INTEGER NOT NULL,
        release_date TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        FOREIGN KEY(author_id) REFERENCES authors(id)
        )'''

# Executing the queries using cursor
cursor.execute(create_authors_table)
cursor.execute(create_books_table)

# Random categories for books
categories = ["Comedy", "Drama", "Horror", "Thriller", "Romance", "Fantasy",
              "Mystery", "Adventure", "Science Fiction"]

"""

 -- Add random fake authors to the "authors" table

for i in range(500):
    fake_first_name = fake.first_name()
    fake_last_name = fake.last_name()
    fake_birthday = fake.date_of_birth(minimum_age=15, maximum_age=200).strftime("%y-%m-%d")
    fake_birthplace = fake.country()
    insert_query = '''
    INSERT INTO authors (first_name, last_name, birth_date, birth_place) 
    VALUES (?, ?, ?, ?)'''
    cursor.execute(insert_query, (fake_first_name, fake_last_name, str(fake_birthday), fake_birthplace))

"""

"""

  -- Add random books to the books table

for i in range(1000):
    fake_book_title = fake.sentence(nb_words=4).replace('.', ' ').title()
    fake_category = random.choice(categories)
    fake_pages = random.randint(100, 300)
    fake_release_date = fake.date_between(start_date="-50y", end_date="-10y")
    fake_author_id = random.randint(1, 500)
    insert_query = '''
    INSERT INTO books (title, category, pages, release_date, author_id) VALUES (?, ?, ?, ?, ?)'''
    cursor.execute(insert_query, (fake_book_title, fake_category, fake_pages, str(fake_release_date), fake_author_id))

"""

# Select books with most pages
cursor.execute('''SELECT * FROM books WHERE pages == (SELECT MAX(pages) FROM books)''')
print("Books with most pages: ")
for row in cursor.fetchall():
    print(row)

# Select average page amount in a book
cursor.execute('''SELECT AVG(pages) FROM books''')
print(f"\nAverage pages: {round(cursor.fetchall()[0][0])}\n")

# Select the youngest author
cursor.execute('''SELECT * FROM authors WHERE birth_date == (SELECT MAX(birth_date) FROM authors)''')
print("Youngest Author: ")
print(cursor.fetchall()[0])

# Select authors who wrote no books yet
cursor.execute('''SELECT * FROM authors WHERE id NOT IN (SELECT author_id FROM books)''')
print("\nAuthors with no books in the \"books\" table: ")
for row in cursor.fetchall():
    print(row)

conn.commit()

cursor.close()

conn.close()
