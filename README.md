# Keep Contact
#### Video Demo:  <https://youtu.be/L1mHh22A9ME>
#### Description:
A simple web application simulates the contact book.

In this application, will allow users to add new contact, which contains the first name, last name, phone number, email and address.

Some basic functions for web application, like login, logout, register and change password.

Materials contained in this project as follow:

    1.static (resource folder)
        favicon.ico         --> web page icon
        main-background.jpg --> web page background
        newcontact.css      --> style sheet for add new contact page
        style.css           --> general style sheet for whole web project

    2.templates (all html files)
        apology.html        --> used when render apology to user
        changepassword.html --> user when user wants to change password
        index.html          --> used for home page for this web project
        layout.html         --> used as template for all html files
        login.html          --> used when user try to log in or when first time visit this site
        newcontact.html     --> used when user wants to add new contact
        register.html       --> used when user wants to register

    3.app.py (control the web application)
        In detail:
        @app.route("/")     --> render index.html(home page) when requests received, will all the contacts per the user

        @app.route("/newcontact", methods=["GET", "POST"])
                            --> render newcontact.html when request method is GET, will insert new contact into database when request method is POST

        @app.route("/changepassword", methods=["GET", "POST"])
                            --> render changepassword.html when request method is GET, will update user password hash when request method is POST

        @app.route("/login", methods=["GET", "POST"])
                            --> render login.html when request method is GET, will redirect to home page when valid username and password submitted

        @app.route("/logout")
                            --> clear user id store in session, redirect user to login.html

        @app.route("/register", methods=["GET", "POST"])
                            --> render register.html when request method is GET, will store the data to table.users when the method is POST

    4.helpers.py (few functions used when app.py is running)

    5.project.db (datebase, to store all the data collected from this web application)
        Tables in detail:
        users  --> will store user id, username and password hash
        people --> will store the people id, friend_id, first name, last name, phone number, email and address

        CREATE TABLE people(
            id            INTEGER,
            friend_id     INTEGER,
            first_name    TEXT NOT NULL,
            last_name     TEXT NOT NULL,
            phone         TEXT NOT NULL,
            email         TEXT NOT NULL,
            address       TEXT NOT NULL,
            PRIMARY KEY(id),
            FOREIGN KEY(friend_id) REFERENCES users(id));

        CREATE UNIQUE INDEX id ON people(id);

        CREATE TABLE IF NOT EXISTS 'users' (
            id            INTEGER,
            username      TEXT NOT NULL,
            hash          TEXT NOT NULL,
            PRIMARY KEY(id));

        CREATE UNIQUE INDEX username ON users(username);

    5.requirements.txt





