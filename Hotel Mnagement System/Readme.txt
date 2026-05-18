# KHAAB GHAR - Assignment 4 (Interactive Frontend System)

**Course**: SE203-T Software Design and Architecture  
**Submitted by**: Group #25  
**Instructor**: Dr. Muhammad Asif  
**Submission Date**: April 29, 2025  

---

## 📌 Objective

This project implements a fully interactive and dynamic frontend system using 
"HTML, CSS (Bootstrap)**, and **JavaScript (DOM, LocalStorage)". 
It fulfills all core requirements of **Assignment 4**, including event handling, responsive UI, 
authentication, and more.

---

## 📁 Folder Structure

Group#25_Assignment#4/ │ ├── index.html ├── login.html ├── signup.html ├── dashboard_admin.html ├── 
dashboard_user.html ├── available_rooms.html ├── view_bookings.html ├── Manage_Rooms.html ├── 
chart_bookings.html ├── chart_availability.html ├── chart_daily_bookings.html └── logo.png


---

## Features Implemented

### 1. **Form Handling** (`signup.html`, `dashboard_admin.html`)
- Validations for empty fields and number-only inputs.
- Real-time feedback and inline error messages.
- Role dropdown auto-handled using JS.

### 2. **Dynamic Updates Without Reload** (`dashboard_admin.html`)
- Rooms are added dynamically and stored in LocalStorage.
- Data persists across refresh.
- Charts update based on bookings.

### 3. **Interactive Dashboards / Charts**
- Admin dashboard shows metrics (new bookings, check-ins).
- Pie charts using **Chart.js** (bookings, availability, daily trends).

### 4. **DOM Manipulation**
- Role-based dashboards.
- Sections toggle via JS (`toggleChart()`).
- Button text changes during loading.

### 5. **Storage & Persistence**
- LocalStorage is used as a mini database.
- Users and rooms stored persistently.
- Login state retained across sessions.

### 6. **Event Handling** 
- Clicks (e.g., Login, Signup, Add Room)
- Input/select changes (e.g., role dropdown)
- `Ctrl+S` keyboard shortcut to submit forms

### 7. **User Authentication**
- Users stored and verified via LocalStorage.
- Redirects based on role (Admin/User).
- Role selection during signup.

### 8. **Responsive UI Feedback**
- Inline success/error messages.
- Confirmation prompts (e.g., before adding room).
- Loading text during processing.

---

## 🧪 How to Test

1. **Open `index.html`**  
   Navigate to login or signup.

2. **Signup**  
   Create a new account with admin or user role.

3. **Login**  
   Use correct credentials and role to enter the dashboard.

4. **Try Admin Features**
   - Add rooms
   - Observe metrics
   - View alerts, confirmations

5. **Try Charts and View Pages**  
   Use the chart files to visualize booking data.

---

## 📦 Dependencies

- [Bootstrap 5](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)

These are loaded via CDN—no installation needed.

---

## ⚠ Notes
- Some of the required mentioned file's code were merged inside the already exisiting files , using the keyword <script>.
- No backend/database — all data is client-side.
- If needed, clear LocalStorage via browser console:
  ```js
  localStorage.clear();
