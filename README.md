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

- **Current Driver:** `pymysql`. 
  - **Why:** It is a pure-Python client, making it highly compatible with various Linux distributions (like Ubuntu, Alpine, or Amazon Linux) without requiring heavy C-compilers or system-level MariaDB/MySQL development headers.
  - **Installation:** Already included in your `uv` environment.
  
- **Performance Alternative:** `mysqlclient`.
  - **Why:** It is a C-extension wrapper. It is significantly faster and more memory-efficient than PyMySQL.
  - **Note:** If you switch to `mysqlclient`, ensure your production environment has the necessary binary dependencies (e.g., `libmysqlclient-dev` or `mysql-devel`).

### 📦 Switching Drivers with `uv`

If you decide to switch for better performance on your AWS instance:

```bash
# Remove PyMySQL
uv remove pymysql

# Add the high-performance C-wrapper
uv add mysqlclient
```

Note: When using PyMySQL, ensure you have the following in your manage.py or wsgi.py to allow Django to recognize it as the primary MySQL driver:

```bash
import pymysql
pymysql.install_as_MySQLdb()
```

© 2026 AgriSense Monitoring
