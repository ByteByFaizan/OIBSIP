# 🏥 Advanced BMI Calculator (Python GUI)

An **Advanced BMI Calculator** built using **Python**, **Tkinter**, **SQLite**, and **Matplotlib**.  
This application supports **multiple users**, stores BMI data persistently in a single shared database, and provides **historical analysis with graphical visualization**.

---

## 📌 Features

### ✅ Core Functionality
- Graphical User Interface (GUI) using Tkinter
- Accurate BMI calculation using standard formula
- Automatic BMI classification:
  - Underweight
  - Normal
  - Overweight
  - Obese
- Personalized health advice based on BMI category

### 🗃️ Data Storage
- Persistent **SQLite file-based database**
- Same database shared for **all users**
- Stores:
  - Name
  - Weight (kg)
  - Height (m)
  - BMI value
  - BMI category
  - Date & time of record

### 📜 History Management
- View BMI history of **all users**
- Delete selected BMI records
- Clear entire history with confirmation

### 📊 Data Visualization
- BMI trend graph for individual users
- Graph plotted using Matplotlib
- Reference lines for BMI categories
- Requires at least **2 records** to generate a trend

### 🛡️ Error Handling
- Input validation for name, weight, and height
- Graceful handling of database errors
- User-friendly warning and error dialogs

---

## 🧠 Technologies Used

| Technology | Description |
|----------|------------|
| Python | Core programming language |
| Tkinter | GUI framework |
| SQLite | File-based persistent storage |
| Matplotlib | Data visualization |
| datetime | Timestamp management |

---
