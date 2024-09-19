# SQLite3 Books and Authors Database Project

This Python project creates and manages a SQLite database of books and authors using the `sqlite3` and `Faker` libraries. It populates the database with randomly generated data and performs various queries on the data.

## Features

- **Authors Table**: Stores information about authors, including first name, last name, birth date, and birthplace.
- **Books Table**: Stores book data such as title, category, page count, release date, and a reference to the author.
- **Data Queries**: The script includes several queries to analyze the data, such as:
  - Fetching books with the most pages.
  - Calculating the average number of pages per book.
  - Identifying the youngest author.
  - Listing authors with no books.
  - Finding authors who have written more than 3 books.

## Dependencies

- Python 3.x
- Faker library: used to generate fake data
- SQLite3 library: Built-in Python library to manage the database

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GigaDarchia/TBC-Task-5.git
   cd TBC-Task-5

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Run the script:
   ```bash
   python main.py

2. By default, the script will:

- Connect to the SQLite database (books.sqlite3)
- Perform various queries to extract insights about the data.

If you wish to insert new random data, uncomment the lines that create tables and insert 
authors and books in the main() function.



