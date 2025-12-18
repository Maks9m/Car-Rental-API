# Car Rental API 🚗

## 📋 Project Description

Car Rental API is a backend platform designed to automate car rental processes. The system allows users to register, browse available cars, book them for specific dates, and enables administrators to track user activity and financial performance.

**Domain:** Car Rental Service.
**Type:** Database Course Project.

---

## 👥 Team
**@Maks9m**
**@edw4rdkk**

---

## 🛠 Technology Stack

- **Language:** Python 3.13
- **Framework:** FastAPI
- **Database:** PostgreSQL (Production), SQLite (Testing)
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Validation:** Pydantic v2
- **Testing:** Pytest
- **Authentication:** JWT (OAuth2 Password Bearer)
- **Containerization:** Docker & Docker Compose

---

## 🚀 Features

### Key Capabilities:
- **Authentication:** Registration, login, JWT token issuance.
- **Users:** Profile management, adding driver's license details.
- **Bookings:** - Create bookings with availability checks for selected dates.
  - Cancel and modify booking dates.
  - Status validation (e.g., closed bookings cannot be modified).
- **Analytics:** User ranking system based on trip count and total spending.

### 📊 Database Schema

The system consists of the following main entities:
- **User**: System users.
- **DriverLicense**: Driver's license data (1-to-1 relationship with User).
- **Car**: Vehicles (linked to Model and Location).
- **Booking**: Car reservations (main transactional table).
- **Trip**: Actual trip record (created based on a Booking).
- **Payment**: Payment transactions.

A detailed description of the schema can be found in [docs/schema.md](docs/schema.md).

---

## ⚙️ Setup & Execution

### Local Setup (without Docker)

1. **Clone the repository:**

```zsh
git clone https://github.com/Maks9m/Car-Rental-API
cd car-rental-api
```

2. **Create a virtual environment:**

A virtual environment isolates the project's dependencies from your global Python installation, ensuring consistency and preventing conflicts.

