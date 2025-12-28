# 📚 Library Management System API

A RESTful API built with **Django Rest Framework (DRF)** for managing a library system.  
This API allows managing books, authors, members, and book borrowing/returning functionality.

---

## 🚀 Features

- 📘 Manage Books (CRUD)
- ✍️ Manage Authors and their Books
- 👤 Member-based Record System
- 🔄 Borrow & Return Books
- 🔐 JWT Authentication (Djoser)
- 🔎 Search & Filtering
- 📄 Pagination Support
- 🛡️ Role-based Permissions (Admin / User)

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** JWT (Djoser)
- **Database:** PostgreSQL
- **Filtering:** django-filter
- **API Style:** RESTful
- **Pagination:** Custom DRF Pagination

---

## 🗃️ Database Models

### Author
- `name`
- `biography`

### Book
- `title`
- `author`
- `isbn`
- `category`
- `is_available`

### Member
- `name`
- `email`
- `membership_date`

### Record
- One-to-One with Member

### BorrowRecord
- `book`
- `record`
- `borrow_date`
- `return_date`
- `is_returned`

---

## 🔗 API Endpoints

### 🔐 Authentication
POST /auth/jwt/create/
POST /auth/jwt/refresh/
POST /auth/users/


---

### 📘 Books
GET /api/v1/books/
POST /api/v1/books/
GET /api/v1/books/{id}/
PUT /api/v1/books/{id}/
DELETE /api/v1/books/{id}/

---

### ✍️ Authors
GET /api/v1/author/
POST /api/v1/author/

---

### 👤 Record (Auto Created Per User)
GET /api/v1/record/

---

### 🔄 Borrow / Return Books
GET /api/v1/record/{record_id}/borrow-books/
POST /api/v1/record/{record_id}/borrow-books/
POST /api/v1/record/{record_id}/borrow-books/{borrow_id}/return_book/

---

## 📥 Borrow Book Example

### Request
```json
{
  "book_id": 3
}
Response
json
Copy code
{
  "id": 1,
  "book": {
    "id": 3,
    "title": "Clean Code",
    "isbn": "9780132350884",
    "category": "Programming"
  },
  "borrow_date": "2025-01-10",
  "is_returned": false
}
