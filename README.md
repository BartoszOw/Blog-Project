# Blog Application Description

The Blog application is a simple blog management system written in Python using the Flask framework. It allows users to browse, add, edit, and delete blog posts, as well as add comments.

## Functionality Overview:

- **User registration and login.**
- **Adding new blog posts.**
- **Editing existing posts.**
- **Deleting posts.**
- **Adding comments to posts.**
- **Searching for posts.**
- **Viewing a list of unpublished posts (available only to logged-in users).**
- **Utilizes The Movie Database (TMDB) API for fetching movie information.**
- **Integrates Flask-WTF and WTForms for form handling.**

## Technologies Used in the Application:

- **Python**: The programming language used for creating the application's backend.
- **Flask**: A micro web framework for building web applications in Python.
- **SQLAlchemy**: An Object-Relational Mapping (ORM) tool for working with SQL databases.
- **SQLite**: A database management system used for storing application data.
- **HTML/CSS**: Languages for creating the user interface.
- **Bootstrap**: A CSS framework for creating responsive and attractive web pages.
- **Jinja2**: A template engine used by Flask for generating dynamic HTML content.
- **Faker**: A tool for generating fake test data.
- **unittest**: Python's unit testing module.
- **requests**: Python library for making HTTP requests.
- **dotenv**: Python module for loading environment variables from a `.env` file.
- **Flask-WTF**: An extension for Flask that integrates Flask with WTForms.
- **WTForms**: A flexible forms validation and rendering library for Python web development.

## Requirements:

Before running the application, make sure you have installed:

- Python
- Flask
- SQLAlchemy
- Faker
- requests
- dotenv
- Flask-WTF

## Running the Application:

1. Clone the repository to your computer:
   ``git clone https://github.com/BartoszOw/Blog-Project``
2. Navigate to the application folder:
   ``cd blog``
3. Install all required dependencies:
   ``pip install -r requirements.txt``
4. Set your environment variables in the `.env` file. In particular, set your own TMDB API key:
   ``TMDB_API_TOKEN=your_api_token``
5. Run the application:
   ``flask run``
6. Open a web browser and go to `http://127.0.0.1:5000/`.

## Test Account:

To log in to the application, use the following credentials:

- **Username**: Test
- **Password**: test

## NOTE:

This project is merely an example of a web application created for educational and demonstrative purposes. It should not be treated as a ready-to-use product for production.
