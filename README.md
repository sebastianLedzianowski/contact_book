# 📚 Contact Book

Contact Book is an application built with FastAPI, SQLAlchemy, Pydantic, and other Python technologies. It provides a user-friendly interface to manage contacts efficiently. Key features include the ability to add, edit, and delete contacts, as well as track upcoming birthdays.

## Registration and Authentication

During the registration process, users are required to confirm their email address by clicking on the activation link sent to the provided email. The login mechanism is secured using JWT pairs, comprising an access token and a refresh token. This ensures a secure and authenticated experience for users.

## Functions

- ⏳ **User Caching:** Mechanism allowing user caching in the application to optimize data access and improve performance.
- 🔒 **Implementation of Authentication Mechanism:** Securing the application by introducing a user authentication mechanism.
- 🗝️ **Implementation of Authorization Mechanism using JWT Tokens:** Ensuring that all operations on contacts are performed only by registered users.
- 📅 **Tracking Upcoming Birthdays:** Feature for monitoring upcoming birthdays among contacts.
- ➕ **Adding Contacts:** Ability to add new contacts to the application.
- ✏️ **Editing Contacts:** Feature allowing the editing of existing contact details.
- ❌ **Deleting Contacts:** Ability to remove unnecessary contacts from the list.
- 🧪 **Generating Fake Contacts for Testing Purposes:** Allows adding artificial contact data for testing purposes.

## Requirements

- 🐍 Python 3.10+
- ⚡ FastAPI(REST API)
- 🐘 PostgresSQL
- 🐘 SQLAlchemy
- 📘 Pydantic
- 🔄 Redis
- 🐳 Docker-compose

## Installation ⬇️

1. **Clone the repository:**

    ```bash
    git clone https://github.com/sebastianLedzianowski/contact_book.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd contact_book
    ```

3. **Set up a virtual environment and activate it (optional but recommended):**

    ```bash
    virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install dependencies using Poetry:**

    ```bash
    pip install poetry
    poetry install
    ```

## Configuration ⚙️

To run this project, you will need to add the following environment variables to your `.env` file.

```bash
#PostgresSQL DateBase
SQLALCHEMY_DATABASE_URL=
#Authentication and token generation
SECRET_KEY=
ALGORITHM=
#Email config
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_PORT=
MAIL_SERVER=
MAIL_FROM_NAME=
MAIL_STARTTLS=
MAIL_SSL_TLS=
USE_CREDENTIALS=
VALIDATE_CERTS=
#Docker-composo settings
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

---

**Note**: Ensure to keep your `.env` file secure and never commit it to the repository to protect sensitive information.

---

## Installation ⬇️

1.Let's launch Docker containers to create a PostgresSQL and Redis server using the following command:

```bash
docker-compose up 
```

2.Now, let's apply the initial migration:

```bash
alembic upgrade head
```

3.Run the application:

```bash
uvicorn main:app --host localhost --port 8000 --reload
```

## User Instructions 🚀

### 1. Registration and Login

### Registration:
1. Go to the API in your browser: http://127.0.0.1:8000/docs. 
2. Navigate to the /signup tab.
3. Use the "Try it out" button and provide user details (e.g., username, password) for registration.
4. Click "Execute" to send the registration request.
5. Check your email inbox for a verification message.
6. Open the verification email and click on the provided activation link.
7. Once the activation link is clicked, return to the API or refresh the browser.
8. You should now be successfully registered and activated. Check the response for confirmation.

### Login:
1. Go to the API in your browser: http://127.0.0.1:8000/docs.
2. Navigate to the `/login` tab.
3. Use the "Try it out" button and provide login credentials (e.g., username, password).
4. Click "Execute" and check the response.

### 2. Adding Contacts

### Adding Contacts:
1. After logging in, go to the `/contact` tab.
2. Use the "Try it out" button and provide contact details.
3. Click "Execute" and check the response.

### 3. Tracking Upcoming Birthdays

### Tracking Birthdays:
1. After logging in, go to the `/api/contact/upcoming_birthdays/{days_in_future}` tab.
2. Use the "Try it out" button and enter the number of days into the future.
3. Click "Execute" and check the response.

### Additional Information

- 🌐 All contact operations are available only for logged-in users.
- 👤 Each user has access only to their contact operations.
- 🔐 Remember to log in correctly before using the contact-related functions.

**Note:**
- If you don't have an account yet, register using the "Registration" option.
- After registering, use the "Login" option to access the contact adding and birthday tracking functions.



## Created 👤

- [Sebastian Ledzianowski](https://github.com/sebastianLedzianowski)

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
