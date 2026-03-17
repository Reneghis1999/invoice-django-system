# Django Invoice System

## Overview

Django Invoice System is a simple backend application built with **Django** to manage customers, invoices, and invoice articles.

The goal of this project is to build a structured and scalable foundation for an invoicing application.

Main features include:

* Customer management
* Invoice creation
* Invoice articles management
* Django Admin integration for quick data management

---

# Technologies Used

* Python
* Django
* SQLite (default Django database)
* Django Admin

---

# Project Structure

```
django-invoice/

 django_invoice/     # Django project configuration
 fact_app/           # Main application (customers, invoices, articles)
 manage.py           # Django management script
 requirements.txt    # Project dependencies
 README.md           # Project documentation
```

---

# Installation

## 1. Clone the Repository

```
git clone https://github.com/your-username/django-invoice-system.git
```

Move into the project directory:

```
cd django-invoice
```

---

## 2. Create a Virtual Environment

```
python -m venv venv
```

Activate the environment.

Windows (PowerShell):

```
.\venv\Scripts\activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

If the requirements file is not available yet, install Django manually:

```
pip install django
```

---

# Database Setup

Create migrations:

```
python manage.py makemigrations
```

Apply migrations:

```
python manage.py migrate
```

---

# Create Admin User

To access the Django admin panel, create a superuser:

```
python manage.py createsuperuser
```

Follow the instructions in the terminal.

---

# Run the Development Server

Start the server:

```
python manage.py runserver
```

Open the application in your browser:

```
http://127.0.0.1:8000/admin
```

Login using the superuser credentials.

---

# Models Implemented

## Customer

Represents a customer in the system.

Fields:

* name
* email
* phone
* address
* sex
* age
* city
* zip_code
* created_date
* save_by

---

## Invoice

Represents a customer invoice.

Fields:

* customer
* save_by
* invoice_date_time
* total
* last_updated_date
* paid
* invoice_type
* comments

Invoice types:

* RECU
* PROFORMA FACTURE
* FACTURE

---

## Article

Represents items within an invoice.

Fields:

* invoice
* name
* quantity
* unit_price
* total

Each invoice can contain multiple articles.

---

# Django Admin

The following models are registered in Django Admin:

* Customer
* Invoice
* Article

Custom admin configurations include:

* `list_display` for better data visualization
* simplified management of invoices and customers

Admin panel:

```
http://127.0.0.1:8000/admin
```

---

# Development Workflow

Feature branch used for this implementation:

```
feature/002-define-models
```

Steps completed:

1. Created Django project and application
2. Implemented database models
3. Generated initial migrations
4. Registered models in Django admin
5. Tested functionality through the admin interface
6. Prepared Pull Request for review

---

# Future Improvements

Planned features include:

* Invoice creation views
* Customer management interface
* Article management inside invoices
* HTML templates
* REST API integration
* Authentication improvements

---

# Author

Ghislain
