# MYSTIC MASALA
Mystic Masala is a web-based application designed to streamline the process of booking tables at our Indian restaurant. The application provides an intuitive and user-friendly interface for customers to make table reservations, view their reservations, and manage their bookings. The project aims to enhance the dining experience by ensuring a smooth and efficient table booking process.


## Technologies Used
**Frontend**
- HTML, CSS, JavaScript, Bootstrap for responsive design.

**Backend**
- Django framework for server-side logic and database management.

**Database**
- PostgreSQL for storing user and reservation data.

**Deployment** 
- Deployed on a cloud platform Heroku for accessibility.

**GitHub**
- Web-based platform providing hosting services for Git repositories and collaboration tools.

**Git**
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

## Future implementations

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


## How to Use 

### Login form
##### For Registered Users:
- Enter a valid Username and Password.
- Click on the Login button.
- If the credentials are correct, the app will authenticate the user and allow them to book a table.

##### For New Users:
- Click on the Register link.
- You will be redirected to the registration form.

#### Registration form

- Fill in all the required fields: First Name, Last Name, Email, Username, Password, and Confirm Password.
- Ensure all inputs are valid.
- Click on the Register Now button.
- Upon successful registration, you will be able to log in and book a table.

#### Booking a Table
- Once logged in, navigate to the table booking section.
- Select the table based on capacity and your convenience.
- Choose the date and time for the reservation.
- Select number of guests
- Confirm the booking. The system will validate to prevent double booking for the same table, date, and time.

#### Viewing and Managing Reservations
- upon clicking manage booking, Navigate to the My Bookings page.
- View all future reservations with detailed information.

#### Update Reservations:
- Select the booking you want to modify.
- Change any of the fields as necessary.
- The system will validate changes to ensure no double booking occurs when time or date is changed.

#### Delete Reservations:
- Choose the booking you wish to cancel.
- Click on the Delete button.
- A confirmation pop-up will appear to confirm the deletion.
- Click ok to delete 
- Cancel button will cancel the delete process

## Flow Chart : How the project works


## Validation Rules and Limits

### Login form
- If the username or password is incorrect or not registered, an error message will display: "Invalid username or password".

### Registration form
**First name:**
- Field cannot be empty
- First name should be characters, if not error message will display: "First name can only contain letters"

**Last name:**
- Field cannot be empty
- Last name should be characters, if not error message will display: "Last name can only contain letters"

**Email:**
- Email field cannot be empty.
- Email should contain a '@' symbol
- Email should be in proper format "eg: mysticmasala@gmail.com"
- If the user enterd email already exsists , error message will display: "Email already exsist"

**Username:**
- Field cannot be empty
- Username should contain atleast 8 characters
- Username can be only allowed characters,numbers and special characters.
- If the user enterd username already exsists , error message will display :" Username already exsists"

**Password:**
- Password should contain atleast 8 characters
- Password should not be common one
- A strong password should contain mix of letters,digits and special symbols.

**Confirm Password:**
- If the password doesn't match, Error message will display " Password dont match"


### Book A Table Form :

#### What is UTC?

**UTC (Coordinated Universal Time)** 
- UTC is the primary time standard by which the world regulates clocks and time. It is used as a reference for timekeeping globally, ensuring synchronization across different regions and systems.

**UTC Validation:**
- Bookings cannot be made for past times.
- Bookings must be within restaurant operating hours (10:00 AM to 10:00 PM UTC).
- Bookings must be made at least 2 hours before closing time (by 8:00 PM UTC).

#### Booking date:
- Field cannot be empty
- User cannot book a table in past date

#### Booking Time:
- Field cannot be empty
- User cannot book a table in past time

**Phone number:**
- Phone number field is optional
- If user enters a phone number , if it is 0 , error message will display "password cannot be zero"
- Phone number cannot be less than 10 digits
- Phone number cannot be greater than 15 digits

**Number of guests:**
- Number of guests will only be postive numbers
- Number of giests cannot be 0
- If number of guest if greater than table capacity, errro messsage will display:" Table capacity is less han number of guests"

**Special Requests:**
- Special request is an optional field
- Special request cannot be more than 200 characters.


### Update Form 

 **Booking Date and Time:**
  - If the date or time has changed, validate the new date and time against existing bookings.
  - If no change in date or time, update other details directly.
  - If a booking conflict is detected, return an appropriate error message.
    
**Phone number:**
- Phone number field is optional
- If user enters a phone number , if it is 0 , error message will display "password cannot be zero"
- Phone number cannot be less than 10 digits
- Phone number cannot be greater than 15 digits

**Number of guests:**
- Number of guests will only be postive numbers
- Number of giests cannot be 0
- If number of guest if greater than table capacity, errro messsage will display:" Table capacity is less han number of guests"

**Special Requests:**
- Special request is an optional field
- Special request cannot be more than 200 characters.

**Delete Button:**
- Get a confirmation from user to delete
- If user clicks ok, then delete the particular record
- If user clicks cancel, record will not be deleted


## Testing

### Pep8 Validation


### Functional Testing

#### Login Page

**Valid Input**

|Test Case|User Input|Expected Behaviour|Pass / Fail|
|---------|----------|------------------|-----------|
|Case 1|Enter valid usename,password and click login|Render book a table form | Pass|
|Case 2|Click Refister link to signup|Render signup form|Pass|

**Invalid Input**
|Test Case|User Input|Expected Behaviour|Pass / Fail|
|---------|----------|------------------|-----------|
|Case 1|Enter invalid username password and click login| Display error message"Invalid username or password"| Pass|
|Case 2|Enter valid username but leave password blank,click login|Display error message "Password is required"|Pass|
|Case 3|Enter valid username but wrong password,click login| Display error message"Invalid username or password"|pass|
|Case 4|Enter invalid username valid password,click login |  Display error message"Invalid username or password"|pass|                  




