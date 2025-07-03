# 💸 Expense Tracker Web Application (Flask + MySQL + Matplotlib)

## 🔍 Overview

This is a **personal expense tracker web app** built using **Flask**, **MySQL**, and **Matplotlib**. It allows users to securely register, log in, and manage their daily expenses. The dashboard provides insights such as:

- ✅ Total Expenses  
- 📆 Monthly Spending  
- 📈 Average Daily Spend  
- 📊 Category-wise Expense Chart (generated using Matplotlib, no JavaScript)

---

## 🚀 Features

- 🔐 **User Authentication**
  - Registration and login with hashed passwords (`bcrypt`)

- 🧾 **Expense Management**
  - Add, edit, and delete expense records with categories, notes, and timestamps

- 📊 **Dashboard Insights**
  - Total and monthly expenses
  - Average daily spend
  - Category-wise bar chart (Matplotlib)

- 🖼️ **Graphical Reports**
  - Per-user chart image saved in `static/charts/`
  - Chart rendered server-side (no JS used)

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS (Bootstrap)  
- **Database:** MySQL  
- **Visualization:** Matplotlib  
- **Security:** bcrypt


 ## Setup MySQL Database via phpMyAdmin

1. Open your browser and go to:
   http://localhost/phpmyadmin

2. Create a new database:
   Database Name: user_db

3. Run the following SQL to create the registration table:

CREATE TABLE registration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255)
);

4. Run the following SQL to create the expenses table:

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100),
    amount DECIMAL(10,2),
    note TEXT,
    date DATETIME,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES registration(id) ON DELETE CASCADE
);
