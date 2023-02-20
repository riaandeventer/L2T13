# Software Engineer: RIAAN VAN DEVENTER (SN: RV22110005417)
# This was programmed for the Software Engineering BOOTCAMP
# Written on 11 January 2023
#
# ************** L2T13 - TASK ASSIGNMENT **************  
#
# - Create a program that can be used by a bookstore clerk. The program should allow the clerk to:
#   * add new books to the database
#   * update book information
#   * delete books from the database
#   * search the database to find a specific book.
# 
# - Create a database called ebookstore and a table called books. The table should have the following structure:
#   id      Title                                       Author              Qty
#   3001    A Tale of Two Cities                        Charles Dickens     30
#   3002    Harry Potter and the Philosopher's Stone    J.K. Rowling        40
#   3003    The Lion, the Witch and the Wardrobe        C. S. Lewis         25
#   3004    The Lord of the Rings                       J.R.R Tolkien       37
#   3005    Alice in Wonderland                         Lewis Carroll       12
#
# - Populate the table with the above values. You can also add your own values if you wish.
# - The program should present the user with the following menu:
#       1. Enter book
#       2. Update book
#       3. Delete book
#       4. Search books
#       0. Exit
#
# - The program should perform the function that the user selects. The implementation of these functions 
#   is left up to you, but a demonstration of the topics we have covered in the last module should be shown.
#
# ****************************************************** 
#  Import Libraries
# ******************************************************
# Tabulate function allows us to print records in table format.
from tabulate import tabulate
# Import to allow Python to run SQL Queries.
import sqlite3

# Open or create a file that contains a sqlite3 database.
# Be sure to create any folder you want to place the database file in, before the time. 
# The sqlite3.connect only creates files and not folders.
try:
    db = sqlite3.connect('./ebookstore_db')
except Exception as error_msg:
    print()
    print (f"--> Connect db: {error_msg} ...\n")
    exit()

