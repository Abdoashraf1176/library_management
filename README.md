# 📚 Library Management Module for Odoo 17

A comprehensive library management system for Odoo 17 Enterprise that allows you to manage books, authors, and orders both in the backend and through a public-facing website.

## 🎯 Features

### Backend Features
- ✅ **Book Management**: Track books with ISBN, authors, cover images, and availability
- ✅ **Author Management**: Manage author profiles with biographies
- ✅ **Order Management**: Handle book orders with draft and sold status
- ✅ **Smart Buttons**: Quick access to related records (orders per book, books per author)
- ✅ **Computed Fields**: Automatic calculation of sold copies, available copies, and availability status
- ✅ **Security Groups**: Librarian role with full access control
- ✅ **Validation**: Constraints to ensure data integrity

### Website Features
- ✅ **Public Book Catalog**: Browse available books with cover images
- ✅ **Book Details Page**: View complete book information including authors and availability
- ✅ **Online Ordering**: Create draft orders directly from the website
- ✅ **Responsive Design**: Works on all devices (desktop, tablet, mobile)
- ✅ **CSRF Protection**: Secure form submissions

## 📁 Module Structure

```
library_management/
├── __init__.py
├── __manifest__.py
├── README.md
├── controllers/
│   ├── __init__.py
│   └── main.py
├── models/
│   ├── __init__.py
│   ├── library_book.py
│   ├── library_author.py
│   └── library_order.py
├── views/
│   ├── library_book_views.xml
│   ├── library_author_views.xml
│   ├── library_order_views.xml
│   ├── website_templates.xml
│   └── menuitems.xml
├── security/
│   ├── library_security.xml
│   └── ir.model.access.csv
└── static/
    └── description/
        └── icon.png
```

## 🗄️ Data Models

### 1. Library Book (`library.book`)

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Book title (Required) |
| `isbn` | Char | International Standard Book Number |
| `author_ids` | Many2many | Related authors |
| `published_date` | Date | Publication date |
| `cover_image` | Binary | Book cover image |
| `summary` | Text | Book description |
| `total_copies` | Integer | Total number of copies |
| `sold_copies` | Integer | Number of sold copies (Computed) |
| `available_copies` | Integer | Available copies (Computed) |
| `is_available` | Boolean | Availability status (Computed) |
| `order_ids` | One2many | Related orders |
| `order_count` | Integer | Number of orders (Computed) |

**Computed Logic:**
- `sold_copies` = Count of orders with status 'sold'
- `available_copies` = `total_copies` - `sold_copies`
- `is_available` = `available_copies` > 0

### 2. Library Author (`library.author`)

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Author name (Required) |
| `biography` | Text | Author biography |
| `book_ids` | Many2many | Related books |
| `book_count` | Integer | Number of books (Computed) |

### 3. Library Order (`library.order`)

| Field | Type | Description |
|-------|------|-------------|
| `book_id` | Many2one | Related book (Required) |
| `customer_name` | Char | Customer name (Required) |
| `status` | Selection | Order status (draft/sold) |
| `order_date` | Date | Order date |

**Status Values:**
- `draft`: Reservation made but not confirmed
- `sold`: Book has been delivered

## 🚀 Installation

### Prerequisites
- Docker and Docker Compose installed
- Git
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space

## Installation Methods

Choose one of the following installation methods:

---

## 🐳 Method 1: Docker Installation (Recommended)

### Step 1: Clone the Repository

```bash
# Clone your module repository
git clone <your-repository-url> library_management
cd library_management
```

### Step 2: Create Docker Compose File

Create a file named `docker-compose.yml` in your project root:

```yaml
version: '3.8'

services:
  web:
    image: odoo:17.0
    container_name: odoo17_library
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./library_management:/mnt/extra-addons/library_management
      - ./config:/etc/odoo
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    restart: always

  db:
    image: postgres:15
    container_name: postgres_library
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - odoo-db-data:/var/lib/postgresql/data/pgdata
    restart: always

volumes:
  odoo-web-data:
  odoo-db-data:
```





### Step 3: Assign Security Groups

1. Go to **Settings → Users & Companies → Users**
2. Select a user
3. In the **Access Rights** tab, find "Library Management"
4. Check the **"Librarian"** role

## 📖 Usage Guide

### Backend Usage

#### Managing Books

1. **Navigate to Books**:
   - Main menu → **Library** → **Books**

2. **Create a New Book**:
   - Click **Create**
   - Fill in the book details:
     - Title (required)
     - ISBN
     - Authors (select or create)
     - Published Date
     - Upload Cover Image
     - Set Total Copies (default: 1)
     - Add Summary
   - Click **Save**

3. **View Book Orders**:
   - Open a book record
   - Click the **"Orders"** smart button at the top
   - View all orders for this book

#### Managing Authors

1. **Navigate to Authors**:
   - Main menu → **Library** → **Authors**

2. **Create a New Author**:
   - Click **Create**
   - Enter author name (required)
   - Add biography
   - Link existing books or create new ones
   - Click **Save**

3. **View Author's Books**:
   - Open an author record
   - Click the **"Books"** smart button at the top
   - View all books by this author

#### Managing Orders

1. **Navigate to Orders**:
   - Main menu → **Library** → **Orders**

2. **Create a New Order**:
   - Click **Create**
   - Select a book
   - Enter customer name
   - Click **Save**

3. **Confirm an Order**:
   - Open a draft order
   - Click **"Confirm Order"** button in the header
   - Status changes to "Sold"
   - Book's sold_copies and available_copies update automatically

4. **Validation**:
   - Cannot confirm order if book has 0 available copies
   - Error message will display if trying to confirm unavailable book

### Website Usage

#### Browsing Books

1. **Access the Website**:
   - Navigate to your Odoo website (e.g., `http://localhost:8069`)
   - Click **"Books"** in the top navigation menu
   - Or visit directly: `http://your-domain/library/books`

2. **View Available Books**:
   - Only books with `is_available = True` are displayed
   - Each book shows:
     - Cover image (or placeholder)
     - Title
     - Author names
     - "View Details" button

#### Viewing Book Details

1. **Click on a book** from the catalog
2. **View complete information**:
   - Large cover image
   - Full title
   - Author badges
   - ISBN number
   - Publication date
   - Number of available copies
   - Book summary/description

#### Creating an Order

1. **On the book details page**, click **"Order This Book"**
2. **Modal popup appears**:
   - Enter your name in the "Customer Name" field
   - Click **"Create Order"**
3. **Success message** displays
4. **Order is created** in draft status in the backend

**Note**: Order button only appears if the book has available copies.

## 🔒 Security

### Security Groups

**Librarian Group** (`group_library_librarian`):
- Full access (Create, Read, Update, Delete) to all models
- Access to all menu items
- Located in: `security/library_security.xml`

### Access Rights

Defined in `security/ir.model.access.csv`:

| Model | Group | Create | Read | Write | Delete |
|-------|-------|--------|------|-------|--------|
| library.book | Librarian | ✅ | ✅ | ✅ | ✅ |
| library.author | Librarian | ✅ | ✅ | ✅ | ✅ |
| library.order | Librarian | ✅ | ✅ | ✅ | ✅ |

### Website Security

- All website pages use `auth='public'` for public access
- Backend operations use `sudo()` to bypass access rights for read-only operations
- Order creation is protected with CSRF tokens
- Only available books are displayed on the website



**Version**: 1.0  
**Odoo Version**: 17.0  
**Last Updated**: December 2024

Made with ❤️ for library management