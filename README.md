# 📚 eBookstore Inventory Management System

A Python command-line application that manages an eBookstore inventory using SQLite. This project demonstrates full CRUD operations with a relational database design, linking books and authors through author IDs.

## ✨ Features

- 📝 Two related tables: `book` and `author`, connected by author IDs.
- ➕ Add, ✏️ update, ❌ delete, and 🔍 search books.
- 📖 View detailed book and author information using SQL JOINs.
- 🖥️ Interactive CLI menu with input validation for IDs and quantities.
- 📦 Batch insertion of initial sample data.
- ⚠️ Robust error handling and user-friendly prompts.

## 🚀 How to Use

1. ▶️ Run the Python script.
2. Use the menu options to:
   - ➕ Add new books with validated input.
   - ✏️ Update book details, including title, author ID, and quantity.
   - ❌ Delete books by ID.
   - 🔍 Search books by ID.
   - 📋 View all books along with their author information.
3. 🛑 Exit the program cleanly with option `0`.

## 🛠️ Technologies

- 🐍 Python 3.x
- 🗄️ SQLite3

## 📁 Project Structure

- `ebookstore.db`: SQLite database file created and managed by the script.
- `main.py` (or your script filename): Contains all functionality including database setup and CLI interaction.

## 💡 Future Improvements

- 🔐 Enforce foreign key constraints for data integrity.
- ✨ Expand update functionality to edit author details fully.
- 📦 Modularize code into classes or separate modules for better maintainability.
- 🖥️ Add a graphical user interface (GUI) or web interface.
