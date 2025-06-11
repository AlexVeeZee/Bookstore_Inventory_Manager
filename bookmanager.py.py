import sqlite3

db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()

cursor.execute('''DROP TABLE book''')
cursor.execute('''DROP TABLE author''')
db.commit()

book_data = [
(3001, "A Tale of Two Cities", 1290, 30),
(3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
(3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
(3004, "The Lord of the Rings", 6380, 37),
(3005, "Alice's Adventures in Wonderland", 5620, 12),
]

author_data = [
(1290, "Charles Dickens", "England"),
(8937, "J.K. Rowling", "England"),
(2356, "C.S. Lewis", "Ireland"),
(6380, "J.R.R. Tolkien", "South Africa"),
(5620, "Lewis Carroll", "England"),
]


def populate_book(data):
	# Creates book table and enters data
	cursor.execute(
		'''
		CREATE TABLE IF NOT EXISTS book(
		id INTEGER PRIMARY KEY,
		title TEXT,
		authorID INTEGER,
		qty INTEGER
			)
		'''
	)
	cursor.executemany(
		'''
		INSERT INTO book(id, title, authorID, qty)
		VALUES(?, ?, ?, ?)	
		''',
		data
	)
	print('Multiple entries inserted.\n')
	db.commit()


def populate_author(data):
	# Creates author table and enters data
	cursor.execute(
		'''
		CREATE TABLE IF NOT EXISTS author(
		id INTEGER PRIMARY KEY,
		name TEXT,
		country TEXT
		)
		'''
	)
	cursor.executemany(
		'''
		INSERT INTO author(id, name, country)
		VALUES(?, ?, ?)	
		''',
		data
	)
	print('Multiple entries inserted.\n')
	db.commit()


def add_book(id, title, authorID, qty):
	# Inserts new book data to the database
	cursor.execute(
		'''
		INSERT INTO book(id, title, authorID, qty)
	VALUES(?, ?, ?, ?)	
		''',
	(id, title, authorID, qty)
	)
	print(f'''\nNew book added:
------------------------------------------
id:			{id}
title:			{title}
authorID:		{authorID}
quantity:		{qty}
------------------------------------------
		''')
	db.commit()


def update_book(upd_id, upd_qty):
	# Default change is the quantity, 
	# but additional options are available.
	try:
		while True:
			mod_choice = input(
	'''
	Select one of the following options:
	1 - edit the book information
	2 - only update the quantity
	: ''')

	# Allows the user to edit the title/authorID or both.
	# Afterwards it will display author info and prompts changes.
			if mod_choice == '1':
				print("\nEditing book details...")
				
				while True:
					edit_option1 = input('''
Do you want to edit the book's title? (Yes/No)
: ''').lower()
					if edit_option1 == 'yes':
						upd_title = input(
	f"Enter the corrected title:\n").title()
						cursor.execute(
							'''
							UPDATE book SET title = ? WHERE id = ?
							''',(upd_title, upd_id)
						)
						db.commit()
						break
					elif edit_option1 == "no":
						print("Skipping title change")
						break
					else:
						print("Choose 'yes' or 'no'.")

				while True:
					edit_option2 = input('''
Do you want to edit the book's AuthorID? (Yes/No)
: ''').lower()
					if edit_option2 == 'yes':
						upd_auth = int(input(
	f"Enter the corrected authorID:\n"))
						cursor.execute(
							'''
							UPDATE book SET authorID = ? WHERE id = ?
							''',(upd_auth, upd_id)
						)
						db.commit()
						break

					elif edit_option2 == 'no':
						print("Skipping authorID change")
						break
					else:
						print("Choose 'yes' or 'no'.")

				cursor.execute(
					'''
					UPDATE book SET qty = ? WHERE id = ?
					''',(upd_qty, upd_id)
				)
				db.commit()

				print("\nEditing author details...")
				cursor.execute(
					'''
					SELECT author.id, name, country FROM book
					INNER JOIN author ON author.id = book.authorID 
					WHERE book.id = ?
					''',(upd_id,)
				)
				author_info = cursor.fetchone()
				if author_info:
				 	print(f'''------------------------------
Author name: 	{author_info[1] if author_info[1] else "Unknown"}
Country: 	 {author_info[2] if author_info[2] else "Unknown"}
------------------------------
''')
				 	if author_info[1] is None:
				 		edit_option3 = input('''Do you want to edit the author\'s name? (Yes/No): ''').lower()
				 		if edit_option3 == 'yes':
				 			upd_name = input("Enter the author's name:\n").title()
				 			cursor.execute('''UPDATE author SET name = ? 
				 				WHERE id = ?''', (upd_name, author_info[0])
				 			)
				 			db.commit()

				 	if author_info[2] is None:
                    	edit_option4 = input('''Do you want to edit the author\'s country? (Yes/No): ''').lower()
                    	if edit_option4 == 'yes':
                    		upd_country = input("Enter the author's country:\n").title()
                    		cursor.execute('''UPDATE author SET country = ? 
                    			WHERE id = ?''', (upd_country, author_info[0])
                    		)
                    		db.commit()

                else:
                    print("No author information found.")

            # Only update the quantity
            elif mod_choice == '2':
                cursor.execute('''UPDATE book SET qty = ? WHERE id = ?''', (upd_qty, upd_id))
                db.commit()
				
			else:
				print("Invalid input. Please choose 1 or 2.")
				continue
			break

	except ValueError:
		print("\nNot a valid index input. Returning.")
	except Exception as e:
		print(f"\nAn error occurred: {e}")

	cursor.execute(
		'''
		UPDATE book SET qty = ? WHERE id = ?
		''',(upd_qty, upd_id)
	)
	db.commit()


def delete_book(del_id):
	# Delete a book from database.
	cursor.execute(
		'''
		DELETE FROM book WHERE id = ? ''', (del_id,)
	)
	db.commit()


def find_book(find_id):
	# Find a book in the database.
	cursor.execute(
		'''
		SELECT * FROM book WHERE id = ?
		''',(find_id,)
	)
	books = cursor.fetchone()
	if books:
		print(f'''\nHere is the requested book's information:
ID:			{books[0]}
title:			{books[1]}
authorID:		{books[2]}
quantity:		{books[3]}
''')
	else:
		print(f"No book found with the ID {find_id}")


def view_books_details():
	# View information about a book and it's author.
	cursor.execute(
		'''
		SELECT title, name, country FROM book
		INNER JOIN author ON author.id = book.authorID
		'''
		)
	book_auth_info = cursor.fetchall()
	print("\nDetails")
	for info in book_auth_info:
		print(f'''----------------------------------------------------------------
Title: 			{info[0]}
Author's Name: 		{info[1]}
Author's Country: 	{info[2]}
			''')


populate_book(book_data)
populate_author(author_data)

while True:
    menu = input(
            '''\nSelect one of the following options:
1 - Enter book
2 - Update book
3 - Delete book
4 - Search books
5 - View details of all books
0 - exit
: '''
        )

    if menu == '1':
        '''Adds books to the database'''
        # Checks that book ID is a 4 digit integer
        while True:
        	new_id = input(
            	'''\nEnter new book's 4 digit ID:''')
        	if new_id.isdigit() and len(new_id) == 4:
        		new_id = int(new_id)
        		break
        	else:
        		print("Invalid book ID. Only 4 digits.")

        # Checks that authorID is a 4 digit integer
        while True:
        	new_authorID = input(
            	'''\nEnter new book's 4 digit authorID:''')
        	if new_authorID.isdigit() and len(new_authorID) == 4:
        		new_authorID = int(new_authorID)
        		break
        	else:
        		print("Invalid authorID. Only 4 digits.")

        # Checks that quantity is an integer
        while True: 
        	new_qty = input(
            	'''\nEnter the quantity available:''')
        	if new_qty.isdigit():
        		new_qty = int(new_qty)
        		break
        	else:
        		print("Invalid. quantity must be a number")

        new_title = input(
            '''\nEnter new book's title:''').title()

        add_book(new_id, new_title, new_authorID, new_qty)

    elif menu == '2':
        '''Updates the information of books in the database'''
        upd_id = int(input(
            '''\nEnter the id of the book you want to update:'''))
        upd_qty = int(input(
            '''\nEnter the new quantity value:''')) 
        update_book(upd_id, upd_qty)

    elif menu == '3':
        '''Deletes books from the database'''
        del_id = int(input(
            '''\nEnter the id of the book you want to delete:''')) 
        delete_book(del_id)

    elif menu == '4':
        '''Search for a specific book in the database'''
        find_id = int(input(
            '''\nEnter the id of the book you want to find:''')) 
        find_book(find_id)  


    elif menu == '5':
        ''' View details of all the books in the database'''
        view_books_details()

    elif menu == '0':
        print('Goodbye!!!')
        db.commit()
        db.close()
        exit()

    else:
        print("You have entered an invalid input. Please try again")