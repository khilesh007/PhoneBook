Django Phonebook API

This is a Django project that provides a Phonebook API for managing users, contacts, and spam reporting.

Instructions to Run the Project

1. Install Dependencies
   Install Python 3.x and Django (and other dependencies) as follows:

   - Download and unzip the project files into the project folder.

   - Navigate to the project folder:
     cd Assessment

   - Create a virtual environment:
     python3 -m venv venv

   - Activate the virtual environment:
     - On Windows:
       venv\Scripts\activate
     - On macOS/Linux:
       source venv/bin/activate

   - Install required dependencies:
     pip install -r requirements.txt

2. Database Setup
   - Run the migrations to set up the database:
     python3 manage.py migrate

3. Run the Development Server
   - Start the development server:
     python3 manage.py runserver

4. Testing the API
   - You can test the API using Postman or any other API testing tool.
   - API documentation for available endpoints is provided at the landing page (`http://127.0.0.1:8000/`).

5. Available Endpoints

   - **POST** `/api/register/`: Register a new user.

   Request:
    Body (JSON):
    {
      "name": "xyz",
      "phone_number": "9876543210",
      "password": "password123",
      "email": "xyz@example.com"
    }
    Response:

        Status: 200 OK
        Body:
    {
      "message": "User registered successfully."
    }

   - **POST** `/api/login/`: Login with credentials.
    Request:
      Body (JSON):
      {
        "phone_number": "9876543210",
        "password": "password123"
      }
    Response:
        Status: 200 OK
        Body:
    {
      "access": "access_token_here",
      "refresh": "refresh_token_here"
    }

   - **POST** `/api/mark_as_spam/`: Mark a phone number as spam.
    Request:
      Headers:
          Authorization: Bearer <access_token>
      Body (JSON):
      {
        "phone_number": "9876543210"
      }
    Response:
        Status: 200 OK
        Body:
        {
          "message": "Phone number marked as spam successfully."
        }

   - **GET** `/api/search-by-name/`: Search for users by name.
    Request:
      Query Parameters:
          query: (string) The name (or part of the name) to search for.
      Headers:
          Authorization: Bearer <access_token>

      Example: /api/search-by-name/?query=John
    Response:
        Status: 200 OK
        Body:
        {
          "results": [
            {
              "name": "John Doe",
              "phone_number": "9876543210",
              "spam_likelihood": 0.8
            }
          ]
        }

   - **GET** `/api/search-by-phone/`: Search for users by phone number.
      Request:
        Query Parameters:
            query: (string) The phone number to search for.
        Headers:
            Authorization: Bearer <access_token>
        Example: /api/search-by-phone/?query=9876543210
    Response:
        Status: 200 OK
        Body:
        {
          "results": [
            {
              "name": "John Doe",
              "phone_number": "9876543210",
              "spam_likelihood": 0.8
            }
          ]
        }
   - **GET** `/api/get-contacts/`: Get all contacts of the logged-in user.
    Request:
      Headers:
          Authorization: Bearer <access_token>
    Response:
        Status: 200 OK
        Body:
        {
          "contacts": [
            {
              "contact_name": "Jane Doe",
              "contact_number": "1234567890"
            }
          ]
        }
   - **POST** `/api/add-contact/`: Add a contact to the user's contact list.
    Request:
      Headers:
          Authorization: Bearer <access_token>
      Body (JSON):
      {
        "contact_name": "Jane Doe",
        "contact_number": "1234567890"
      }
    Response:
        Status: 200 OK
        Body:
        {
          "message": "Contact added successfully."
        }
   - **POST** `/api/token/refresh/`: Refresh the access token.
    Request:
        Body (JSON):
        {
          "refresh": "refresh_token_here"
        }
    Response:
        Status: 200 OK
        Body:
        {
          "access": "new_access_token_here"
        }

Requirements

- Python 3.x
- Django 3.x+
- Other Python packages listed in `requirements.txt`

Notes

- The project uses JWT authentication for user login and token management.
- **User Registration**: User provides their name, phone number, password, and email (optional).
- **Login**: After registration, the user logs in with phone number and password to receive `access_token` and `refresh_token`.
- **Access Token**: The access token is used for subsequent API requests in the `Authorization` header.
- You can run **python3 populate_data.py** to populate the database with test data.
