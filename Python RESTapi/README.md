# Flask User Payments API

This is a simple RESTful API built using **Flask** and **MySQL** to manage users and their payments.

## 📁 Project Structure

├── app.py # Main entry point

├── db.py # Database connection logic

├── config.py # DB configuration

├── schema.sql # MySQL schema

├── models

│ ├── payment_model.py # Payment-related DB operations

│ └── user_model.py # User-related DB operations

├── routes

│ ├── payment_routes.py # Payment routes

│ └── user_routes.py # User routes

├── screenshots

│   ├── swagger-ui.png

│   ├── create-user-postman.png

│   └── payment-response.png

└── requirements.txt # Python dependencies


## Setup

1. Create and Activate Virtual Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Setup MySQL
a) Start MySQL Server
Make sure MySQL server is running on localhost:3306.

(b) Create Database and Tables
```bash
mysql -u root -p
```

4. Run Application 
```bash
python app.py
```
By default, the app runs on: http://localhost:8080


## API Endpoints
Method  -  	Endpoint       -  Description

GET	    -   /users	       -  Get all users

POST    -  	/users	       -  Create a new user

GET	    -   /users/<id>	   -  Get a single user

PUT	    -   /users/<id>	   -  Update a user

DELETE  -  	/users/<id>	   -  Delete a user

GET	    -   /payments	     -  Get all payments

POST    -  	/payments	     -  Create a payment

GET	    -   /payments/<id> -  Get a payment

PUT	    -   /payments/<id> -  Update a payment

DELETE  -  	/payments/<id> -  Delete a payment


## Swagger API Docs
Interactive Swagger UI is available at: http://localhost:8080/apidocs

This allows you to explore and test all API endpoints from the browser.
i've added screenshots you can check


## SCHEMA
schemais available in schema.sql


## EXTRA
You can use tools like Postman, curl  or the built-in Swagger UI to test the API.

No authentication is used to keep things simple for this assignment(JWT can be added for enhancement).
