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
