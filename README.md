# README

## Project Name
Access Control System Prototype

## Authors
- Manaog, Johnlerein B. (BSCS 3A)
- Fajardo, Jude Daniel F.

## Executive Summary
This project is a prototype access control system designed for small organizations. Implemented as a web application using Python and Flask, it demonstrates essential features such as user authentication, role-based access control, and basic identity management. It provides a foundation for enhancing functionality and security with additional features.

## Features
### User Authentication
- **Secure Login and Logout**: Utilizes session management.
- **Password Hashing**: Ensures secure password storage using SHA-256.

### Role-Based Access Control (RBAC)
- **Admin Role**: Access to user management features like registration and deletion.
- **Regular User Role**: Limited to profile management.

### User Management
- **Registration**: Admin-only feature for adding new users.
- **Deletion**: Admins can delete users.
- **View Users**: Admins can view a list of registered users.

### Profile Management
- **Edit Profile**: Users can update personal information.
- **Change Password**: Users can securely update passwords.
- **Profile Pictures**: Upload and display profile pictures.

### Security Measures
- **Password Hashing**: Prevents password leakage.
- **CSRF Protection**: Guards against cross-site request forgery.
- **Session Management**: Enhances session security.
- **Cache Control Headers**: Prevents sensitive data from being cached.

### Database Integration
- **Database**: MySQL for data storage.
- **ORM**: XAMPP for database operations.

## Technical Stack
- **Backend**: Python with Flask.
- **Database**: MySQL.
- **Authentication**: Flask-Login.
- **Frontend**: HTML templates.

## Design and Architecture
- **Modular Design**: Simplifies maintenance and scalability.
- **RBAC**: Ensures clear user privilege separation.
- **Secure Sessions**: Managed using Flask's session framework.
- **Database Sanitization**: Prevents SQL injection vulnerabilities.

## Challenges and Solutions
- **Database Connectivity**: Resolved with configuration parser.
- **Authentication**: Enhanced with password hashing and session checks.
- **Role Validation**: Secured using session-based role verification.

## Future Improvements
- Add Two-Factor Authentication (2FA).
- Enforce strong password policies.
- Implement audit logging for user actions.
- Support advanced RBAC with dynamic role creation.
- Upgrade to modern frontend frameworks like React or Vue.js.
- Integrate Single Sign-On (SSO) with OAuth or SAML providers.

## Third-Party Libraries and Tools
- Flask
- Flask-Login
- MySQL
- ConfigParser
- Hashlib

## User Manual
### Installation and Setup
1. Install Python and pip.
2. Clone the repository.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database in `config.ini`.
5. Run the application.

### Admin Role
- **Register Users**: Access `/register`.
- **Delete Users**: Access `/users` to manage users.
- **View Users**: Access `/users` to view registered users.

### Regular User Role
- **Login**: Access `/login`.
- **Manage Profile**: Access `/profile` to edit information or change passwords.

### Troubleshooting
- **Database Connection Issues**:
  - Verify database configuration in `config.ini`.
  - Ensure MySQL server is running.
- **Login Issues**:
  - Check username and password.
  - Review server logs for errors.
- **Permission Denied**:
  - Confirm user roles in the database.

"# InfoAssSecFinal" 
