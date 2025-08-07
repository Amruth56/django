# STEP 1:  Create Django Project
* django-admin startproject curd
* cd crud

# STEP 2 :  Create Django App
* python manage.py startapp blog


* add the project names into the INSTALLEd_APPS in crud/setings.py


# STEP 3: Create Model
 * in blog/models.py

# STEP 4: Create Datebase Tables
```bash
python manage.py makemigrations
python manage.py migrate
```
# STEP 5: Register Model in Admin
* in blog/admin.py
* Create a superuser to access Django Admin:
```bash 
python manage.py createsuperuser
```
# STEP 6: Create CRUD Views
* blog/views.py


# STEP 7: Create Forms
* blog/forms.py


# STEP 8: Create URLS 
* blog/urls.py
*crud/urls.py

# STEP 9: Create Templates
1. post_list.html
2. postform.html
3. post_confirm_delete.html

# STEP 10: Run server
* pyhton manage.py runserver