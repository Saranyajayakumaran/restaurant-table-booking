# MYSTIC MASALA
Mystic Masala is a web-based application designed to streamline the process of booking tables at our Indian restaurant. The application provides an intuitive and user-friendly interface for customers to make table reservations, view their reservations, and manage their bookings. The project aims to enhance the dining experience by ensuring a smooth and efficient table booking process.


### Technologies Used
#### Frontend
- HTML, CSS, JavaScript, Bootstrap for responsive design.
#### Backend
- Django framework for server-side logic and database management.
#### Database
- PostgreSQL for storing user and reservation data.
#### Deployment 
- Deployed on a cloud platform Heroku for accessibility.
#### GitHub
- Web-based platform providing hosting services for Git repositories and collaboration tools.
#### Git
- A distributed version control system for tracking changes in source code

## Features
### Customer Features
#### Home page
- Home page contains basic detailed description about restaurant ,special offers and contact details.
- Users can book a table by clicking the "Book a Table with Us" button or navigating to the "Book a Table" link.

#### Menu Page
- Menu page contais all the menu available in restaurant with price and detailed description.

#### User Registration and Login: 
- Secure user accounts for managing reservations and personal details.
- Authenticates users based on valid username and password and redirects to the booking page.
- New users can register their details on the registration page.

#### Table Reservation
- Allows customers to view table capacity and select based on their convenience.
- Customers can book tables for specific dates and times.
- Validates to prevent double booking if the table is already booked for the same date and time.

#### My bookings
- Customers can view their booking details for both past and future reservations.
- Double booking validation occurs when booking time or date is changed.

#### Update Reservations
- Customer can modify their booking in all the fields.
- Double booking validation occurs when booking time or date is changed.

#### Delete Reservations
- Customers can cancel bookings by deleting specific reservations.
- A deletion confirmation pop-up appears when the user tries to delete a record.

### Admin Features
#### Admin Dashboard
- Provides an overview of all reservations, table capacity, and customer details.

#### Manage Tables
- Admin can add, remove, or update table information.

#### View Reservations 
- Displays a comprehensive list of all reservations with options to modify or cancel them.

#### User Management
- Allows management of customer accounts and their reservation history.

### Future implementations

#### Real-time Table Availability:
- Implement real-time updates for table availability to reflect bookings and cancellations immediately.

#### Mobile App Integration:
- Develop a mobile application for both iOS and Android to make reservations even more accessible.

#### SMS or Email Notifications:
- Implement SMS notifications for booking confirmations, reminders, and cancellations.

#### Waitlist Management:
- Introduce a waitlist feature where customers can join a waitlist if no tables are available and be notified when a table becomes free.

#### Table Preferences:
- Let customers specify table preferences (e.g., window seat, near a specific area) during booking.

#### Integration with Calendar Apps:
- Enable customers to add their reservations to their Google Calendar, Apple Calendar, or other calendar apps with a single click.


### How to Use 

#### Login form
##### For Registered Users:
- Enter a valid Username and Password.
- Click on the Login button.
- If the credentials are correct, the app will authenticate the user and allow them to book a table.

##### For New Users:
- Click on the Register link.
- You will be redirected to the registration form.

#### Registration form

- Give all the valid inputs and click register now
- User will be registered and can login and book a table