#===================================== Functions =====================================
def access_tbl ():
    '''
    This function will create the books table if it does not exist.
    '''
    try: 
        cursor = db.cursor() 
        # Test if this table exists else create a table called books_tbl with id as the primary key,
        # and Title must have a value.
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                            books_tbl(Id INTEGER PRIMARY KEY, 
                                    Title TEXT NOT NULL ON CONFLICT IGNORE, 
                                    Author TEXT,
                                    Qty INTEGER)''')
        db.commit()
    # Catch  exception for CREATE TABLE errors.
    except Exception as error_msg:
        db.rollback()
        print()
        print (f"--> Create Table: {error_msg} ...\n")
        exit()

#===================================== End access_tbl() =====================================
def pop_tbl ():
    '''
    This function will populate the books table with initial records read from file InventoryReset.txt
    '''
    # If we find the InventoryReset.txt file then f_books will change from None to a representation of the file.
    # Let's start f_books with a value of None.
    f_books = None
    # If the file is empty then file_reads_bln will be changed to False. Let's start with a value of True.
    file_reads_bln = True
        
    while f_books is None :
        try:
            # Open the file for read mode. If the file is found then f_books value will change and 
            # the while f_books == None will not repeat at the end of this instance.
            f_books = open ("./InventoryReset.txt", "r")
            # Read the first line of headings as to not include it in the books table.
            # For an empty file we are using next() to catch an except StopIteration error.
            next(f_books)
            cursor = db.cursor() 
            # We create a books_lst to load all the records from the file in order to run one SQL Insert that will
            # insert all the records with the one insert command. 
            books_lst = []
            # Set load_success = 1 for continuation. If we get an error, we will set it to 0 to handle exception.
            load_success = 1

            # Now read through the rest of the file from line 2 till end and store it in books_lst.
            for line in f_books :
                if line.strip () :
                    # We remove the next line character to fix the data value at the end of the line.
                    line = line.replace ("\n", "")
                    # Separate the string by ", " and place the parts into a list.
                    new_book = line.split ("; ")

                    try:
                        # Prepare 1 record by using load_book, then append the record to the books_lst of records.
                        # Use the try: to catch any int type variables that might not have an integer input.
                        load_book = (int(new_book[0]), new_book[1], new_book[2], int(new_book[3]))
                    except ValueError :
                        print()
                        print ("--> pop_tbl: Value does not translate to integer ...")
                        load_success = 0   
                        break           

                    books_lst.append (load_book)

            # Insert all rows into the books table if load_success allows (If still = 1).
            if load_success == 1 :
                try:
                    # Use try: to catch any SQL command errors.
                    cursor.executemany('''INSERT INTO books_tbl(Id, Title, Author, Qty) VALUES(?,?,?,?)''', books_lst)
                    db.commit()
                # Catch the exception for INSERT errors.
                except Exception as error_msg:
                    db.rollback()
                    print()
                    print (f"--> pop_tbl: {error_msg} ...")

        # If the file opened in f_books above is not found then this FileNotFoundError logic will run.
        except FileNotFoundError:
            print()
            print ("--> The InventoryReset file cannot be found in the folder.")

        # If the file exists but has no data in it, then we will get this error on the next(f_books) statement.
        except StopIteration:
            file_reads_bln = False
            print()
            print ("--> The InventoryReset file is empty.")
        
        finally:
            # If the file is not found, we will get an error on f_books.close(), so we will only execute
            # the finally: if we found the file represented by f_books and the value changed from None.
            if f_books is not None:
                f_books.close()
            
            # If we had a successful first read and if there were book inventory entries, then we will
            # display success message else we will display error message.
            if file_reads_bln == True and len (books_lst) > 0 and load_success == 1 :
                print()
                print ("--> Books Table loaded with initial inventory list.")
            else :
                print()
                print ("--> Books inventory load error... CHECK the InventoryReset File content!")

#===================================== End pop_tbl() =====================================
def view_all_books():
    '''
    This function will select all the records in the table and display them with a break continue flow.
    '''
    cursor = db.cursor() 

    # Display all the books in the table.
    try:
        cursor.execute('''SELECT * FROM books_tbl''')
        results = cursor.fetchall()
        # To display 5 records at a time, set View_pause_int = 5.
        view_pause_int = 5
 
        if len(results) > 0:
            print()
            print ("=========================== Books in the eBookStore ===========================\n")
            # book_tbl_nlst is a nested list with first instance being the headers for our table.
            book_tbl_nlst = [["Id", "Title", "Author", "Quantity"]]

            for i in range (len(results)) :
                table_row = (results[i][0], results[i][1], results[i][2], results[i][3])
                book_tbl_nlst.append (table_row)

                # Pause the view for every {view_pause_int} rows so it does not run off the screen. 
                # This can easily be adjusted to 10 (change view_pause_int value) depending on the screen conditions.
                # We are not showing continuation option or doing the below if-statement if our
                # last record is on a multiple of {view_pause_int} display.
                if (i+1) % view_pause_int == 0 and (i+1) != len(results):
                    # Calculate start of display.
                    view_start_int = (i + 1) - (view_pause_int - 1)
                    print (tabulate(book_tbl_nlst, headers = 'firstrow'))
                    print (f"================================= Books {view_start_int} to {i + 1} =================================")
                    # reset book_tbl_nlst with first instance being the headers for our next screen display.
                    book_tbl_nlst = [["Id", "Title", "Author", "Quantity"]]
                    print ()
                    go_response = input ("<Enter> for next rows or type M to return to Menu : ").lower()
                    print ()

                    if go_response == 'm':
                        break
                
                # When the last display is less than or exactly 5 rows, display the last books with this if statement.
                if i == (len(results)-1):
                    # Calculate start of display.
                    # For this one we calculate the last record displayed and then add 1 for start of next display.
                    view_start_int = ((i+1) - ((i+1) % view_pause_int)) + 1    
                    print (tabulate(book_tbl_nlst, headers = 'firstrow'))
                    print (f"================================= Books {view_start_int} to {i + 1} =================================")
        
        else:
            # if no records were found with the SELECT * statement, then display below message.
            print()
            print ("--> There are no books listed in the ebookstore!")
            print ("--> Use Menu Option 6 to load default inventory!")

    # Catch  exception errors for the SELECT * query or the fetchall()
    except Exception as error_msg:
        print (f"--> read_all_books: {error_msg} ...\n")

#===================================== End read_all_books() =====================================
def capture_book():
    '''
    This function will allow the user to capture new books.
    '''
    cursor = db.cursor() 

    # Get the new book Id.
    # Use while True: to repeat the input request until we receive a valid integer.
    while True :
        try:
            print()
            book_id = int (input ("Enter an id number for your new book > "))

            try:
                # Test if the id already exist.
                cursor.execute('''SELECT * FROM books_tbl 
                                    WHERE Id = ?''', (book_id,))
                results = cursor.fetchone()

                if results is not None:
                    print ("--> This id already exists in the ebookstore!")
                else:
                    break

            # Catch the exception for the SELECT * statement or the fetchone().
            except Exception as error_msg:
                print (f"--> capture_book (Test Id): {error_msg} ...\n")

        # Catch the exception where the id entry is blank or not an integer.
        except ValueError :
            print ("--> That was not a valid id. Please try again ...\n")

    # Get the new book title.
    # Use while True: to repeat the input request until the entry is not blank.
    # since we declare Title in the table to be a NOT NULL value.
    while True :
            book_ttl = input ("Enter the title for your new book > ")

            if book_ttl == "":
                print ("--> The title cannot be blank ...\n")
            else:
                # If the input is not blank, then exit the while True:
                break

    # Get the new book author
    book_auth = input ("Enter the author name for your new book > ")
    # If the user pressed enter and did not enter anything, then set book_auth to
    # a space to avoid any None or not defined errors.
    if book_auth == "":
        book_auth = " "

    # Get the new book quantity.
    # Quantity must be an integer number, so let's repeat the input request until we
    # are satisfied with the input.
    while True :
        try:
            book_qty = int (input ("Enter the quantity available for your new book > ")) 
            # If we get an integer input error above then we will jump over the break to the exept ValueError:
            # This below break will therefor run if the integer input is valid and we will exit the while True:
            break      
        # Catch the exception where the quantity entry is blank or not an integer.
        except ValueError :
            print ("--> That was not a valid number. Please try again ...\n")

    cursor = db.cursor()    
    # Set the values in a list/tuple.
    books_new = (book_id, book_ttl, book_auth, book_qty)

    # We use the try: here to catch any INSERT errors.
    try:
        # Insert new rows into the books table.
        cursor.execute('''INSERT INTO books_tbl(Id, Title, Author, Qty) VALUES(?,?,?,?)''', books_new)
        db.commit()
    # Catch the exception for INSERT errors.
    except Exception as error_msg:
        # Roll back any change if something goes wrong.
        db.rollback()
        print (f"--> capture_book (Insert New Book): {error_msg} ...\n")
    # Print message to user if the capture was successful.
    finally:
        print()
        print ("--> New book was loaded. Use Menu option 1 or 5 to view.") 

#===================================== End capture_book() =====================================
def update_book():
    '''
    This function will allow the user to update the data on a book, like the quantity available or 
    typing errors on the title or author.
    '''
    cursor = db.cursor()   

    # Use the while True: to repeat the input request for id until it is a valid integer.
    while True :
        try:
            print()
            book_id = int (input ("Enter the id for the book you want to update : "))

            # Use try: to catch SELECT * or fetchone erros
            try:
                # Test if the id already exist.
                cursor.execute('''SELECT * FROM books_tbl 
                                    WHERE Id = ?''', (book_id,))
                results = cursor.fetchone()

                # If we found records with the SELECT *, display the record to use as reference for update.
                if results is not None:
                    # book_tbl_nlst is a nested list with first instance being the headers for our table.
                    book_tbl_nlst = [["Id", "Title", "Author", "Quantity"], [results[0], results[1], results[2], results[3]]]
                    print()
                    print ("========================== Search Results for Id ==============================")
                    print (tabulate(book_tbl_nlst, headers = 'firstrow'))
                    print ("===============================================================================")
                    update_opt = " "

                    # Run below repeatly until user enters x for Exit. This allows user to make multiple changes on the same record.
                    # To make a change to a different record, the user can E(x)it and choose update from the menu to enter a different
                    # Id to update.
                    while update_opt != 'x' :
                        print()
                        update_opt = input ("Would you like to update the (T)itle, (A)uthor, (Q)uantity or E(x)it? Enter T,A,Q or X > ").lower()

                        # Choose to update the Title.
                        if update_opt [0] == 't' :
                            print()
                            book_ttl = input ("Enter the correct title for the book : ")

                            if book_ttl is not None:
                                try:
                                    # Update the Title.
                                    cursor.execute('''UPDATE books_tbl 
                                                        SET Title = ?
                                                        WHERE Id = ?''', (book_ttl,book_id),)
                                    print()
                                    print ("--> Book title was updated. Use Menu option 1 or 5 to view.") 
                                # Catch the exception for UPDATE errors.
                                except Exception as error_msg:
                                    db.rollback()
                                    print (f"--> Update Title: {error_msg} ...\n")
                            else :
                                print ("--> You did not enter any characters ...\n")

                        # Choose to update the Author.
                        elif update_opt [0] == 'a' :
                            print()
                            book_auth = input ("Enter the correct author for the book : ")

                            if book_auth is not None:
                                try:
                                    # Update the Author.
                                    cursor.execute('''UPDATE books_tbl 
                                                        SET Author = ?
                                                        WHERE Id = ?''', (book_auth,book_id),)
                                    print()
                                    print ("--> Book author was updated. Use Menu option 1 or 5 to view.") 
                                # Catch the exception for UPDATE errors.
                                except Exception as error_msg:
                                    db.rollback()
                                    print (f"--> Update Author: {error_msg} ...\n")
                            # If input was blank, do not update and return to update options.
                            else :
                                print ("--> You did not enter any characters ...\n")

                        # Choose to update the Quantity.
                        elif update_opt [0] == 'q' :
                            # Run while to repeat input until receive an integer quantity.
                            while True :
                                try: 
                                    print()
                                    book_qty = int (input ("Enter the correct quantity for the book : "))

                                    # If user did not just enter with no input and input is integer, then update.
                                    try:
                                        # Update the quantity.
                                        cursor.execute('''UPDATE books_tbl 
                                                            SET Qty = ?
                                                            WHERE Id = ?''', (book_qty,book_id),)
                                        print()
                                        print ("--> Book quantity was updated. Use Menu option 1 or 5 to view.") 
                                        # Update option was successful so let's exit the while loop.
                                        break
                                    # Catch the exception for UPDATE errors.
                                    except Exception as error_msg:
                                        db.rollback()
                                        print (f"--> Update Quantity: {error_msg} ...\n")

                                # This error will catch blank input and non-integer inputs.
                                except ValueError :
                                    print ("--> That was not a valid quantity. Please try again ...")

                        # Go back to Main Menu.
                        elif update_opt [0] == 'x' :
                            print()
                            print ("--> Back to Main Menu!")

                        # Display message for invalid options and display update options again.
                        else :
                            print ("---> Please enter a valid option!")

                # Display message when id does not exist for update request.
                else :
                    print ("--> This id does not exists in the ebookstore!")

                # We received a valid input so we can exit the while True: loop.
                break

            # Catch the exception for SELECT * and fetchone errors.
            except Exception as error_msg:
                print (f"--> Update Book: {error_msg} ...\n")

        # Catch the exception where the id entry is blank or not an integer.
        except ValueError :
            print ("--> That was not a valid id. Please try again ...")

#===================================== End update_tbl() =====================================
def delete_book():
    '''
    This function will allow a user to remove a book from the table. We will use the Id to 
    remove an item and this can be found with a view all or search function.
    '''
    cursor = db.cursor() 

    # Get id from book to delete.
    while True :
        # Use try: to repeat input request until input is an integer.
        try:
            print()
            book_id = int (input ("Enter an id number for your new book : "))

            try:
                # Test if the id already exist.
                cursor.execute('''SELECT * FROM books_tbl 
                                    WHERE Id = ?''', (book_id,))
                results = cursor.fetchone()

                # If we found the record then we can run DELETE query.
                if results is not None:
                    cursor.execute('''DELETE FROM books_tbl 
                                        WHERE Id = ?''', (book_id,))
                    print()
                    print ("--> Requested book was removed. Use Menu option 1 or 5 to confirm.")
                else:
                    print ("--> This id does not exists in the ebookstore!")
                    
            # Catch the exception for SELECT *, fetchone and DELETE errors.
            except Exception as error_msg:
                db.rollback()
                print (f"--> delete_book (Test Id): {error_msg} ...\n")
            finally:
                # Exit the while True: if we received a valid id input and book was delete successfully.
                break

        # Catch the exception for Id input errors.
        except ValueError :
            print ("--> That was not a valid id. Please try again ...") 

#===================================== End delete_book() =====================================
def search_book():
    '''
     This function will search for a book from the table using the book id, title, author or limited stock.
    '''
    # Create a menu that chooses the search method.
    # Initialise menu option variable with any value outside of menu options.
    sub_menu_int = 10

    # Repeat search options until user exit the menu with integer 0 input.
    while sub_menu_int != 0 :
        # Display search submenu until user input valid option.
        while True :
            # Use try: except: finally: to catch menu option error.
            try : 
                print()
                print ("=============== Search MENU ==================")
                print ("1. Search by Id")
                print ("2. Search by Title")
                print ("3. Search by Author")
                print ("4. Search for limited stock")
                print ("0. Exit Search")
                print ("==============================================\n")
                sub_menu_int = int (input ("Please choose a menu option (e.g. 0 to 4) > "))
                
                if sub_menu_int >= 0 and sub_menu_int < 5 :
                    break
                else :
                    print ("--> That was not a valid option. Please try again ...")
    
            # Catch exception for when input is not integer.
            except ValueError :
                print ("--> That was not a valid option. Please try again ...")

        cursor = db.cursor()    
    
        # SubMenu option to search by Id.
        if sub_menu_int == 1 : # book_id
            while True :
                try:
                    print()
                    book_id = int (input ("Enter an id number for your search : "))

                    try:
                        # Search for Id
                        cursor.execute('''SELECT * FROM books_tbl 
                                            WHERE Id = ?''', (book_id,))
                        results = cursor.fetchone()

                        # If we found the book.
                        if results is not None:
                            # book_tbl_nlst is a nested list with first instance being the headers for our table.
                            book_tbl_nlst = [["Id", "Title", "Author", "Quantity"], [results[0], results[1], results[2], results[3]]]
                            print()
                            print ("========================= Id Search in the eBookStore =========================\n")
                            print (tabulate(book_tbl_nlst, headers = 'firstrow'))
                            print ("===============================================================================")
                        else :
                            print ("--> This id does not exists in the ebookstore!")
                        
                        break

                    # Catch the exception for SELECT * and fetchone errors.
                    except Exception as error_msg :
                        print (f"--> Search Id: {error_msg} ...\n")

                # Catch errors for id input blank or not integer.
                except ValueError :
                    print ("--> That was not a valid id. Please try again ...")
            
        # Sub-Menu option to search by title.
        elif sub_menu_int == 2 : # book_ttl  
            print()
            book_ttl = input ("Enter a title for your search - partials also ok : ")

            # If the user input is not blank.
            if book_ttl != "":
                try:
                    # Search for Title
                    cursor.execute('''SELECT * FROM books_tbl 
                                        WHERE Title LIKE ?''', ('%{}%'.format(book_ttl),))
                    results = cursor.fetchall()

                    # If we found at least 1 record.
                    if len(results) > 0 :
                        print()
                        print ("======================== Title Search in the eBookStore ========================\n")
                        # book_tbl_nlst is a nested list with first instance being the headers for our table.
                        book_tbl_nlst = [["Id", "Title", "Author", "Quantity"]]

                        # Run through the instances and enter them into the display list.
                        for i in range (len(results)) :
                            table_row = (results[i][0], results[i][1], results[i][2], results[i][3])
                            book_tbl_nlst.append (table_row)

                        print (tabulate(book_tbl_nlst, headers = 'firstrow'))
                        print ("===============================================================================")
                    else:
                        print (f"--> No titles containing >{book_ttl}< in the ebookstore!\n")

                # Catch the exception for SELECT * and fetchall errors.
                except Exception as error_msg:
                    print (f"--> Search Title: {error_msg} ...\n")

            else :
                print ("--> You did not enter any characters ...")

        # Sub-Menu option to search by author.
        elif sub_menu_int == 3 : # book_auth
            print()
            book_auth = input ("Enter an author for your search - partials also ok : ")

            # If the user input is not blank.
            if book_auth != "":
                try:
                    # Search for Author.
                    cursor.execute('''SELECT * FROM books_tbl 
                                        WHERE Author LIKE ?''', ('%{}%'.format(book_auth),))
                    results = cursor.fetchall()

                    # If we found at least 1 record.
                    if len(results) > 0 :
                        print ()
                        print ("======================== Author Search in the eBookStore ========================\n")
                        # book_tbl_nlst is a nested list with first instance being the headers for our table.
                        book_tbl_nlst = [["Id", "Title", "Author", "Quantity"]]

                        # Run through the instances and enter them into the display list.
                        for i in range (len(results)) :
                            table_row = (results[i][0], results[i][1], results[i][2], results[i][3])
                            book_tbl_nlst.append (table_row)

                        print (tabulate(book_tbl_nlst, headers = 'firstrow'))
                        print ("=================================================================================")

                    else:
                        print (f"--> No authors containing >{book_auth}< in the ebookstore!\n")

                # Catch the exception for SELECT * and fetchall errors.
                except Exception as error_msg:
                    print (f"--> Search Author: {error_msg} ...\n")

            else :
                print ("--> You did not enter any characters ...")

        # Sub-Menu option to search by quantity.
        elif sub_menu_int == 4 : # book_qty
            while True :
                try:
                    print()
                    book_qty = int (input ("Enter quantity to return books available less than that : "))

                    try:
                        # Search for quantities less than input.
                        cursor.execute('''SELECT * FROM books_tbl 
                                            WHERE Qty < ?''', (book_qty,))
                        results = cursor.fetchall()

                        # If we found at least 1 record.
                        if len(results) > 0 :
                            print()
                            print ("===================== Limited Stock Search in the eBookStore =====================\n")
                            # book_tbl_nlst is a nested list with first instance being the headers for our table.
                            book_tbl_nlst = [["Id", "Title", "Author", "Quantity"]]

                            # Run through the instances and enter them into the display list.
                            for i in range (len(results)) :
                                table_row = (results[i][0], results[i][1], results[i][2], results[i][3])
                                book_tbl_nlst.append (table_row)

                            print (tabulate(book_tbl_nlst, headers = 'firstrow'))
                            print ("=================================================================================")
                        else:
                            print (f"--> There are no books with quantity less than {book_qty} in the ebookstore!\n")

                        break

                    # Catch the exception for SELECT * and fetchall errors.
                    except Exception as error_msg:
                        print (f"--> Search Quantity: {error_msg} ...\n")

                # Catch errors for quantity input blank or not integer.
                except ValueError :
                    print ("--> That was not a valid quantity. Please try again ...")
            
        elif sub_menu_int == 0 :
            print()
            print ("--> Back to Main Menu!")

#===================================== End search_book() =====================================
def reset_books_tbl():
    '''
     This function will reset the books table by removing all records and loading the records in the InventoryReset.txt file.
    '''
    cursor = db.cursor()    

    try:
        # Remove all rows in the books table.
        cursor.execute('''DELETE FROM books_tbl''')
        db.commit()
        pop_tbl ()
    # Catch the exception for DELETE.
    except Exception as error_msg:
        # Roll back any change if something goes wrong.
        db.rollback()
        print()
        print (f"--> reset_books_tbl: {error_msg} ...")

#===================================== End reset_books_tbl() =====================================

# ============  MAIN LOGIC - eBookStore Management  ===============
# Make sure the table exists.
access_tbl ()

# ------> For no books in eBookStore, choose menu option 6 to load initial inventory list.

#====================== Main Menu ======================
# Create a menu that executes each function above.
# Initialise menu option variable with any value outside of menu options.
menu_int = 10

while menu_int != 0 :
    # Display bookstore menu until valid option is chosen.
    while True :
        # Use try: except: finally: to catch menu option error.
        try : 
            print()
            print ("========================== Bookstore MENU ==========================")
            print ("1. View the Books")
            print ("2. Capture a new book")
            print ("3. Update details for a book")
            print ("4. Remove a book from the system")
            print ("5. Search for a book")
            print ("6. Load/Reload database with default inventory list (Take Caution!)")
            print ("0. Exit Program")
            print ("====================================================================\n")

            menu_int = int (input ("Please choose a menu option (e.g. 0 to 6) > "))

            # If the user entered an available menu integer option then exit the while True:
            if menu_int >= 0 and menu_int < 7 :
                break
            else :
                print ("--> That was not a valid option. Please try again ...")
    
        # Catch the exception for an input that is not integer.
        except ValueError :
            print ("--> That was not a valid option. Please try again ...")

#====================== End Main Menu ======================

#==================== Menu Options Logic ===================   

    # Menu option to view the books.
    if menu_int == 1 :
        view_all_books()

    # Menu option to capture a new book.
    elif menu_int == 2 :
        capture_book()

    # Menu option to update details for a book.
    elif menu_int == 3 :
        update_book()

    # Menu option to remove a book from the system.
    elif menu_int == 4 :
        delete_book()

    # Menu option to search for a book.
    elif menu_int == 5 :
        search_book()

    # Menu option to reset the database.
    elif menu_int == 6 :
        print()
        print ("--> This will remove all books and load books from the InventoryReset.txt file.")
        print ("--> Make sure the InventoryReset.txt file is in the same folder as the *.py file.\n")

        # Repeat input request until input first character is upper or lower case y or n. 
        while True :
            reset_opt = input ("---> Are you sure you want to reset the ebookstore books list? (Answer Y or N) > ").lower()

            if reset_opt == "": # Input is None.
                reset_opt = " "

            if reset_opt [0] == 'y' :
                reset_books_tbl()
                break
            elif reset_opt [0] == "n" :
                print()
                print ("--> Back to Main Menu without resetting the ebookstore books list!")
                break
            else : 
                print()
                print ("--> Invalid input.")

    elif menu_int == 0 :
        # Close the db connection
        db.close()
        print()
        print ("Goodbye!\n")

# =================  END PROGRAM LOGIC HERE  ====================