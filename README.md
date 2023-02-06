# Bookstore Management Program

This program helps the clerk in the bookstore to keep track of the books in the store.

## Description

The management program can be used by a bookstore clerk. The program allows the clerk to:
* add new books to the database
* update book information
* delete books from the database
* search the database to find a specific book.

## Table of Content
1. Installation
2. Executing Program
3. Authors

### Dependencies

* This program uses the tabulate function and sqlite3.

### Installation

* Create the executable from ebookstore.py and place in same folder as InventoryReset.txt
* The file InventoryReset.txt contains the book data that you want to load initially. Update the information detail and note the format.
* The program will read in this file through a menu option and the database with table will be created or updated if it already exists.
* After initial load, you will notice the database file ebookstore_db in the folder.
* Database is called ebookstore and a table called books. The table has the following structure:

|Id     | Title                                     | Author             | Qty  |
|-------|-------------------------------------------|--------------------|------|
|3001   | A Tale of Two Cities                      | Charles Dickens    | 30   |
|3002   | Harry Potter and the Philosopher's Stone  | J.K. Rowling       | 40   |
|3003   | The Lion, the Witch and the Wardrobe      | C. S. Lewis        | 25   |
|3004   | The Lord of the Rings                     | J.R.R Tolkien      | 37   |
|3005   | Alice in Wonderland                       | Lewis Carroll      | 12   |

### Executing Program

* Run the program
* You will see the menu.

![Main Menu](/images/1.jpg)

* Menu Option 6: Start here to load the database or reset it in the future.
* Menu Option 1: This will straight display all the books in the inventory.
* Menu Option 2: This will request an identification number for the book, then book title, author and quantity you have available.
* Menu Option 3: You need the id of a book to update the title, author or quantity available. Use Menu Option 1 to get id number.
* Menu Option 4: Remove a book from you inventory by providing the id of the book. Use Menu Option 1 to get the id number.
* Menu Option 5: Search for books with below menu.

![Main Menu](/images/2.jpg)

* Menu Option 5: With submenu option 4 you can search for books with stock less than a certain number.

## Authors

Riaan Deventer  - [@riaandeventer](https://twitter.com/riaandeventer)
