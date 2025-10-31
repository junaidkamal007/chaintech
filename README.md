# Chaintech

Chaintech is a simple and powerful web application built with **Django**, a high-level Python web framework that encourages rapid development and clean, pragmatic design. This project includes essential features like user authentication, a database interface, and an optional REST API.

---

## 🚀 Features

- **Django 5+** (or your preferred version)
- User authentication: login, logout, and register
- Database support: SQLite (default) or PostgreSQL
- Admin panel for managing data
- REST API (if applicable)

---

## 🛠️ Installation

Follow the steps below to get your local environment set up and running.

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/junaidkamal007/chaintech.git
cd chaintech
```

## 2. Set up a Virtual Environment (Optional but Recommended)

It's a good practice to create a virtual environment to keep dependencies isolated.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

## 3. Install Dependencies

Install the required packages from the requirements.txt file:
```bash
pip install -r requirements.txt
```

## 4. Configure Database

By default, the project uses SQLite. If you'd like to use PostgreSQL, follow these steps:

 - Install PostgreSQL and configure a new database.

 - Update the DATABASES setting in settings.py with your PostgreSQL database credentials.

For SQLite (default), no changes are needed.

## 5. Apply Migrations

Run the following command to set up the database schema:
```bash
python manage.py migrate
```

## 6. Create a Superuser

To access the Django admin panel, you'll need to create a superuser account:
```bash
python manage.py createsuperuser
```

Follow the prompts to set the username, email, and password.

## 7. Start the Development Server

Run the server with the following command:
```bash
python manage.py runserver
```

The development server should now be running. You can access the app in your browser at:
```bash
http://127.0.0.1:8000/
```

To access the Django admin panel, go to:
```bash
http://127.0.0.1:8000/admin/
```

Login with the superuser credentials you created earlier.
