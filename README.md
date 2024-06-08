# social-networking-application

Django Social Networking API with JWT Authentication
This Django application provides a set of APIs for a social networking platform. Users can sign up, log in, search for other users, send/accept/reject friend requests, list friends, and manage pending friend requests. JWT token authentication is used for secure authentication.

Installation
To run this Django application locally, follow these steps:

Clone the repository:

git clone <git@github.com:amanbondekar/social-networking-application.git>
cd <repository-directory>

Install requirement using 

pip install -r requirements.txt

Install Docker and Docker Compose:

Follow the official Docker documentation to install Docker Desktop for your operating system.

Set up JWT Authentication:

Install djangorestframework-simplejwt package:


pip install djangorestframework-simplejwt
Add rest_framework_simplejwt to your Django settings:

python
Copy code
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Add other authentication classes if needed
    ],
}

Build the Docker image:


docker-compose build
Start the Docker container:

docker-compose up
Access the Django application:

Open your web browser and go to http://localhost:8000

APIs Overview

Authenticate user
Login: Users can log in with their email and password. Email is case-insensitive. Upon successful login, JWT tokens are generated.

Signup: Users can sign up with their email only. No OTP verification is required.


User Management(socail apis)
Search Users: Search for other users by email or name. Pagination is applied with 10 records per page.
If the search keyword matches an exact email, return the user associated with that email.
If the search keyword contains any part of the name, return a list of all users whose names contain that keyword.

Friend Requests: Users can send, accept, or reject friend requests.

Users can send a friend request to other users.

Users can view pending friend requests and accept or reject them.


List Friends: List all users who have accepted friend requests.
Throttling
Friend Request Throttling: Users cannot send more than 3 friend requests within a minute.
Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License

Replace <git@github.com:amanbondekar/social-networking-application.git> with the URL of your Git repository, and <repository-directory> with the directory name if applicable.

This README file provides an overview of the installation process and the functionalities offered by the Django Social Networking API with JWT authentication. It aims to make it easier for users to set up and use the application, as well as for contributors to understand the project structure and contribute to its development.

