# 📚 Contact Book

Contact Book is an application built with FastAPI, SQLAlchemy, Pydantic, and other Python technologies. It provides a user-friendly interface to manage contacts efficiently. Key features include the ability to add, edit, and delete contacts, as well as track upcoming birthdays.

## Registration and Authentication

During the registration process, users are required to confirm their email address by clicking on the activation link sent to the provided email. The login mechanism is secured using JWT pairs, comprising an access token and a refresh token. This ensures a secure and authenticated experience for users.

## Functions

- ⏳ **User Caching:** Mechanism allowing user caching in the application to optimize data access and improve performance.
- 🔒 **Implementation of Authentication Mechanism:** Securing the application by introducing a user authentication mechanism.
- 🗝️ **Implementation of Authorization Mechanism using JWT Tokens:** Ensuring that all operations on contacts are performed only by registered users.
- 🚧 **Rate Limiting for API Throttling:** Throttle the number of requests to the API to prevent abuse, protect against DDoS attacks, and manage resource consumption efficiently.
- 🛡️ **Enhanced Security Measures:** Implementation of additional security measures to safeguard against various forms of abuse and spam.
- 🔄 **Cross-Origin Resource Sharing (CORS):** Implementation to facilitate resource sharing between servers located in different domains, enhancing security against cross-domain scripting (XSS) and cross-site request forgery (CSRF) attacks.
- ☁️ **Cloudinary Integration for Avatar Storage:** Storage of avatars in the cloud using [Cloudinary](https://cloudinary.com) for enhanced scalability and availability.
- 📅 **Tracking Upcoming Birthdays:** Feature for monitoring upcoming birthdays among contacts.
- ➕ **Adding Contacts:** Ability to add new contacts to the application.
- ✏️ **Editing Contacts:** Feature allowing the editing of existing contact details.
- ❌ **Deleting Contacts:** Ability to remove unnecessary contacts from the list.
- 🧪 **Generating Fake Contacts for Testing Purposes:** Allows adding artificial contact data for testing purposes.

## Requirements

- 🐍 Python 3.11+
- ⚡ FastAPI(REST API)
- 🐘 PostgresSQL
- 🐘 SQLAlchemy
- 📘 Pydantic
- 🔄 Redis
- 🐳 Dockerfile
- 🐳 Docker-compose
- ☁️ Cloudinary(Cloud file storage)

## Installation ⬇️

1. **Clone the repository:**

    ```bash
    git clone https://github.com/sebastianLedzianowski/contact_book.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd contact_book
    ```

3. **Add the `.env` file with the following settings:**

```bash
#PostgreSQL Date Base
SQLALCHEMY_DATABASE_URL=
#Authentication and token generation
SECRET_KEY=
ALGORITHM=
#Email config
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_PORT=
MAIL_SERVER=
MAIL_FROM=
MAIL_STARTTLS=
MAIL_SSL_TLS=
USE_CREDENTIALS=
VALIDATE_CERTS=
#Docker-compose Redis
REDIS_HOST=
REDIS_PORT=
REDIS_DB=
#Docker-compose Postgres
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=
#Cloudinary
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

---

**Note:** Ensure to keep your `.env` file secure and never commit it to the repository to protect sensitive information.

---

4. Create Docker containers to create the PostgresQL server, Redis and the applications itself with the following command:

```bash
docker-compose build
```

5. Run Docker containers:

```bash
docker-compose up
```

## User Instructions 🚀

### 1. Registration and Login

### Registration:
- Go to the API in your browser: http://0.0.0.0:8000/docs. 
- Navigate to the /signup tab.
- Use the "Try it out" button and provide user details (e.g., username, password) for registration.
- Click "Execute" to send the registration request.
- Check your email inbox for a verification message.
- Open the verification email and click on the provided activation link.
- Once the activation link is clicked, return to the API or refresh the browser.
- You should now be successfully registered and activated. Check the response for confirmation.

### Login:
- Go to the API in your browser: http://0.0.0.0:8000/docs.
- Navigate to the `/login` tab.
- Use the "Try it out" button and provide login credentials (e.g., username, password).
- Click "Execute" and check the response.

### 2. Adding Contacts

- After logging in, go to the `/contact` tab.
- Use the "Try it out" button and provide contact details.
- Click "Execute" and check the response.

### 3. Tracking Upcoming Birthdays

- After logging in, go to the `/api/contact/upcoming_birthdays/{days_in_future}` tab.
- Use the "Try it out" button and enter the number of days into the future.
- Click "Execute" and check the response.

### 4. Updating Avatar

- After logging in, go to the /users/avatar tab.
- Use the "Try it out" button and upload an image file for the avatar.
- Click "Execute" and check the response.
- Your avatar is now updated. You can retrieve it using the /users/me/ endpoint.

---

**Note:** Make sure to adhere to the rate limits specified for each operation. The avatar can be updated using the provided FastAPI route /users/avatar, which allows users to change their avatar by uploading a new image file. The uploaded image is securely stored using Cloudinary, and the user's avatar URL is updated in the database.

---

### Additional Information

- 🌐 All contact operations are available only for logged-in users.
- 👤 Each user has access only to their contact operations.
- 🔐 Remember to log in correctly before using the contact-related functions.

---


## Created 👤

- [Sebastian Ledzianowski](https://github.com/sebastianLedzianowski)

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
