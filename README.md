# Django Phonebook API

This is a Django project that provides a Phonebook API for managing users, contacts, and spam reporting.

## Instructions to Run the Project

### 1. Install Dependencies

Install Python 3.x and Django (and other dependencies) as follows:

- Download and unzip the project files into the project folder.
- Navigate to the project folder:
  ```sh
  cd Assessment
  ```
- Create a virtual environment:
  ```sh
  python3 -m venv venv
  ```
- Activate the virtual environment:
  - On Windows:
    ```sh
    venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```sh
    source venv/bin/activate
    ```
- Install required dependencies:
  ```sh
  pip install -r requirements.txt
  ```

### 2. Database Setup

Run the migrations to set up the database:

```sh
python3 manage.py migrate
```

### 3. Run the Development Server

Start the development server:

```sh
python3 manage.py runserver
```

### 4. Testing the API

- You can test the API using Postman or any other API testing tool.
- API documentation for available endpoints is provided at the landing page [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/).

## Available Endpoints

### **User Authentication**

#### **Register a new user**

**POST** `/api/register/`

**Request:**

```json
{
  "name": "xyz",
  "phone_number": "9876543210",
  "password": "password123",
  "email": "xyz@example.com"
}
```

**Response:**

```json
{
  "message": "User registered successfully."
}
```

#### **Login with credentials**

**POST** `/api/login/`

**Request:**

```json
{
  "phone_number": "9876543210",
  "password": "password123"
}
```

**Response:**

```json
{
  "access": "access_token_here",
  "refresh": "refresh_token_here"
}
```

#### **Refresh the access token**

**POST** `/api/token/refresh/`

**Request:**

```json
{
  "refresh": "refresh_token_here"
}
```

**Response:**

```json
{
  "access": "new_access_token_here"
}
```

### **Spam Reporting**

#### **Mark a phone number as spam**

**POST** `/api/mark_as_spam/`

**Request:**

- Headers:
  ```
  Authorization: Bearer <access_token>
  ```
- Body:
  ```json
  {
    "phone_number": "9876543210"
  }
  ```

**Response:**

```json
{
  "message": "Phone number marked as spam successfully."
}
```

### **Search Functionality**

#### **Search for users by name**

**GET** `/api/search-by-name/`

**Request:**

- Query Parameters:
  ```
  query: (string) The name (or part of the name) to search for.
  ```
- Headers:
  ```
  Authorization: Bearer <access_token>
  ```
- Example: `/api/search-by-name/?query=John`

**Response:**

```json
{
  "results": [
    {
      "name": "John Doe",
      "phone_number": "9876543210",
      "spam_likelihood": 0.8
    }
  ]
}
```

#### **Search for users by phone number**

**GET** `/api/search-by-phone/`

**Request:**

- Query Parameters:
  ```
  query: (string) The phone number to search for.
  ```
- Headers:
  ```
  Authorization: Bearer <access_token>
  ```
- Example: `/api/search-by-phone/?query=9876543210`

**Response:**

```json
{
  "results": [
    {
      "name": "John Doe",
      "phone_number": "9876543210",
      "spam_likelihood": 0.8
    }
  ]
}
```

### **Contacts Management**

#### **Get all contacts of the logged-in user**

**GET** `/api/get-contacts/`

**Request:**

- Headers:
  ```
  Authorization: Bearer <access_token>
  ```

**Response:**

```json
{
  "contacts": [
    {
      "contact_name": "Jane Doe",
      "contact_number": "1234567890"
    }
  ]
}
```

#### **Add a contact to the user's contact list**

**POST** `/api/add-contact/`

**Request:**

- Headers:
  ```
  Authorization: Bearer <access_token>
  ```
- Body:
  ```json
  {
    "contact_name": "Jane Doe",
    "contact_number": "1234567890"
  }
  ```

**Response:**

```json
{
  "message": "Contact added successfully."
}
```

## Requirements

- Python 3.x
- Django 3.x+
- Other Python packages listed in `requirements.txt`

## Notes

- The project uses JWT authentication for user login and token management.
- **User Registration**: User provides their name, phone number, password, and email (optional).
- **Login**: After registration, the user logs in with phone number and password to receive `access_token` and `refresh_token`.
- **Access Token**: The access token is used for subsequent API requests in the `Authorization` header.
- You can run the following command to populate the database with test data:
  ```sh
  python3 populate_data.py
  ```
