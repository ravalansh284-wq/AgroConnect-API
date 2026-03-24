# 🌱 AgroConnect API

An enterprise-grade RESTful API built with FastAPI that acts as a digital bridge between Farmers and Distributors for seamless agricultural trading and inventory management.

## ✨ Key Features & Architecture

* **Role-Based Access Control (RBAC):** Secure architecture ensuring users are properly authorized (e.g., only Farmers can create products, only Distributors can place orders).
* **Automated Audit Trails:** Custom-built Middleware intercepts requests, validates JWT tokens, and automatically stamps every database transaction with `created_by` and `updated_at` tags.
* **Graceful Caching:** Integrated Redis caching for high-performance product retrieval, engineered with a failsafe to gracefully fall back to PostgreSQL if the cache server is unreachable.
* **Modern Security:** JWT-based stateless authentication with bcrypt password hashing and fully configured CORS middleware.

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy & Pydantic
* **Caching:** Redis (Upstash)
* **Authentication:** OAuth2 with JWT (JSON Web Tokens)

## 🚀 How to Run Locally

### 1. Set up the virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
