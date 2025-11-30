# 💈 Barber Shop – Appointment Booking System  
A full appointment scheduling system built with **Flask**, **MongoDB Atlas**, and **SendGrid**.  
Includes a **client booking page** + **admin dashboard** for managing appointments.

---

## 🚀 Features

### 👤 Client Side
- Book appointments easily through a clean UI
- Select available time slots dynamically
- Email confirmation on request submission
- Automatic email updates when approved/canceled

### 🛠 Admin Dashboard
- View all appointments
- Filter by date
- Approve / cancel / delete appointments
- Stats overview (today, week, pending, approved, canceled)
- Secure admin login

### 🌐 Tech Stack
- **Python + Flask**
- **MongoDB Atlas**
- **SendGrid Mailer**
- **HTML / CSS / JS**
- **Jinja2 Templates**

---

## 📦 Installation (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/maronhawa1/barbershop_en
cd barbershop_en
### 2️⃣ Create a virtual environment
#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set environment variables
Create a `.env` file in the project folder and put inside:

```env
MONGO_URI=your_mongo_atlas_connection
SENDGRID_API_KEY=your_sendgrid_key
ADMIN_EMAIL=your_verified_domain_email
ADMIN_USERNAME=admin
ADMIN_PASSWORD=adminpassword
```

### 5️⃣ Start the application
```bash
python main.py
```

Your app will be available at:

```
http://127.0.0.1:5000
```

---

## 🗂 Project Structure
```
barbershop_en/
│
├── static/                # CSS, images, JS
├── templates/             # HTML templates (client + admin)
│
├── main.py                # Flask server
├── mailer.py              # SendGrid email functions
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📧 Email Notifications (SendGrid)

### When a new appointment is made:
- Admin receives email  
- Client receives “pending approval” message  

### When the admin approves:
- Client receives confirmation

### When the admin cancels:
- Client receives cancellation message

---

## 🌐 Deployment Options
You can deploy this project using:

### ✔ Render (recommended)
- Connect your GitHub repo  
- Add environment variables  
- Set **Start Command**:
```bash
gunicorn main:app
```

### ✔ Railway
Same setup as Render.

### ✔ Ubuntu Server
- Clone repository  
- Setup venv  
- Install requirements  
- Run with Gunicorn + Nginx

---

## ⭐ Credits
Built by **Maron Hawa**.  
If you like this project — ⭐ star it on GitHub!
