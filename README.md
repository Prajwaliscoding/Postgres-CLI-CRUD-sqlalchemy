# 🗃️ Postgres CLI CRUD with SQLAlchemy

A simple command-line app that demonstrates **CRUD operations** (Create, Read, Update, Delete) for users and their tasks, using:

- 📦 **SQLAlchemy** (ORM)
- 🔐 **dotenv** for environment variable management
- 🐘 **PostgreSQL** as the database
- 🧠 Fully modular, terminal-based, and human-friendly

---

## 📁 Features

- ✅ Add new users and tasks
- 📋 List users and their tasks
- 🔄 Update user details
- ❌ Delete users or their tasks
- 🚫 Prevent duplicate users by email

---

## 💻 How to Run It Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Prajwaliscoding/Postgres-CLI-CRUD-sqlalchemy.git
cd Postgres-CLI-CRUD-sqlalchemy
```
### 2. Set Up PostgreSQL

Make sure PostgreSQL is installed and running on your system.
Then open your terminal or PostgreSQL GUI (e.g., pgAdmin) and create a database:
``` sql
CREATE DATABASE dbname;
```
You can use any database name. Just make sure it matches the name in your .env file.

### 3. Create a .env File
In the root of your project folder, create a .env file and add the following:
```env
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mycruddb
```
⚠️ Do not commit this file. Make sure your .gitignore includes .env

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the App
```bash
python main.py
```
