# AcademiNet - Installation and Setup Guide

## Description
AcademiNet is an online space designed for students, offering essential information about the rights and benefits you deserve. On this website, you will find useful and practical information related to university life and beyond. The site features a student forum for asking questions, getting help on various subjects, and joining study groups.

## Authors
- Eden Cohen - edenco5@ac.sce.ac.il
- Felix Khmelnitsky - khmelfe@ac.sce.ac.il
- Shir Cohen - shirco3@ac.sce.ac.il
- Rotem Bahalker - rotemba3@as.sce.ac.il

## Installation Instructions

### Prerequisites
Make sure Python is installed on your computer. If not, download and install the latest version from [python.org](https://www.python.org/).

### Setup for Windows
1. Open the command prompt (cmd).
2. Type `pip install django` and press Enter.

### Setup for Mac
1. Open Terminal, which you can find in the 'Applications' folder under 'Utilities'.
2. Type `sudo pip3 install django` and press Enter.

## Database Setup
This project uses SQLite3 as its database, which is a lightweight disk-based database that does not require a separate server process.

### Configuring the Database
1. Ensure your Django settings file (`settings.py`) is set to use SQLite as its default database:
   
 DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',}
   }

##Create the necessary database tables:

python manage.py makemigrations
python manage.py migrate

##Running the Application
Start the development server:
python manage.py runserver

Access the web app in a browser at http://127.0.0.1:8000/ to check if everything is running correctly.

Additional Dependencies

##Install the following packages to ensure full functionality of the application:
pip install django-adminlte3
pip install django-admin-interface
pip install django-colorfield
pip install django-crispy-forms
pip install django-admin-logs
pip install chartjs

Running Tests

##Ensure your application is functioning correctly by running:
pip install django-test
pip install unittest2
pip install django-reverse-js
pip install resolve

##How to Use
For a detailed guide on how to use AcademiNet, refer to the documentation provided in the project's repository or the additional resources included in the setup files