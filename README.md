
# Library Management System

A Django REST API for managing a library system where users can register, browse, borrow, and return books with penalty tracking. Admins can manage books, authors, categories, and borrowing is limited and tracked with due dates.

---

## Features

- User registration and JWT-based authentication
- Browse and filter books by author and category
- Borrow books with a maximum limit of 3 active borrows
- Automatic inventory updates with atomic transactions
- Book return functionality with late return penalty points
- Admin panel to manage books, authors, and categories

---

## Installation

Follow the steps below to set up the project locally:

1. **Clone the repository**

   ```bash
   git clone https://github.com/thatsayon/library-management.git
   cd library-management
   ```

2. **Create and activate a virtual environment**

   - On Windows:

     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

## Usage

- Access the API at `http://localhost:8000/api/`
- Use the admin panel at `http://localhost:8000/admin/` to manage books, authors, and categories.
- Register and authenticate users using the provided endpoints.
- Borrow and return books while respecting borrowing limits and penalty rules.

---

## API Endpoints

### Authentication

- `POST /api/register/` — Register a new user
- `POST /api/login/` — Obtain JWT token

### Books & Metadata

- `GET /api/books/` — List books (supports filtering by author and category)
- `GET /api/books/{id}/` — Retrieve book details
- `POST /api/books/` — Create a new book (admin only)
- `PUT /api/books/{id}/` — Update a book (admin only)
- `DELETE /api/books/{id}/` — Delete a book (admin only)
- `GET /api/authors/` — List authors (admin only to create)
- `POST /api/authors/` — Create an author (admin only)
- `GET /api/categories/` — List categories (admin only to create)
- `POST /api/categories/` — Create a category (admin only)

### Borrowing

- `POST /api/borrow/` — Borrow a book (max 3 active borrows)
- `GET /api/borrow/` — List active borrows of the authenticated user
- `POST /api/return/` — Return a borrowed book (calculates penalties if late)
- `GET /api/users/{id}/penalties/` — View penalty points (admin and self access only)

---

## Borrowing & Penalty Logic

- Users can borrow up to 3 books simultaneously.
- Each borrow sets a due date 14 days after the borrow date.
- Books can only be borrowed if copies are available.
- Returning a book updates inventory atomically.
- Late returns add penalty points equal to days overdue.

---

## Contributing

Contributions are welcome! Please fork the repository and open a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, open an issue or contact the maintainer via GitHub.