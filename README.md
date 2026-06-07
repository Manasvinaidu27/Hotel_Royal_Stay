<div align="center">

# 🏨 Hotel Royal Stay

### *Premium Hotel Management System*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Razorpay](https://img.shields.io/badge/Razorpay-Integrated-02042B?style=for-the-badge&logo=razorpay&logoColor=white)](https://razorpay.com)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

<br/>

> A **production-grade** full-stack hotel management web application built with Django.
> Features luxury UI, AI-powered room recommendations, Razorpay payment integration,
> real-time analytics dashboard, and a complete booking management system.

<br/>

### 🌐 [View Live Demo](https://hotel-royal-stay.onrender.com) &nbsp;|&nbsp; 📖 [Documentation](#️-local-setup) &nbsp;|&nbsp; 🐛 [Report Bug](https://github.com/Harsha7215/Hotel-Royal-stay/issues)

<br/>

---

</div>

## 📌 Table of Contents

- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🗄️ Data Models](#️-data-models)
- [🔗 Routes](#-routes)
- [⚙️ Local Setup](#️-local-setup)
- [🌍 Deployment](#-deployment)
- [🎨 UI Design](#-ui-design)
- [📁 Project Structure](#-project-structure)
- [👨‍💻 Author](#-author)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🛏️ Room Management
- Browse rooms with real-time availability
- Filter by dates, guests, room type
- Room detail pages with amenities
- Status tracking (Available / Occupied / Maintenance)

### 📅 Smart Booking System
- Date conflict detection
- Guest count validation
- Special requests support
- Booking history and management

### 💳 Razorpay Payments
- UPI, Credit/Debit Cards, Net Banking
- Secure transaction handling
- Payment status tracking
- Refund management

</td>
<td width="50%">

### 📊 Admin Analytics Dashboard
- Revenue charts with Chart.js
- Occupancy rate tracking
- Booking trend analysis
- Guest statistics

### 🤖 AI Room Recommendations
- Rule-based recommendation engine
- Scoring by ratings and pricing
- Personalized suggestions
- Smart filtering

### 👥 Role-Based Access
- Admin / Staff / Customer roles
- JWT Authentication
- Secure login/logout
- Profile management

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Django 5.1 | Core web framework |
| **API** | Django REST Framework | RESTful API endpoints |
| **Auth** | SimpleJWT | JSON Web Token authentication |
| **Frontend** | Bootstrap 5 + Chart.js | Responsive UI and analytics |
| **Icons** | Font Awesome | UI icons |
| **Database** | SQLite (dev) / PostgreSQL (prod) | Data storage |
| **Payments** | Razorpay | Payment gateway |
| **Static Files** | WhiteNoise | Static file serving in production |
| **Server** | Gunicorn | WSGI HTTP server |
| **Deployment** | Render | Cloud hosting platform |

---

## 🗄️ Data Models

```
RoomType     →  Standard / Deluxe / Suite (pricing, capacity, amenities)
    └── Room         →  Individual rooms (floor, status, availability)
         └── Booking      →  Reservations (check-in/out, guests, price)
              └── Payment      →  Transactions (Razorpay, status, method)
Room
    └── RoomReview   →  Guest ratings (1-5 stars) and comments
UserProfile  →  Extended user (phone, address, ID proof)
```

---

## 🔗 Routes

### Web Routes
| Route | Description |
|---|---|
| `/` | Home page with stats |
| `/rooms/` | Room listing with search and filters |
| `/rooms/<id>/` | Room detail with reviews |
| `/rooms/<id>/book/` | Make a booking |
| `/recommendations/` | AI room picker |
| `/payment/<id>/` | Razorpay checkout |
| `/bookings/` | User booking history |
| `/dashboard/` | Admin analytics |

### REST API
| Endpoint | Method | Description |
|---|---|---|
| `/api/rooms/` | GET | List all rooms |
| `/api/bookings/` | GET/POST | Bookings CRUD |
| `/api/token/` | POST | Obtain JWT token |
| `/api/token/refresh/` | POST | Refresh JWT token |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Harsha7215/Hotel-Royal-stay.git
cd Hotel-Royal-stay
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations and Seed Data

```bash
python manage.py migrate
python seed_data.py
python manage.py createsuperuser
```

### 5. Start Development Server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

> 🔑 Admin panel: **http://127.0.0.1:8000/admin**

---

## 🌍 Deployment

This project is live on **Render** with PostgreSQL.

### Environment Variables

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` in production |
| `ALLOWED_HOSTS` | Your domain name |
| `CSRF_TRUSTED_ORIGINS` | `https://yourdomain.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection URL |
| `RAZORPAY_KEY_ID` | Razorpay API key |
| `RAZORPAY_KEY_SECRET` | Razorpay secret key |

### Build and Start Commands

```bash
# Build Command
pip install -r requirements.txt

# Start Command
sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn hotel_management.wsgi --log-file -"
```

---

## 🎨 UI Design

| Property | Value |
|---|---|
| **Theme** | Luxury dark-navy + gold accent |
| **Primary Font** | Cormorant Garamond (headings) |
| **Body Font** | DM Sans |
| **Layout** | Fully responsive Bootstrap 5 |
| **Charts** | Chart.js for analytics |
| **Icons** | Font Awesome 6 |

---

## 📁 Project Structure

```
Hotel-Royal-stay/
│
├── 📁 hotel/                    # Main application
│   ├── models.py                # RoomType, Room, Booking, Payment, Review
│   ├── views.py                 # All view logic
│   ├── urls.py                  # URL routing
│   └── forms.py                 # Django forms
│
├── 📁 accounts/                 # Authentication
│   ├── models.py                # UserProfile
│   ├── views.py                 # Login, register, profile
│   └── urls.py
│
├── 📁 hotel_management/         # Project config
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL config
│   └── wsgi.py
│
├── 📁 templates/                # HTML templates
│   ├── base.html                # Base layout
│   ├── hotel/                   # App templates
│   └── accounts/                # Auth templates
│
├── 📁 static/                   # Static assets
│   ├── css/style.css            # Custom styles
│   └── images/                  # Room images, logo
│
├── seed_data.py                 # Sample data seeder
├── manage.py
├── Procfile                     # Deployment config
├── runtime.txt                  # Python version
└── requirements.txt             # Dependencies
```

---

## 👨‍💻 Author

<div align="center">

**Harsha**

[![GitHub](https://img.shields.io/badge/GitHub-Harsha7215-181717?style=for-the-badge&logo=github)](https://github.com/Harsha7215)

*Built with ❤️ using Django*

---

⭐ **If you found this project helpful, please give it a star!** ⭐

</div>
