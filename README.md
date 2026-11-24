# 🌍 CivicPulse – Smart Civic Complaint Management System

<p align="center">
  <strong>Where Every Complaint Creates Insight</strong>
</p>

CivicPulse is a web-based civic complaint management system designed to simplify the process of reporting, managing, and tracking civic issues. It provides separate dashboards for citizens and officers, along with an analytics dashboard that transforms complaint data into meaningful visual insights.

## 📌 About the Project

CivicPulse aims to create a more organized and transparent approach to civic complaint management. Citizens can report civic issues and track their complaints, while officers can manage complaints and update their status.

The system also integrates data analytics to visualize complaint patterns, identify frequently reported issues, and understand complaint distribution across different areas.

## ✨ Key Features

### 👤 Citizen Dashboard
- Citizen registration and login.
- Submit civic complaints.
- View submitted complaints.
- Track complaint status.
- Edit complaint details.
- Manage profile information.
- Access help section.

### 👮 Officer Dashboard
- Secure officer login.
- View and manage complaints.
- Access complaint details.
- Update complaint status.
- Manage officer profile.

### 📊 Analytics Dashboard
- Category-wise complaint analysis.
- Area-wise complaint analysis.
- Priority-wise complaint distribution.
- Complaint status visualization.
- Complaint resolution analysis.
- Complaint trend analysis.
- Civic issue heatmap.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Jinja2 | Dynamic HTML templating |
| HTML5 | Frontend structure |
| CSS3 | Styling |
| Bootstrap | Responsive design |
| JavaScript | Frontend interactions |
| Microsoft SQL Server | Database management |
| Pandas | Data processing |
| NumPy | Numerical computing |
| Matplotlib | Data visualization |

## 📈 Data Analytics & Visualization

CivicPulse uses Python-based data analytics to convert complaint records into visual representations.

The analytics dashboard includes:

- **Category Chart:** Displays complaints across different categories.
- **Location Chart:** Shows complaint distribution by area.
- **Priority Chart:** Visualizes complaint priority levels.
- **Status Chart:** Represents complaint statuses.
- **Trend Chart:** Shows complaint trends over time.
- **Resolution Chart:** Provides insights into complaint resolution.
- **Heatmap:** Visualizes the geographical distribution of civic issues.

## 📁 Project Structure

```text
CivicPulse/
│
├── analytics/
│   └── dashboard.py
│
├── static/
│   ├── charts/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── auth/
│   ├── citizen/
│   ├── officer/
│   └── index.html
│
├── app.py
├── config.py
├── requirements.txt
├── SQLQuery1.sql
├── SQLQuery2.sql
└── SQLQuery3.sql
```

## ⚙️ Installation & Setup

Follow these steps to run CivicPulse locally.

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/CivicPulse.git
```

**2. Navigate to the project directory**

```bash
cd CivicPulse
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate the virtual environment**

Windows:

```bash
venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

**6. Configure the database**

- Install and configure Microsoft SQL Server.
- Create the required database.
- Execute the provided SQL scripts.
- Configure database connection settings in `config.py`.

**7. Run the application**

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 🎯 Project Objectives

- Simplify civic complaint reporting.
- Improve complaint management and tracking.
- Provide an organized communication platform between citizens and officers.
- Use data analytics to understand civic issues.
- Support data-driven insights through visualizations.

## 🔮 Future Scope

- Email and SMS notifications.
- Advanced geographical analytics.
- Mobile application integration.
- Predictive analysis of civic complaints.

## 👩‍💻 Developed By

**Pratiksha Chaudhari**

TY BBA(CA) | Academic Project

---

⭐ If you find this project interesting, consider giving the repository a star!
