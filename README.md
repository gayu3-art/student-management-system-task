# Student Management System

A production-ready Django application for managing student records.

## Features
- **Student Management**: Create, Read, Update, and Delete (CRUD) student records.
- **Authentication**: Secure login and logout system. All views are protected.
- **Data Validation**: 
  - Phone number must be exactly 10 digits.
  - Email addresses must be unique.
- **Modern UI**: Built with Bootstrap 5 and custom styling for a premium feel (Sidebar, Glassmorphism touches).
- **Responsive Design**: Works on mobile and desktop.

## Screenshots

### Login Page
![Login Page](screenshots/login_page.png)

### Student List Dashboard
![Student List](screenshots/student_list.png)

### Add/Edit Student Form
![Add Student](screenshots/student_form.png)

### Student Detail View
![Student Details](screenshots/student_detail.png)

## Model Design
The core **Student** model includes the following fields:
- `name`: Full name of the student.
- `email`: Email address (Unique, validated).
- `phone`: Contact number (Validated for 10 digits using RegexValidator).
- `course`: Enrolled course.
- `date_of_joining`: Date of enrollment.

## Setup Instructions

Follow these steps to set up the project locally.

### Prerequisites
- Python 3.8 or higher installed on your system.

### Step 1: Create a Virtual Environment
Open your terminal in the project directory and run:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Requirements
Install Django (and any other dependencies if listed, or just Django for now):

```bash
pip install -r requirements.txt
```

*(Note: This project uses Django 4.2 LTS)*

### Step 3: Apply Database Migrations
Initialize the SQLite database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create an Admin User
To access the admin panel and log in to the system (since registration is not open to public):

```bash
python manage.py createsuperuser
```
Follow the prompts to set a username and password.

### Step 5: Run the Development Server
Start the server:

```bash
python manage.py runserver
```

### Step 6: Access the Application
1. Open your browser and go to `http://127.0.0.1:8000/`.
2. You will be redirected to the Login page.
3. Log in with the superuser credentials you created in Step 4.
4. You will be directed to the Student Dashboard.

## REST API

This project includes a **fully functional REST API** built with Django REST Framework.

### Quick Start

**Base URL:** `http://127.0.0.1:8000/api/`

**Authentication:** Basic Auth or Session Auth
```bash
# Using Basic Auth
curl -u username:password http://127.0.0.1:8000/api/students/
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/` | List all students (paginated, searchable, filterable) |
| POST | `/api/students/` | Create a new student |
| GET | `/api/students/{id}/` | Get student details with computed fields |
| PUT | `/api/students/{id}/` | Update student (full) |
| PATCH | `/api/students/{id}/` | Update student (partial) |
| DELETE | `/api/students/{id}/` | Delete student |
| GET | `/api/students/statistics/` | Get student statistics & analytics |
| POST | `/api/students/bulk_create/` | Create multiple students at once |

### Enhanced API Features

✨ **New in this version:**
- **Advanced Filtering**: Filter by course, search across multiple fields
- **Custom Validation**: Enhanced validation with detailed error messages
- **Computed Fields**: `days_since_joining` automatically calculated
- **Statistics Endpoint**: Get aggregated data and insights
- **Bulk Operations**: Create multiple students in one request
- **CORS Support**: Ready for frontend integration (React, Vue, etc.)
- **Browsable API**: Interactive web interface at `/api/`

### Query Parameters

- **Search**: `?search=query` - Search by name, email, or course
- **Filter**: `?course=Computer%20Science` - Filter by exact course
- **Ordering**: `?ordering=-date_of_joining` - Sort (use `-` for descending)
- **Pagination**: `?page=2` - Navigate pages (10 items per page)

### Example API Usage

**List Students with Search:**
```bash
curl -u admin:password "http://127.0.0.1:8000/api/students/?search=John&ordering=-date_of_joining"
```

**Create Student:**
```bash
curl -u admin:password \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "course": "Computer Science",
    "date_of_joining": "2026-01-15"
  }' \
  http://127.0.0.1:8000/api/students/
```

**Get Statistics:**
```bash
curl -u admin:password http://127.0.0.1:8000/api/students/statistics/
```

**Bulk Create:**
```bash
curl -u admin:password \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "students": [
      {"name": "Student 1", "email": "s1@example.com", "phone": "1111111111", "course": "Physics", "date_of_joining": "2026-01-15"},
      {"name": "Student 2", "email": "s2@example.com", "phone": "2222222222", "course": "Chemistry", "date_of_joining": "2026-01-15"}
    ]
  }' \
  http://127.0.0.1:8000/api/students/bulk_create/
```

### Testing the API

**Option 1: Python Script**
```bash
python test_api.py
```

**Option 2: Postman**
1. Import `Student_Management_API.postman_collection.json`
2. Update authentication credentials
3. Test all endpoints interactively

**Option 3: Browsable API**
1. Navigate to `http://127.0.0.1:8000/api/`
2. Log in with your credentials
3. Explore endpoints in your browser

### Project Structure
- `config/`: Project main configuration (settings, urls).
- `students/`: The main app containing models, views, and forms.
- `templates/`: Global templates (base.html, login).
- `static/`: CSS and other static assets.
