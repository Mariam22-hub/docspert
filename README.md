# Fund Transfer Web Application

## Project Overview

This project is a Django-based web application that handles fund transfers between two accounts. It supports importing a list of accounts with opening balances, querying these accounts, and transferring funds between any two accounts. The application features:

- Importing accounts from CSV files
- Listing all accounts
- Viewing account information
- Transferring funds between accounts
- Notification for insufficient funds during transfer
- Notification for duplicate file uploads during account import

## Features

1. **Import Accounts**:
   - Upload a CSV file to import account data.
   - The application checks for duplicate file uploads and notifies the user if the file has already been uploaded.

2. **List Accounts**:
   - View a list of all accounts along with their balances.

3. **View Account Information**:
   - Retrieve detailed information about a specific account.

4. **Transfer Funds**:
   - Transfer funds between two accounts.
   - Notification is displayed for insufficient funds.

5. **Notifications**:
   - Alerts for duplicate file uploads during import.
   - Alerts for insufficient funds during fund transfer.

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (optional but recommended for a robust setup)
- Django 5.0.7

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repo_name>
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Configure Database**:
    Open fund_transfer/settings.py and configure the DATABASES setting for PostgreSQL or use the default SQLite configuration.
4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
4. **Run Server**:
  ```bash
  python manage.py runserver
```

Open your web browser and navigate to http://127.0.0.1:8000/accounts.
