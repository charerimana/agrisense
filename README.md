# 🌾 AgriSense: Smart Farm Monitoring System

AgriSense is a real-time agricultural IoT dashboard designed to help farm owners in Rwanda monitor environmental conditions. It features a robust **Django** backend, **AJAX-driven** CRUD operations, and dynamic data visualization using **Chart.js**.

## 🚀 Features

- **Dynamic Dashboard**: 
    - Real-time **Line Charts** for temperature trends.
    - **Data Volume Pie Charts** to compare sensor activity.
    - **Farm Health Doughnut Charts** showing "In-Range" vs "Alert" status.
- **Seamless CRUD**: Manage Farms and Sensors via **Bootstrap Modals** and **AJAX** (no page refreshes).
- **Smart Filtering**: Multi-farm selector and search functionality for specific locations or names.
- **Automated Alerts**: Integrated **Email (SMTP)** and **SMS (Twilio)** notifications for threshold breaches.
- **Secure Architecture**: Strict data isolation—users only see their own farms and sensor data.

## 🛠️ Tech Stack

- **Framework**: [Django 5.x](https://www.djangoproject.com)
- **Package Manager**: [uv](https://github.com) (Fast Python package installer)
- **Database**: 
    - **Development**: SQLite
    - **Production**: AWS RDS (MySQL)
- **Frontend**: Bootstrap 5, jQuery, Chart.js
- **Communications**: [Twilio API](https://www.twilio.com) (SMS), SendGrid/Gmail (Email)

## 📊 Data Models

- **Farm**: Tracks name and location (Supports all 30 Rwandan Districts).
- **Sensor**: `OneToOne` with Farm. Stores `min_temp` and `max_temp` thresholds.
- **SensorReading**: Stores temperature values and timestamps (`recorded_at`).
- **NotificationPreference**: User-specific toggles for SMS/Email alerts and phone numbers.
- **Notification**: History of all alerts sent to users.

## ⚡ Quick Start (Manual Download)

If you have [uv](https://astral.sh) installed, run this to get started in seconds:

1. **Download & Extract** the ZIP from GitHub.
2. **Open Terminal** in the project folder.
3. **Run Setup:**
   ```bash
   uv sync && uv run manage.py migrate && uv run manage.py runserver
   ```

## 📦 Installation & Setup

This project uses `uv` for ultra-fast dependency management.

### 1. Clone & Sync
```bash
git clone <repository-url>
cd agrisense
uv sync
```

### 2. Environment Configuration
Create a `.env` file in the root directory:

```bash
DEBUG=True
SECRET_KEY=your-secret-key

# Email Config (Mailpit for Local Testing)
EMAIL_HOST=localhost
EMAIL_PORT=1025

# For GMAIL
EMAIL_HOST_PASSWORD=your_gmail_app_password
EMAIL_PORT=587

# Twilio Config (SMS)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_twilio_number

# Production DB (AWS RDS MySQL)
DB_NAME=agrisense_db
DB_USER=admin
DB_PASSWORD=your_rds_password
DB_HOST=your-rds-endpoint.aws.com
DB_PORT=3306
```

### 3. Database Migration
```bash
uv run manage.py migrate
uv run manage.py createsuperuser
```

### 4. Run Development Server
```bash
uv run manage.py runserver
```

## 🗄️ Database & Production Drivers

This project is configured to use **MySQL** on **AWS RDS** for production. To ensure your environment can communicate with the database, follow these dependency guidelines:
  
- **Current Driver:** `mysqlclient`.
  - **Why:** It is a C-extension wrapper. It is significantly faster and more memory-efficient than PyMySQL.
  - **Note:** If you switch to `mysqlclient`, ensure your production environment has the necessary binary dependencies (e.g., `libmysqlclient-dev` or `mysql-devel`).

## 🔐 Authentication & Security
This project implements a dual-layer authentication system to balance user experience with machine-to-machine security.
### 1. Session Authentication (Web Dashboard)
The web interface uses standard Django Session Authentication.
Login: Users must authenticate via the Bootstrap-styled login page.
Protection: All dashboard forms are protected against CSRF (Cross-Site Request Forgery) using the `{% csrf_token %}` middleware.

### 2. JWT Authentication (Sensor API)
For the sensors/IoT devices, we use JSON Web Tokens (JWT) via the SimpleJWT library. This is ideal for stateless, secure communication.

Header: `Authorization: Bearer <your_access_token>`

Endpoints:
- **POST** `/api/token/`: Obtain a new token pair (Access & Refresh).
- **POST** `/api/token/refresh/`: Renew an expired access token using the refresh token.

### 3. Permissions
We use a custom permission class IsOwnerOrSuperUser.
- **Sensors**: Can only post data to IDs they are registered to.
- **Users**: Can only view dashboard data for the farms they own.

© 2026 AgriSense Monitoring