```zsh
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```zsh
pip install -r requirements.txt
```

4. Environment Variables: Create an **.env** file based on the example and configure your DB credentials.

5. **Run Migrations:**

```zsh
alembic upgrade head
```

6. **Seed DB**

```zsh
python ./seed.py
```

7. **Run Dev**

```zsh
python -m fastapi dev src/main.py
```

### Docker setup

```zsh
docker-compose up --build
```

---

## 🧪 Running Tests

Automated Testing

Run all tests using Pytest (uses SQLite by default):
```zsh
pytest -v
```

Test Database Setup

* The test suite uses a separate SQLite database for isolation.
* Fixtures for test data are located in test/conftest.py.

---

## 📁 Project Structure
```
Car_Rental_API/
├── alembic/                      # Database migrations (Alembic)
│   ├── versions/                 # Individual migration scripts
│   │   ├── 7e7ed367cffc_create_initial_tables.py
│   │   ├── fc414d616f5f_add_password_hash_column_to_user.py
│   │   ├── 7376dd384a23_rename_book_id_to_booking_id.py
│   │   ├── f9fd9c24f4bd_remove_unneeded_indexes.py
│   │   └── a389956bf545_added_date_columns_to_bookings.py
│   ├── env.py                    # Alembic environment configuration
│   └── README
├── docs/
│   ├──schema.md                  # Detailed database schema
│   └──queries.md                 # SQL queries explained
├── src/                          # Main application source code
│   ├── auth/                     # Authentication module
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Auth dependencies (get_current_user)
│   │   ├── exceptions.py
│   │   ├── router.py             # Auth routes (login)
│   │   ├── schema.py
│   │   ├── service.py            # Auth logic
│   │   └── utils.py              # Password hashing utilities
│   ├── bookings/                 # Bookings module
│   │   └── ...
│   ├── cars/                     # Cars module
│   │   └── ...
│   ├── driver_licenses/          # Driver licenses module
│   │   └── ...
│   ├── payments/                 # Payments module
│   │   └── ...
│   ├── trips/                    # Trips module
│   │   └── ...
│   ├── users/                    # Users module
│   │   └── ...                   # User business logic
│   ├── config.py                 # Configuration (env vars)
│   ├── database.py               # Database connection setup
│   ├── exceptions.py             # Global exceptions
│   ├── logger.py                 # Logging configuration
│   ├── main.py                   # App entry point (FastAPI app)
│   └── models.py                 # SQLAlchemy DB models
├── test/                         # Tests
│   ├── conftest.py               # Pytest fixtures
│   ├── test_auth.py
│   ├── test_bookings.py
│   └── test_users.py
├── .env                          # Environment variables
├── .gitignore
├── alembic.ini                   # Alembic config file
├── docker-compose.yml            # Docker configuration
├── pytest.ini                    # Pytest configuration
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── seed.py                       # Script to populate initial data
```

---

## 📑 API Endpoints

### Authentication (`/token`)

| Method | Endpoint   | Description      | Auth |
|--------|------------|------------------|------|
| POST   | `/token`   | Login (get JWT)  | ❌   |

### Users (`/users`)

| Method | Endpoint        | Description              | Auth |
|--------|----------------|--------------------------|------|
| GET    | `/`            | Get all users profiles   | ❌   |
| POST   | `/register`    | Register new user        | ❌   |
| GET    | `/me`          | Get current user profile | ✅   |
| PATCH  | `/me/update`   | Update current user info | ✅   |
| GET    | `/ranking`     | Get user ranking         | ❌   |
| GET    | `/{user_id}`   | Get user by ID           | ❌   |

### Cars (`/cars`)

| Method | Endpoint             | Description                | Auth |
|--------|----------------------|----------------------------|------|
| GET    | `/available-cars`    | List available cars        | ❌   |
| DELETE | `/cars/{car_id}`     | Delete car (admin)         | ✅   |
| PATCH  | `/models/{model_id}` | Update car model price     | ✅   |

### Bookings (`/bookings`)

| Method | Endpoint                  | Description                | Auth |
|--------|---------------------------|----------------------------|------|
| GET    | `/`                       | List all bookings (admin)  | ✅   |
| GET    | `/me`                     | List my bookings           | ✅   |
| POST   | `/create`                 | Create booking             | ✅   |
| PATCH  | `/{booking_id}/dates`     | Update booking dates       | ✅   |
| PATCH  | `/{booking_id}/cancel`    | Cancel booking             | ✅   |

### Trips (`/trips`)

| Method | Endpoint            | Description                    | Auth |
|--------|---------------------|--------------------------------|------|
| POST   | `/{trip_id}/finish` | Finish trip and create payment | ✅   |

### Driver Licenses (`/driver-licenses`)

| Method | Endpoint | Description                | Auth |
|--------|----------|----------------------------|------|
| GET    | `/me`    | Get my driver license info | ✅   |

---

## 💡 Usage Examples

### Register New User

```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "firstname": "John",
    "lastname": "Doe",
    "driver_license": {
      "license_number": "DL123456",
      "license_type": "B",
      "expiry_date": "2026-12-31"
    }
  }'
```

### Book a Car

```bash
curl -X POST http://localhost:8000/bookings/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "car_id": 1,
    "start_date": "2025-01-10",
    "end_date": "2025-01-15"
  }'
```

---

## 🔍 Complex SQL Queries

The system includes analytical queries for:

1. **User ranking by bookings and spending** (window functions)
2. **Car usage analytics**
3. **Revenue by period**
4. **Top users by completed trips**

**Detailed documentation:** [`docs/queries.md`](docs/queries.md)

---

## 🚧 Troubleshooting

### Database Connection Error

- Make sure PostgreSQL is running (`docker compose ps`)
- Check `DATABASE_URL` in `.env`

### Tests Failing

- Ensure test database is configured and migrations are applied
- Clean and re-seed the test database if needed

---

**Last Updated:** December 18, 2025
