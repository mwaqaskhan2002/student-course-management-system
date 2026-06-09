# Student Course Management System 

A robust, production-grade, and highly optimized **Django Student Management System** built with Python and Bootstrap 5. This project demonstrates clean architecture, secure backend validations, database optimization tactics, and dynamic conditional frontend fields.

---

##  Key Features

* **Advanced Search & Filtering:** Live lookup across Students, Departments, and Courses simultaneously using Django `Q` objects.
* **Database Optimization:** Zero N+1 query explosion bugs. Utilizes `select_related` and `prefetch_related` for lightning-fast database execution.
* **Dynamic Form Interaction:** AJAX-driven dependent dropdown system—selecting a department dynamically filters and displays only its corresponding courses.
* **Robust Backend Validation:** Strict custom `RegexValidator` system mapping correct constraints for phone numbers, uppercase course codes (e.g., CS101), and alphabetic names.
* **CRUD Ecosystem:** Secure Class-Based Views (`ListView`, `CreateView`, `UpdateView`, `DeleteView`) with enforced safe-delete architectures.

---

##  Tech Stack & Concepts Demonstrated

* **Backend:** Python, Django (ORM)
* **Database:** SQLite3 
* **Frontend:** HTML5, Bootstrap 5, 
* **Best Practices:** Separation of concerns (Validators $\rightarrow$ Models $\rightarrow$ Forms $\rightarrow$ Views)

---

## 📂 Project Structure Overview

* **`models.py`**: Custom data tier validation, relational mapping (Many-to-Many & Foreign Keys).
* **`forms.py`**: Overridden form field assets, customized HTML attributes, and conditional lookup queryset structures.
* **`views.py`**: Clean handling of logic pipelines with specialized search filters and custom delete safeguards.

---

## 🚀 How To Setup & Run Locally

### 1. Clone the repository
```bash
git clone [https://github.com/mwaqaskhan2002/student-course-management-system.git](https://github.com/mwaqaskhan2002/student-course-management-system.git)
cd student-course-management-system
```

### 2. Set up and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Django
```bash
pip install django
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

👨‍💻 Author
Muhammad Waqas Khan
