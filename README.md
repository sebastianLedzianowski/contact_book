# 📚 Contact Book

A simple app to manage your contacts and track upcoming birthdays.

## Introduction

Contact Book is an application created using FastAPI, SQLAlchemy, Pydantic, and other Python technologies. It allows you to add, edit, delete contacts, and keep track of upcoming birthdays. All of this is supported to JWT token pairs: access token and refresh token.

## Functions

- ➕ Add, ✏️ edit, and ❌ delete contacts.
- 📅 Track upcoming birthdays.
- 🧪 Generate fake contacts for testing purposes.
- 🔐 Implementation of an authentication mechanism.
- 🔑 Implementation of an authorization mechanism using JWT tokens, so that all operations on contacts are performed only by registered users.
- 🧑‍💻 The user only has access to their contacts operations.

## Requirements

- 🐍 Python 3.7+
- ⚡ FastAPI(REST API)
- 🐘 SQLAlchemy
- 🐘 PostgresSQL

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
# PostgresSQL Database
SQLALCHEMY_DATABASE_URL=
# Authentication and token generation
SECRET_KEY=
ALGORITHM=
```

---

**Note**: Ensure to keep your `.env` file secure and never commit it to the repository to protect sensitive information.

---

## Installation ⬇️

1.Let's run a Docker container to create a PostgresSQL server using the following command:

```bash
docker run --name db-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

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
2. Navigate to the `/signup` tab.
3. Use the "Try it out" button and provide user details (e.g., username, password) for registration.
4. Click "Execute" and check the response.

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
