# 🛒 FastAPI E-Commerce Product Catalog API

A high-performance RESTful API for managing an e-commerce product catalog built with **FastAPI**, **Pydantic v2**, and **JSON file persistence**. This project demonstrates clean API architecture, robust data validation, business logic enforcement, dependency injection, and automatic OpenAPI documentation.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Project Architecture & Directory Structure](#-project-architecture--directory-structure)
- [Tech Stack & Dependencies](#-tech-stack--dependencies)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Environment Configuration](#environment-configuration)
  - [Running the Server](#running-the-server)
- [API Documentation & Endpoints](#-api-documentation--endpoints)
  - [Interactive Documentation](#interactive-documentation)
  - [Endpoints Summary](#endpoints-summary)
  - [Detailed Request & Response Examples](#detailed-request--response-examples)
- [Data Models & Validation Rules](#-data-models--validation-rules)
  - [Pydantic Schemas](#pydantic-schemas)
  - [Custom Validators & Business Rules](#custom-validators--business-rules)
  - [Computed Fields](#computed-fields)
- [Data Storage](#-data-storage)
- [Future Enhancements](#-future-enhancements)

---

## 🚀 Overview

The **FastAPI E-Commerce API** provides full CRUD (Create, Read, Update, Delete) capabilities for e-commerce products. It features:
- Case-insensitive search, multi-field filtering, price-based sorting, and pagination.
- Strict data typing and nested schema validations for sellers and physical dimensions.
- Domain-restricted email verification for sellers and structured SKU formatting.
- Automatically calculated properties such as discounted final price and package volume in cm³.

---

## ✨ Key Features

- **Full Product CRUD Operations**: Create, read (all or by ID), search, filter, update (partial/full), and delete products.
- **Advanced Query Parameters**:
  - `name`: Substring search by product name (case-insensitive).
  - `sort_by_price` & `order`: Sort ascending (`asc`) or descending (`desc`).
  - `limit` & `offset`: Configurable pagination with bounded item limits.
- **Pydantic v2 Validation**:
  - **SKU Format Validator**: Enforces a hyphen and trailing 3-digit number (e.g. `241-242-432`).
  - **Seller Domain Check**: Restricts seller emails to approved partner domains (`mistore.in`, `hpworld.in`).
  - **Business Rules Enforcement**:
    - An active product cannot have zero stock.
    - A discounted product cannot have zero rating.
- **Computed Fields**:
  - `final_price`: Dynamically calculates discounted price: `price * (1 - discount_percent / 100)`.
  - `volume_cm3`: Dynamically computes volume: `length * width * height`.
- **FastAPI Dependency Injection**:
  - Modular data loading via `Depends(load_products)`.
  - Reusable common logic on root endpoints with `Depends(common_logic)`.
- **JSON File-Based Persistence**:
  - Lightweight and portable JSON storage without external database setup.

---

## 📁 Project Architecture & Directory Structure

```text
FastAPI/
├── README.md                           # Project documentation (Root)
├── fastapi-ecommerce/
│   ├── README.md                       # Project documentation
│   └── app/
│       ├── .env                        # Environment variables
│       ├── requirements.txt            # Python dependencies
│       ├── main.py                     # FastAPI application, route handlers & dependencies
│       ├── data/
│       │   ├── dummy.json              # Active sample dataset
│       │   └── products.json           # Extended mock product catalog
│       ├── schema/
│       │   └── product.py              # Pydantic schemas (Product, ProductUpdate, Seller, Dimensions)
│       └── service/
│           └── products.py             # Data access layer (CRUD & file persistence)
└── venv/                               # Python virtual environment
```

---

## 🛠 Tech Stack & Dependencies

- **Language**: Python 3.10+ (Tested on 3.11 / 3.14)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/)
- **Email Validation**: `email-validator`
- **Unique Identifiers**: Python `uuid` (UUIDv4)
- **Environment Management**: `python-dotenv`

Dependencies defined in [`requirements.txt`](fastapi-ecommerce/app/requirements.txt):
```txt
fastapi
uvicorn
pydantic
sqlalchemy
UUID
email-validator
```

---

## ⚙️ Getting Started

### Prerequisites

Ensure you have Python 3.10 or later installed on your system. Verify with:
```bash
python --version
```

### Installation & Setup

1. **Clone or navigate to the repository directory**:
   ```bash
   cd "c:\Users\Rishabh Pandey\Desktop\FastAPI\fastapi-ecommerce\app"
   ```

2. **Create and activate a virtual environment** (if not already using the root `venv`):
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

The application reads configurations from `.env` in `fastapi-ecommerce/app/.env`:
```env
BASE_URL=app/data/products.json
```

### Running the Server

Navigate to the `app` folder and launch the Uvicorn ASGI server with hot-reload enabled:

```bash
cd "fastapi-ecommerce\app"
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Once running, access the application at:
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc UI**: `http://127.0.0.1:8000/redoc`

---

## 📖 API Documentation & Endpoints

### Interactive Documentation
FastAPI automatically generates interactive API documentation:
- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` to test endpoints directly from the browser.
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc` for an alternative, structured view.

### Endpoints Summary

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Root endpoint; returns status and dependency info | `200 OK` |
| `GET` | `/products` | List, search, sort, and paginate products | `200 OK` / `404 Not Found` |
| `GET` | `/products/{product_id}` | Retrieve a specific product by UUID | `200 OK` / `404 Not Found` |
| `POST` | `/products` | Create a new product (with UUID and UTC timestamp) | `201 Created` / `400 Bad Request` |
| `PUT` | `/products/{product_id}` | Update product details (partial / full) | `200 OK` / `404 Not Found` |
| `DELETE` | `/products/{product_id}` | Remove a product from the catalog | `200 OK` / `404 Not Found` |

---

### Detailed Request & Response Examples

#### 1. Root Endpoint
**Request**:
```http
GET / HTTP/1.1
Host: 127.0.0.1:8000
```
**Response (`200 OK`)**:
```json
{
  "message": "Hello World",
  "dependency": null,
  "data_path": "app/data/products.json"
}
```

---

#### 2. Get Products (Search, Sort & Pagination)
**Request**:
```http
GET /products?name=laptop&sort_by_price=true&order=asc&limit=10&offset=0 HTTP/1.1
Host: 127.0.0.1:8000
```
**Response (`200 OK`)**:
```json
{
  "total": 1,
  "items": [
    {
      "id": "1f9409af-21a1-4940-b41a-f7d322a1b3e7",
      "sku": "241-242-432",
      "name": "HP Laptop",
      "description": "A high-quality laptop with 16GB RAM and 512GB SSD.",
      "tags": ["electronics", "laptop", "gaming"],
      "rating": 4.5,
      "image_urls": [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
      ],
      "discount_percent": 10.0,
      "stock": 50,
      "is_active": true,
      "price": 999.99,
      "dimension_cm": {
        "length": 35.8,
        "width": 24.2,
        "height": 1.8
      },
      "seller": {
        "id": "5ff1519e-b952-4315-9151-c94b938123c9",
        "name": "HP Official",
        "email": "support@mistore.in",
        "website": "https://www.hp.com/"
      },
      "created_at": "2026-09-23T18:50:00Z",
      "final_price": 899.99,
      "volume_cm3": 1559.45
    }
  ]
}
```

---

#### 3. Create a New Product
**Request**:
```http
POST /products HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "sku": "PROD-A-101",
  "name": "Xiaomi Wireless Earbuds",
  "description": "Noise-cancelling wireless Bluetooth earbuds.",
  "tags": ["audio", "bluetooth", "accessories"],
  "rating": 4.2,
  "image_urls": ["https://mistore.in/images/earbuds.jpg"],
  "discount_percent": 15.0,
  "stock": 100,
  "is_active": true,
  "price": 49.99,
  "dimension_cm": {
    "length": 6.0,
    "width": 4.5,
    "height": 2.5
  },
  "seller": {
    "id": "c1f728ea-4993-4b47-b8d9-2e11894a4b12",
    "name": "Mi Store India",
    "email": "contact@mistore.in",
    "website": "https://mistore.in"
  },
  "created_at": "2026-10-27T10:00:00Z"
}
```
> **Note**: While `id` and `created_at` can be provided in the payload, the backend overrides them with an auto-generated UUIDv4 and the current UTC timestamp for consistency.

**Response (`201 Created`)**: Returns the created product payload with computed fields (`final_price: 42.49`, `volume_cm3: 67.5`).

---

#### 4. Update Product
**Request**:
```http
PUT /products/1f9409af-21a1-4940-b41a-f7d322a1b3e7 HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "price": 899.99,
  "stock": 40
}
```
**Response (`200 OK`)**: Returns the updated product record.

---

#### 5. Delete Product
**Request**:
```http
DELETE /products/1f9409af-21a1-4940-b41a-f7d322a1b3e7 HTTP/1.1
Host: 127.0.0.1:8000
```
**Response (`200 OK`)**:
```json
{
  "Message": "Product deleted successfully",
  "deleted_product": { ... }
}
```

---

## 🔒 Data Models & Validation Rules

### Pydantic Schemas

- **`Seller`**:
  - `id`: UUID
  - `name`: String between 2 and 60 characters
  - `email`: Valid `EmailStr` restricted to `@mistore.in` or `@hpworld.in`
  - `website`: Valid URL (`AnyUrl`)
- **`Dimensions`**:
  - `length`, `width`, `height`: Floats $\ge 0.0$ cm
- **`Product`**:
  - `id`: Unique UUID
  - `sku`: String (minimum length 6, must contain `-` and terminate with a 3-digit number)
  - `name`: String
  - `description`: Optional text
  - `tags`: Optional list of strings (maximum 10 tags)
  - `rating`: Optional float between `0.0` and `5.0`
  - `image_urls`: List of valid URLs
  - `discount_percent`: Float between `0.0` and `100.0`
  - `stock`: Integer $\ge 0$
  - `is_active`: Boolean status flag
  - `price`: Float $\ge 0.0$ USD
  - `dimension_cm`: Nested `Dimensions` model
  - `seller`: Nested `Seller` model
  - `created_at`: Datetime
- **`ProductUpdate`**:
  - All fields are optional to facilitate partial updates (`PATCH`/`PUT`).

### Custom Validators & Business Rules

1. **Email Domain Validator (`@field_validator`)**:
   ```python
   allowed_domains = ["mistore.in", "hpworld.in"]
   ```
   Ensures that only authorized partners can sell products.

2. **SKU Structure Validator (`@field_validator`)**:
   - Must contain a hyphen `-`.
   - The characters following the last hyphen must be exactly 3 numeric digits (e.g., `ABC-123`).

3. **Cross-Field Model Validation (`@model_validator(mode="after")`)**:
   - **Zero Stock for Active Products**: Raises an error if `is_active == True` and `stock == 0`.
   - **Zero Rating on Discount**: Raises an error if `discount_percent > 0` and `rating == 0`.

### Computed Fields

- **`final_price`**:
  $$\text{final\_price} = \text{round}\left(\text{price} \times \left(1 - \frac{\text{discount\_percent}}{100}\right), 2\right)$$
- **`volume_cm3`**:
  $$\text{volume\_cm3} = \text{round}(\text{length} \times \text{width} \times \text{height}, 2)$$

---

## 💾 Data Storage

The service layer (`app/service/products.py`) reads and writes to JSON files using standard Python file I/O with UTF-8 encoding:
- `dummy.json`: Lightweight mock file for testing and development.
- `products.json`: Production-sized mock dataset containing a rich collection of electronics and catalog items.

To switch datasets, update `DATA_FILE` in [`app/service/products.py`](fastapi-ecommerce/app/service/products.py):
```python
# To use the full catalog:
DATA_FILE = Path(__file__).parent.parent / "data" / "products.json"

# To use dummy test data:
DATA_FILE = Path(__file__).parent.parent / "data" / "dummy.json"
```

---

## 🔮 Future Enhancements

- [ ] Transition from JSON file storage to a relational database using **SQLAlchemy** with PostgreSQL / SQLite.
- [ ] Add JWT-based user authentication and role-based access control (Admin vs. Seller vs. Buyer).
- [ ] Implement database migrations using **Alembic**.
- [ ] Add unit and integration tests using **pytest** and `httpx.AsyncClient`.
- [ ] Containerize the application with **Docker** and `docker-compose`.

---

## 📄 License

This project is licensed under the MIT License - feel free to use and adapt it for learning or production.
