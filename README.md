# Contact Book

A simple app to manage your contacts and track upcoming birthdays.

## Introduction

Contact Book is an application created using FastAPI, SQLAlchemy, Pydantic and other Python technologies. It allows you to add, edit, delete contacts and track upcoming birthdays.

## Functions

- Add, edit and delete contacts.
- Track upcoming birthdays.
- Generate fake contacts for testing purposes.

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- PostgreSQL

## Installation

1.Clone the repository:

```bash
git clone https://github.com/sebastianLedzianowski/contact_book.git
```

2.Navigate to the Project Directory:

```bash
cd contact_book
```

3.Set up a virtual environment and activate it (optional but recommended):

```bash
virtualenv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4.Install dependencies using Poetry:

```bash
pip install poetry
poetry install
```

## Configuration


To run this project, you will need to add the following environment variables to your `.env` file.

```bash
SQLALCHEMY_DATABASE_URL=
```
---

**Note**: Ensure to keep your `.env` file secure and never commit it to the repository to protect sensitive information.

---

## Usage 

1.Let's run a Docker container to create a PostgreSQL server using the following command:

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


---

The application will be available at http://127.0.0.1:8000.


---


## Using

1.Adding Contacts
Go to the API in your browser: http://127.0.0.1:8000/docs.
In the /contact tab, use the "Try it out" button and provide the contact details.
Click "Execute" and check the response.

2.Track Upcoming Birthdays
Go to the API in your browser: http://127.0.0.1:8000/docs.
In the /api/contact/upcoming_birthdays/{days_in_future} tab, use the "Try it out" button and enter the number of days into the future.
Click "Execute" and check the response.

## Created 
- [Sebastian Ledzianowski](https://github.com/sebastianLedzianowski)


## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
