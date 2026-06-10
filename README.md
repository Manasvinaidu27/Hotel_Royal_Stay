
# 🏨 Hotel Royal Stay

A production-ready hotel management system built with Django, featuring AI-powered room recommendations, Razorpay payment integration, and a real-time analytics dashboard.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Django](https://img.shields.io/badge/Django-5.1-green) ![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

🌐 **Live Demo:** [hotel-royal-stay.onrender.com](https://hotel-royal-stay-blpo.onrender.com)

---

## 📌 Overview

Hotel Royal Stay is a full-stack web application that enables guests to browse rooms, make bookings, and pay securely — while providing hotel administrators with a comprehensive dashboard for revenue tracking, occupancy monitoring, and guest analytics.

The system includes an AI-powered room recommendation engine that ranks rooms based on guest ratings and pricing to deliver personalized suggestions.

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Bootstrap 5, Chart.js, Font Awesome |
| Backend | Python, Django 5.1, Django REST Framework |
| Authentication | Django Auth + SimpleJWT |
| Database | SQLite (development) / PostgreSQL (production) |
| Payments | Razorpay (UPI, Cards, Net Banking) |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Deployment | Render |

---

## 🎯 Features

### 🛏️ Room Management
- Browse rooms with real-time availability search
- Filter by dates, guest count, and room type
- Room detail pages with amenities, capacity, and reviews
- Status tracking: Available / Occupied / Maintenance

### 📅 Smart Booking System
- Date conflict detection and validation
- Guest count enforcement per room capacity
- Special requests support
- Full booking history and management

### 💳 Payment Integration
- Razorpay support for UPI, Credit/Debit Cards, and Net Banking
- Secure transaction handling with payment status tracking
- Automatic booking confirmation on payment success

### 📊 Admin Analytics Dashboard
- Revenue trend charts powered by Chart.js
- Occupancy rate and booking analytics
- Guest statistics overview

### 🤖 AI Room Recommendation Engine

| Feature | Logic | Purpose |
|---------|-------|---------|
| Rating Score | Average guest rating | Prefer highly rated rooms |
| Price Score | Value-for-money index | Balance cost and quality |
| Availability Check | Real-time date filtering | Show only bookable rooms |
| Combined Ranking | Weighted scoring | Personalized suggestions |

### 👥 Role-Based Access Control
- Admin / Staff / Customer roles
- JWT Authentication for REST API
- Django session auth for the web interface

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/rooms/` | List all rooms |
| GET | `/api/rooms/<id>/` | Room detail |
| GET/POST | `/api/bookings/` | Bookings CRUD |
| POST | `/api/token/` | Obtain JWT token |
| POST | `/api/token/refresh/` | Refresh JWT token |

---

## 🗂️ Project Structure

```
Hotel-Royal-stay/
├── hotel/
├── accounts/
├── hotel_management/
├── templates/
├── static/
├── seed_data.py
├── manage.py
├── Procfile
├── runtime.txt
└── requirements.txt
```

---

## ▶️ Getting Started

### Prerequisites
- Python 3.11+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Manasvinaidu27/Hotel-Royal-stay.git
cd Hotel-Royal-stay

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and seed data
python manage.py migrate
python seed_data.py
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Access the app at `http://127.0.0.1:8000`
Admin panel at `http://127.0.0.1:8000/admin`

---

## 🌍 Deployment

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` in production |
| `ALLOWED_HOSTS` | Your domain name |
| `DATABASE_URL` | PostgreSQL connection URL |
| `RAZORPAY_KEY_ID` | Razorpay API key |
| `RAZORPAY_KEY_SECRET` | Razorpay secret key |

### Build & Start Commands

```bash
# Build
pip install -r requirements.txt

# Start
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn hotel_management.wsgi
```

---

## ⚠️ Known Limitations

- Media uploads are not persistent on free-tier hosting
- Razorpay is currently in test mode
- Free tier on Render auto-sleeps after inactivity

---

## 🚀 Planned Enhancements

- [ ] AWS S3 / Cloudinary for persistent media storage
- [ ] Redis caching and Celery async tasks
- [ ] OAuth social login
- [ ] WebSocket real-time updates
- [ ] Stripe payment support
- [ ] React Native mobile app
- [ ] AI-based dynamic pricing

---

## 🤝 Contributing

Contributions are welcome! Please open an issue before submitting a pull request.

---

## 👨‍💻 Author

**Manasvi Naidu** — [GitHub](https://github.com/Manasvinaidu27)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
