
from flask import Flask, render_template , request , redirect, session , flash , url_for
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "civicpulse-secret-key-change-later"
OFFICER_CODE = "CIVICPULSE-OFFICER-2026"
PUNE_AREAS = [
    "Kothrud",
    "Baner",
    "Aundh",
    "Wakad",
    "Hadapsar",
    "Viman Nagar",
    "Kharadi",
    "Shivajinagar",
    "Deccan",
    "Swargate",
    "Kondhwa",
    "Pashan",
    "Warje",
    "Bibwewadi",
    "Yerawada",
    "Sinhagad Road",
    "Camp",
    "Katraj",
    "Bavdhan",
    "Dhayari"
]

# ================= DATABASE CONNECTION =================

def get_db_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=CivicPulseDB;"
        "Trusted_Connection=yes;"
    )
    return connection


# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("auth/register.html")

    fullname = request.form.get("fullname", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    city = request.form.get("city", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    role = request.form.get("role", "")
    officer_code = request.form.get("officer_code", "").strip()
    terms = request.form.get("terms")

    # ---------- VALIDATION ----------

    if not fullname or len(fullname) < 3 or len(fullname) > 100:
        return render_template(
            "auth/register.html",
            error="Full name must be between 3 and 100 characters."
        )

    if not email or "@" not in email:
        return render_template(
            "auth/register.html",
            error="Please enter a valid email address."
        )

    if not phone.isdigit() or len(phone) != 10:
        return render_template(
            "auth/register.html",
            error="Phone number must contain exactly 10 digits."
        )

    if not city:
        return render_template(
            "auth/register.html",
            error="City is required."
        )

    if len(password) < 8:
        return render_template(
            "auth/register.html",
            error="Password must contain at least 8 characters."
        )

    if password != confirm_password:
        return render_template(
            "auth/register.html",
            error="Passwords do not match."
        )

    if role not in ["Citizen", "Officer"]:
        return render_template(
            "auth/register.html",
            error="Please select a valid role."
        )
    if role == "Officer":
        if officer_code != OFFICER_CODE:
            return render_template(
                "auth/register.html",
                error="Invalid officer authorization code."
            )

    if not terms:
        return render_template(
            "auth/register.html",
            error="You must accept the terms and conditions."
        )

    # ---------- DATABASE ----------

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT UserID FROM Users WHERE Email = ?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()

        return render_template(
            "auth/register.html",
            error="An account with this email already exists."
        )

    # Hash password
    hashed_password = generate_password_hash(password)

    # Insert user
    cursor.execute(
        """
        INSERT INTO Users
        (FullName, Email, Phone, City, Password, Role)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            fullname,
            email,
            phone,
            city,
            hashed_password,
            role
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/login")


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])   
def login():

    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email:
        return render_template(
            "auth/login.html",
            error="Email is required."
        )

    if not password:
        return render_template(
            "auth/login.html",
            error="Password is required."
        )

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT UserID, FullName, Password, Role
        FROM Users
        WHERE Email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user is None:
        return render_template(
            "auth/login.html",
            error="Invalid email or password."
        )

    user_id = user[0]
    full_name = user[1]
    hashed_password = user[2]
    role = user[3]

    if not check_password_hash(hashed_password, password):
        return render_template(
            "auth/login.html",
            error="Invalid email or password."
        )

    session["user_id"] = user_id
    session["full_name"] = full_name
    session["role"] = role

    if role == "Citizen":
        return redirect("/citizen/dashboard")

    if role == "Officer":
        return redirect("/officer/dashboard")
    


    return render_template(
        "auth/login.html",
        error="Invalid user role."
    )

@app.route("/officer/dashboard")
def officer_dashboard():
    """Officer analytics dashboard with database-driven Smart Insights."""
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Officer":
        return redirect("/login")

    os.makedirs("static/charts", exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # KPI cards
        cursor.execute("SELECT COUNT(*) FROM Complaints")
        total = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(*) FROM Complaints WHERE Status = 'Pending'")
        pending = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(*) FROM Complaints WHERE Status = 'In Progress'")
        in_progress = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(*) FROM Complaints WHERE Status = 'Resolved'")
        resolved = cursor.fetchone()[0] or 0

        # Category distribution
        cursor.execute("""
            SELECT cat.CategoryName, COUNT(*) AS Total
            FROM Complaints c
            JOIN Categories cat ON c.CategoryID = cat.CategoryID
            GROUP BY cat.CategoryName
            ORDER BY COUNT(*) DESC
        """)
        category_data = cursor.fetchall()

        # Status distribution
        cursor.execute("""
            SELECT Status, COUNT(*) AS Total
            FROM Complaints
            GROUP BY Status
            ORDER BY COUNT(*) DESC
        """)
        status_data = cursor.fetchall()

        # Priority distribution
        cursor.execute("""
            SELECT Priority, COUNT(*) AS Total
            FROM Complaints
            GROUP BY Priority
            ORDER BY COUNT(*) DESC
        """)
        priority_data = cursor.fetchall()

        # Daily complaint trend
        cursor.execute("""
            SELECT CAST(CreatedAt AS DATE) AS ComplaintDate, COUNT(*) AS Total
            FROM Complaints
            WHERE CreatedAt IS NOT NULL
            GROUP BY CAST(CreatedAt AS DATE)
            ORDER BY ComplaintDate
        """)
        trend_data = cursor.fetchall()

        # Area extracted from the beginning of "Area - specific location"
        cursor.execute("""
            SELECT LTRIM(RTRIM(LEFT(Location, CHARINDEX(' - ', Location + ' - ') - 1))) AS Area,
                   COUNT(*) AS Total
            FROM Complaints
            GROUP BY LTRIM(RTRIM(LEFT(Location, CHARINDEX(' - ', Location + ' - ') - 1)))
            ORDER BY COUNT(*) DESC
        """)
        area_data = cursor.fetchall()

        # Resolved complaint counts by resolution date
        cursor.execute("""
            SELECT CAST(ResolvedAt AS DATE) AS ResolvedDate, COUNT(*) AS Total
            FROM Complaints
            WHERE Status = 'Resolved' AND ResolvedAt IS NOT NULL
            GROUP BY CAST(ResolvedAt AS DATE)
            ORDER BY ResolvedDate
        """)
        resolution_data = cursor.fetchall()

        # High-priority complaints still awaiting resolution
        cursor.execute("""
            SELECT COUNT(*) FROM Complaints
            WHERE Priority = 'High' AND Status IN ('Pending', 'In Progress')
        """)
        high_priority_open = cursor.fetchone()[0] or 0

        # Last seven calendar days compared with the preceding seven days
        cursor.execute("""
            SELECT
                SUM(CASE WHEN CreatedAt >= DATEADD(DAY, -6, CAST(GETDATE() AS DATE))
                          AND CreatedAt < DATEADD(DAY, 1, CAST(GETDATE() AS DATE)) THEN 1 ELSE 0 END) AS Recent7,
                SUM(CASE WHEN CreatedAt >= DATEADD(DAY, -13, CAST(GETDATE() AS DATE))
                          AND CreatedAt < DATEADD(DAY, -6, CAST(GETDATE() AS DATE)) THEN 1 ELSE 0 END) AS Previous7
            FROM Complaints
            WHERE CreatedAt IS NOT NULL
        """)
        trend_comparison = cursor.fetchone()
        recent_7 = int(trend_comparison[0] or 0)
        previous_7 = int(trend_comparison[1] or 0)

        # Average resolution time, only where a valid resolution timestamp exists
        cursor.execute("""
            SELECT AVG(CAST(DATEDIFF(HOUR, CreatedAt, ResolvedAt) AS FLOAT))
            FROM Complaints
            WHERE Status = 'Resolved' AND CreatedAt IS NOT NULL
              AND ResolvedAt IS NOT NULL AND ResolvedAt >= CreatedAt
        """)
        avg_resolution_hours = cursor.fetchone()[0]
        avg_resolution_hours = round(float(avg_resolution_hours), 1) if avg_resolution_hours is not None else None

        # Recent complaints
        cursor.execute("""
            SELECT TOP 5 c.ComplaintID, u.FullName, cat.CategoryName,
                   c.Location, c.Priority, c.Status, c.CreatedAt
            FROM Complaints c
            JOIN Users u ON c.UserID = u.UserID
            JOIN Categories cat ON c.CategoryID = cat.CategoryID
            ORDER BY c.CreatedAt DESC
        """)
        recent_complaints = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    # Prepare dataframes for Matplotlib charts
    df_category = pd.DataFrame([list(r) for r in category_data], columns=["Category", "Total"])
    df_status = pd.DataFrame([list(r) for r in status_data], columns=["Status", "Total"])
    df_priority = pd.DataFrame([list(r) for r in priority_data], columns=["Priority", "Total"])
    df_trend = pd.DataFrame([list(r) for r in trend_data], columns=["Date", "Total"])
    df_area = pd.DataFrame([list(r) for r in area_data[:8]], columns=["Area", "Total"])
    df_resolution = pd.DataFrame([list(r) for r in resolution_data], columns=["Date", "Total"])

    # Consistent CivicPulse navy / steel-blue / teal chart theme.
    import matplotlib.dates as mdates

    chart_dir = "static/charts"
    os.makedirs(chart_dir, exist_ok=True)

    NAVY = "#172B4D"
    BLUE = "#4169A1"
    BLUE_LIGHT = "#8FAED8"
    TEAL = "#2A9D9F"
    AMBER = "#E9A23B"
    RED = "#D96C6C"
    PURPLE = "#8273B8"
    GRID = "#E7EDF5"
    MUTED = "#718096"
    STATUS_COLORS = {
        "Pending": AMBER,
        "In Progress": PURPLE,
        "Resolved": TEAL
    }
    PRIORITY_COLORS = {
        "High": RED,
        "Medium": AMBER,
        "Low": TEAL
    }

    def style_axis(ax):
        ax.set_facecolor("#FFFFFF")
        ax.tick_params(axis="both", labelsize=8, colors=MUTED, length=0)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)

    def save_chart(fig, filename):
        fig.patch.set_facecolor("#FFFFFF")
        fig.tight_layout(pad=1.5)
        fig.savefig(os.path.join(chart_dir, filename), dpi=180,
                    bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close(fig)

    def empty_chart(ax, message):
        ax.text(0.5, 0.5, message, ha="center", va="center",
                transform=ax.transAxes, color=MUTED, fontsize=10)
        ax.set_axis_off()

    # 1. Category-wise complaints — horizontal bars suit longer category names.
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    if not df_category.empty:
        chart_df = df_category.sort_values("Total", ascending=True)
        bars = ax.barh(chart_df["Category"], chart_df["Total"],
                       color=BLUE, height=0.58)
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
        ax.set_xlabel("Complaints", fontsize=8, color=MUTED, labelpad=6)
        ax.tick_params(axis="y", labelsize=8, colors=MUTED, length=0)
        ax.tick_params(axis="x", labelsize=8, colors=MUTED, length=0)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.bar_label(bars, padding=4, fontsize=8, color=NAVY)
        ax.set_xlim(0, max(chart_df["Total"].max() * 1.18, 1))
    else:
        empty_chart(ax, "No complaint data yet")
    
    save_chart(fig, "category_chart.png")

    # 2. Complaint status — clean donut chart.
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    if not df_status.empty and int(df_status["Total"].sum()) > 0:
        colors = [STATUS_COLORS.get(str(value), BLUE_LIGHT)
                  for value in df_status["Status"]]
        wedges, _, _ = ax.pie(
            df_status["Total"], startangle=90, counterclock=False,
            colors=colors, autopct="%1.0f%%", pctdistance=0.78,
            textprops={"fontsize": 8, "color": NAVY},
            wedgeprops={"width": 0.36, "edgecolor": "white", "linewidth": 2}
        )
        ax.legend(wedges, df_status["Status"], loc="lower center",
                  bbox_to_anchor=(0.5, -0.08), ncol=min(3, len(wedges)),
                  frameon=False, fontsize=8, labelcolor=MUTED)
    else:
        empty_chart(ax, "No complaint data yet")
    
    save_chart(fig, "status_chart.png")

    # 3. Area-wise complaints — horizontal bars keep area names readable.
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    if not df_area.empty:
        chart_df = df_area.sort_values("Total", ascending=True)
        bars = ax.barh(chart_df["Area"], chart_df["Total"],
                       color=TEAL, height=0.58)
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
        ax.set_xlabel("Complaints", fontsize=8, color=MUTED, labelpad=6)
        ax.tick_params(axis="y", labelsize=8, colors=MUTED, length=0)
        ax.tick_params(axis="x", labelsize=8, colors=MUTED, length=0)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.bar_label(bars, padding=4, fontsize=8, color=NAVY)
        ax.set_xlim(0, max(chart_df["Total"].max() * 1.18, 1))
    else:
        empty_chart(ax, "No complaint data yet")
    
    save_chart(fig, "location_chart.png")

    # 4. Priority-wise complaints — vertical bars with priority colours.
    fig, ax = plt.subplots(figsize=(4.4, 3.0))

    if not df_priority.empty:
        order = {"Low": 0, "Medium": 1, "High": 2}

        chart_df = df_priority.copy()
        chart_df["_order"] = chart_df["Priority"].map(order).fillna(3)
        chart_df = chart_df.sort_values("_order", ascending=True)

        bar_colors = [
        PRIORITY_COLORS.get(str(value), BLUE_LIGHT)
        for value in chart_df["Priority"]
       ]

        bars = ax.bar(
        chart_df["Priority"],
        chart_df["Total"],
        color=bar_colors,
        width=0.55,
        edgecolor="white",
        linewidth=1
        )

        ax.yaxis.grid(True, color=GRID, linewidth=0.8)
        ax.set_ylabel("Complaints", fontsize=8, color=MUTED, labelpad=6)

        ax.tick_params(axis="x", labelsize=8, colors=MUTED, length=0)
        ax.tick_params(axis="y", labelsize=8, colors=MUTED, length=0)

        ax.set_axisbelow(True)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.bar_label(
        bars,
        padding=3,
        fontsize=8,
        color=NAVY,
        fontweight="bold"
        )

        ax.set_ylim(0, max(chart_df["Total"].max() * 1.18, 1))

    else:
        empty_chart(ax, "No complaint data yet")

    save_chart(fig, "priority_chart.png")

    # 5. Complaint trend — line chart.
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    if not df_trend.empty:
        ax.plot(df_trend["Date"], df_trend["Total"], color=BLUE,
                marker="o", markersize=4, linewidth=2.2,
                markerfacecolor="#FFFFFF", markeredgewidth=1.8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=6))
        ax.tick_params(axis="x", rotation=25)
        style_axis(ax)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_ylabel("Complaints", fontsize=8, color=MUTED)
    else:
        empty_chart(ax, "No complaint data yet")
    
    save_chart(fig, "trend_chart.png")

    # 6. Resolution analytics — resolved complaints over time.
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    if not df_resolution.empty:
        ax.plot(df_resolution["Date"], df_resolution["Total"], color=TEAL,
                marker="o", markersize=4, linewidth=2.2,
                markerfacecolor="#FFFFFF", markeredgewidth=1.8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=6))
        ax.tick_params(axis="x", rotation=25)
        style_axis(ax)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_ylabel("Resolved complaints", fontsize=8, color=MUTED)
    else:
        empty_chart(ax, "No resolved complaints yet")
    
    save_chart(fig, "resolution_chart.png")

    # Generate plain-language insights from actual query results.
    top_category = str(category_data[0][0]) if category_data else "No category data yet"
    top_category_count = int(category_data[0][1]) if category_data else 0
    top_area = str(area_data[0][0]) if area_data else "No area data yet"
    top_area_count = int(area_data[0][1]) if area_data else 0
    resolution_rate = round((resolved / total) * 100, 1) if total else 0.0
    if previous_7 == 0:
        trend_message = (f"{recent_7} complaints were submitted in the last 7 days; there were none in the previous 7-day period." if recent_7 else "No complaints were submitted in the last 7 days.")
        trend_change = None
        trend_direction = "neutral" if recent_7 == 0 else "up"
    else:
        trend_change = round(((recent_7 - previous_7) / previous_7) * 100, 1)
        if trend_change > 0:
            trend_message = f"Complaints increased {trend_change}% compared with the previous 7-day period."
            trend_direction = "up"
        elif trend_change < 0:
            trend_message = f"Complaints decreased {abs(trend_change)}% compared with the previous 7-day period."
            trend_direction = "down"
        else:
            trend_message = "Complaint volume stayed the same as the previous 7-day period."
            trend_direction = "neutral"

    insights = [
        {"title": "Most Reported Category", "value": top_category, "detail": f"{top_category_count} complaints recorded", "icon": "▦"},
        {"title": "Most Affected Area", "value": top_area, "detail": f"{top_area_count} complaints recorded", "icon": "⌖"},
        {"title": "High-Priority Open", "value": str(high_priority_open), "detail": "Pending or in progress", "icon": "!"},
        {"title": "Resolution Rate", "value": f"{resolution_rate}%", "detail": f"{resolved} of {total} complaints resolved", "icon": "✓"},
    ]

    return render_template(
        "officer/dashboard.html",
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        recent_complaints=recent_complaints,
        insights=insights,
        trend_message=trend_message,
        trend_change=trend_change,
        trend_direction=trend_direction,
        recent_7=recent_7,
        previous_7=previous_7,
        avg_resolution_hours=avg_resolution_hours,
        category_chart="charts/category_chart.png",
        status_chart="charts/status_chart.png",
        location_chart="charts/location_chart.png",
        priority_chart="charts/priority_chart.png",
        trend_chart="charts/trend_chart.png",
        resolution_chart="charts/resolution_chart.png",
    )

@app.route("/officer/complaints")
def officer_complaints():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Officer":
        return redirect("/login")

    # Read filters
    filters = {
        "search": request.args.get("search", "").strip(),
        "complaint_id": request.args.get("complaint_id", "").strip(),
        "citizen_id": request.args.get("citizen_id", "").strip(),
        "category_id": request.args.get("category_id", "").strip(),
        "area": request.args.get("area", "").strip(),
        "status": request.args.get("status", "all"),
        "priority": request.args.get("priority", "all"),
        "date_range": request.args.get("date_range", "all"),
        "start_date": request.args.get("start_date", ""),
        "end_date": request.args.get("end_date", ""),
        "sort": request.args.get("sort", "newest")
    }

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Load categories for dropdown
        cursor.execute("""
            SELECT CategoryID, CategoryName
            FROM Categories
            ORDER BY CategoryName
        """)
        categories = cursor.fetchall()

        # Load citizens for dropdown
        cursor.execute("""
            SELECT UserID, FullName
            FROM Users
            WHERE Role = 'Citizen'
            ORDER BY FullName
        """)
        citizens = cursor.fetchall()

        # Build the complaint query
        query = """
            SELECT
                c.ComplaintID,
                u.FullName,
                cat.CategoryName,
                c.Description,
                c.Location,
                c.Priority,
                c.Status,
                c.CreatedAt
            FROM Complaints c
            JOIN Users u ON c.UserID = u.UserID
            JOIN Categories cat ON c.CategoryID = cat.CategoryID
            WHERE 1 = 1
        """

        params = []

        # Search by ID, citizen, category or location
        if filters["search"]:
            search = "%" + filters["search"] + "%"
            query += """
                AND (
                    CAST(c.ComplaintID AS VARCHAR(20)) LIKE ?
                    OR u.FullName LIKE ?
                    OR cat.CategoryName LIKE ?
                    OR c.Location LIKE ?
                )
            """
            params.extend([search, search, search, search])

        # Exact complaint ID
        if filters["complaint_id"]:
            try:
                complaint_id = int(filters["complaint_id"])
                if complaint_id > 0:
                    query += " AND c.ComplaintID = ?"
                    params.append(complaint_id)
            except ValueError:
                filters["complaint_id"] = ""

        # Citizen filter
        if filters["citizen_id"]:
            try:
                citizen_id = int(filters["citizen_id"])
                query += " AND c.UserID = ?"
                params.append(citizen_id)
            except ValueError:
                filters["citizen_id"] = ""

        # Category filter
        if filters["category_id"]:
            try:
                category_id = int(filters["category_id"])
                query += " AND c.CategoryID = ?"
                params.append(category_id)
            except ValueError:
                filters["category_id"] = ""

        # Area filter: match the area before " - "
        if filters["area"]:
            query += """
                AND LTRIM(RTRIM(
                    LEFT(c.Location, CHARINDEX(' - ', c.Location + ' - ') - 1)
                )) = ?
            """
            params.append(filters["area"])

        # Status filter
        if filters["status"] != "all":
            if filters["status"] in [
                "Pending", "In Progress", "Resolved"
            ]:
                query += " AND c.Status = ?"
                params.append(filters["status"])

        # Priority filter
        if filters["priority"] != "all":
            if filters["priority"] in ["Low", "Medium", "High"]:
                query += " AND c.Priority = ?"
                params.append(filters["priority"])

        # Date presets
        date_range = filters["date_range"]

        if date_range == "today":
            query += """
                AND c.CreatedAt >= CAST(GETDATE() AS DATE)
                AND c.CreatedAt < DATEADD(DAY, 1, CAST(GETDATE() AS DATE))
            """

        elif date_range == "last7":
            query += """
                AND c.CreatedAt >= DATEADD(
                    DAY, -6, CAST(GETDATE() AS DATE)
                )
                AND c.CreatedAt < DATEADD(
                    DAY, 1, CAST(GETDATE() AS DATE)
                )
            """

        elif date_range == "last30":
            query += """
                AND c.CreatedAt >= DATEADD(
                    DAY, -29, CAST(GETDATE() AS DATE)
                )
                AND c.CreatedAt < DATEADD(
                    DAY, 1, CAST(GETDATE() AS DATE)
                )
            """

        elif date_range == "this_month":
            query += """
                AND c.CreatedAt >= DATEFROMPARTS(
                    YEAR(GETDATE()), MONTH(GETDATE()), 1
                )
                AND c.CreatedAt < DATEADD(
                    MONTH, 1,
                    DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
                )
            """

        elif date_range == "custom":
            if filters["start_date"]:
                query += " AND c.CreatedAt >= ?"
                params.append(filters["start_date"])

            if filters["end_date"]:
                query += """
                    AND c.CreatedAt < DATEADD(
                        DAY, 1, CAST(? AS DATE)
                    )
                """
                params.append(filters["end_date"])

        # Sorting
        if filters["sort"] == "oldest":
            query += " ORDER BY c.CreatedAt ASC"
        else:
            query += " ORDER BY c.CreatedAt DESC"

        # Execute filtered query
        cursor.execute(query, params)
        complaints = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template(
        "officer/complaints.html",
        complaints=complaints,
        filters=filters,
        categories=categories,
        citizens=citizens,
        pune_areas=PUNE_AREAS
    )

@app.route("/officer/update-status/<int:complaint_id>", methods=["POST"])
def update_complaint_status(complaint_id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Officer":
        return redirect("/login")

    status = request.form.get("status", "").strip()

    # Allow only valid statuses
    allowed_statuses = ["Pending", "In Progress", "Resolved"]

    if status not in allowed_statuses:
        return redirect(url_for(
            "officer_complaint_details",
            complaint_id=complaint_id
        ))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if status == "Resolved":
            cursor.execute(
                """
                UPDATE Complaints
                SET Status = ?,
                    OfficerID = ?,
                    ResolvedAt = GETDATE()
                WHERE ComplaintID = ?
                """,
                (status, session["user_id"], complaint_id)
            )
        else:
            cursor.execute(
                """
                UPDATE Complaints
                SET Status = ?,
                    OfficerID = ?,
                    ResolvedAt = NULL
                WHERE ComplaintID = ?
                """,
                (status, session["user_id"], complaint_id)
            )

        conn.commit()

    finally:
        cursor.close()
        conn.close()

    # Return to the page from which the status was updated
    return_to = request.form.get("return_to", "complaints")

    if return_to == "details":
        return redirect(url_for(
            "officer_complaint_details",
            complaint_id=complaint_id
        ))

    return redirect(url_for("officer_complaints"))

@app.route("/officer/complaint/<int:complaint_id>")
def officer_complaint_details(complaint_id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Officer":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.ComplaintID,
            u.FullName,
            u.Email,
            cat.CategoryName,
            c.Description,
            c.Location,
            c.Priority,
            c.Status,
            c.ImagePath,
            c.CreatedAt,
            c.ResolvedAt
        FROM Complaints c
        JOIN Users u
            ON c.UserID = u.UserID
        JOIN Categories cat
            ON c.CategoryID = cat.CategoryID
        WHERE c.ComplaintID = ?
    """, (complaint_id,))

    complaint = cursor.fetchone()

    cursor.close()
    conn.close()

    if complaint is None:
        return redirect("/officer/complaints")

    return render_template(
        "officer/complaint_details.html",
        complaint=complaint
    )

@app.route("/officer/delete-complaint/<int:complaint_id>", methods=["POST"])
def delete_complaint(complaint_id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Officer":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete only the selected complaint
        cursor.execute(
            """
            DELETE FROM Complaints
            WHERE ComplaintID = ?
            """,
            (complaint_id,)
        )

        if cursor.rowcount == 0:
            conn.rollback()
        else:
            conn.commit()

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("officer_complaints"))

@app.route("/officer/profile")
def officer_profile():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "Officer":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT FullName, Email, Phone, City, Role
        FROM Users
        WHERE UserID = ?
    """, (session["user_id"],))

    officer = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "officer/profile.html",
        officer=officer
    )
    
# ================= CITIZEN DASHBOARD =================

@app.route("/citizen/dashboard")
def citizen_dashboard():

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Check role
    if session.get("role") != "Citizen":
        return redirect("/login")

    user_id = session["user_id"]

    connection = get_db_connection()
    cursor = connection.cursor()

    # Total complaints
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM Complaints
        WHERE UserID = ?
        """,
        (user_id,)
    )

    total_complaints = cursor.fetchone()[0]

    # Pending
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM Complaints
        WHERE UserID = ?
        AND Status = 'Pending'
        """,
        (user_id,)
    )

    pending_complaints = cursor.fetchone()[0]

    # In Progress
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM Complaints
        WHERE UserID = ?
        AND Status = 'In Progress'
        """,
        (user_id,)
    )

    in_progress_complaints = cursor.fetchone()[0]

    # Resolved
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM Complaints
        WHERE UserID = ?
        AND Status = 'Resolved'
        """,
        (user_id,)
    )

    resolved_complaints = cursor.fetchone()[0]

    # Recent complaints
    cursor.execute(
        """
        SELECT TOP 5
            c.ComplaintID,
            cat.CategoryName,
            c.Location,
            c.Priority,
            c.Status,
            c.CreatedAt
        FROM Complaints c
        INNER JOIN Categories cat
            ON c.CategoryID = cat.CategoryID
        WHERE c.UserID = ?
        ORDER BY c.CreatedAt DESC
        """,
        (user_id,)
    )

    recent_complaints = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "citizen/dashboard.html",
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints,
        recent_complaints=recent_complaints
    )


@app.route("/citizen/report", methods=["GET", "POST"])
def report_issue():

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can access this page
    if session.get("role") != "Citizen":
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        category_id = request.form.get("category")
        description = request.form.get("description", "").strip()
        area = request.form.get("area", "").strip()
        specific_location = request.form.get("specific_location", "").strip()
        priority = request.form.get("priority")

        # Combine area and specific location
        location = f"{area} - {specific_location}"

        # -------------------------
        # VALIDATION
        # -------------------------

        if not category_id:
            flash("Please select a category.", "error")
            conn.close()
            return redirect("/citizen/report")

        if not description:
            flash("Please enter a description.", "error")
            conn.close()
            return redirect("/citizen/report")

        if not area:
            flash("Please select a Pune area.", "error")
            conn.close()
            return redirect("/citizen/report")

        if area not in PUNE_AREAS:
            flash("Please select a valid Pune area.", "error")
            conn.close()
            return redirect("/citizen/report")

        if not specific_location:
            flash("Please enter a specific location or landmark.", "error")
            conn.close()
            return redirect("/citizen/report")

        if priority not in ["Low", "Medium", "High"]:
            flash("Please select a valid priority.", "error")
            conn.close()
            return redirect("/citizen/report")

        # -------------------------
        # IMAGE
        # -------------------------

        image = request.files.get("image")
        image_path = None

        if image and image.filename:

            allowed_extensions = ["jpg", "jpeg", "png"]

            filename = image.filename
            extension = filename.rsplit(".", 1)[-1].lower()

            if extension not in allowed_extensions:
                flash("Only JPG, JPEG and PNG images are allowed.", "error")
                conn.close()
                return redirect("/citizen/report")

            upload_folder = "static/uploads"
            os.makedirs(upload_folder, exist_ok=True)

            new_filename = str(uuid.uuid4()) + "." + extension

            image.save(
                os.path.join(upload_folder, new_filename)
            )

            image_path = "uploads/" + new_filename

        # -------------------------
        # INSERT COMPLAINT
        # -------------------------

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Complaints
            (
                UserID,
                CategoryID,
                Description,
                Location,
                Priority,
                ImagePath
            )
            OUTPUT INSERTED.ComplaintID
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                category_id,
                description,
                location,
                priority,
                image_path
            )
        )

        complaint_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        flash(
            f"Complaint submitted successfully! Your Complaint ID is {complaint_id}.",
            "success"
        )

        return redirect("/citizen/report")

    # -------------------------
    # GET CATEGORIES
    # -------------------------

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT CategoryID, CategoryName
        FROM Categories
        ORDER BY CategoryName
        """
    )

    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "citizen/report.html",
        categories=categories
    )


@app.route("/citizen/complaints")
def my_complaints():

    # Check if user is logged in
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can access this page
    if session.get("role") != "Citizen":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.ComplaintID,
            cat.CategoryName,
            c.Description,
            c.Location,
            c.Priority,
            c.Status,
            c.ImagePath,
            c.CreatedAt,
            c.ResolvedAt
        FROM Complaints c
        INNER JOIN Categories cat
            ON c.CategoryID = cat.CategoryID
        WHERE c.UserID = ?
        ORDER BY c.CreatedAt DESC
    """, (session["user_id"],))

    complaints = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "citizen/complaints.html",
        complaints=complaints
    )

# ==========================================
# EDIT CITIZEN COMPLAINT
# ==========================================

@app.route("/citizen/delete/<int:complaint_id>", methods=["POST"])
def delete_citizen_complaint(complaint_id):

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can delete complaints
    if session.get("role") != "Citizen":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete only the citizen's own pending complaint
        cursor.execute("""
            DELETE FROM Complaints
            WHERE ComplaintID = ?
              AND UserID = ?
              AND Status = 'Pending'
        """, (complaint_id, session["user_id"]))

        if cursor.rowcount == 0:
            conn.rollback()
            flash(
                "Complaint cannot be deleted. Only your pending complaints can be deleted.",
                "error"
            )
        else:
            conn.commit()
            flash(
                f"Complaint #{complaint_id} deleted successfully.",
                "success"
            )

    except Exception:
        conn.rollback()
        flash("Unable to delete the complaint. Please try again.", "error")

    finally:
        cursor.close()
        conn.close()

    return redirect("/citizen/complaints")

@app.route("/citizen/reopen/<int:complaint_id>", methods=["POST"])
def reopen_citizen_complaint(complaint_id):

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can reopen complaints
    if session.get("role") != "Citizen":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Reopen only the citizen's own resolved complaint
        cursor.execute("""
            UPDATE Complaints
            SET Status = 'Pending',
                ResolvedAt = NULL
            WHERE ComplaintID = ?
              AND UserID = ?
              AND Status = 'Resolved'
        """, (complaint_id, session["user_id"]))

        if cursor.rowcount == 0:
            conn.rollback()
            flash(
                "Complaint cannot be reopened. Only your resolved complaints can be reopened.",
                "error"
            )
        else:
            conn.commit()
            flash(
                f"Complaint #{complaint_id} reopened successfully.",
                "success"
            )

    except Exception:
        conn.rollback()
        flash("Unable to reopen the complaint. Please try again.", "error")

    finally:
        cursor.close()
        conn.close()

    return redirect("/citizen/complaints")

@app.route("/citizen/edit/<int:complaint_id>", methods=["GET", "POST"])
def edit_complaint(complaint_id):

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can edit complaints
    if session.get("role") != "Citizen":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch only a complaint belonging to this citizen
        cursor.execute("""
            SELECT
                ComplaintID,
                CategoryID,
                Description,
                Location,
                Priority,
                Status,
                ImagePath
            FROM Complaints
            WHERE ComplaintID = ?
              AND UserID = ?
        """, (complaint_id, session["user_id"]))

        complaint = cursor.fetchone()

        if not complaint:
            flash("Complaint not found.", "error")
            return redirect("/citizen/complaints")

        # Editing is allowed only for Pending complaints
        if complaint.Status != "Pending":
            flash(
                "Only pending complaints can be edited.",
                "error"
            )
            return redirect("/citizen/complaints")

        # Load categories
        cursor.execute("""
            SELECT CategoryID, CategoryName
            FROM Categories
            ORDER BY CategoryName
        """)

        categories = cursor.fetchall()

        if request.method == "POST":

            category_id = request.form.get("category")
            description = request.form.get(
                "description", ""
            ).strip()

            area = request.form.get("area", "").strip()
            specific_location = request.form.get(
                "specific_location", ""
            ).strip()

            priority = request.form.get("priority", "").strip()

            # Validate category
            valid_category_ids = [
                str(category.CategoryID)
                for category in categories
            ]

            if category_id not in valid_category_ids:
                flash("Please select a valid category.", "error")
                return redirect(
                    url_for(
                        "edit_complaint",
                        complaint_id=complaint_id
                    )
                )

            if not description:
                flash("Please enter a description.", "error")
                return redirect(
                    url_for(
                        "edit_complaint",
                        complaint_id=complaint_id
                    )
                )

            if area not in PUNE_AREAS:
                flash("Please select a valid Pune area.", "error")
                return redirect(
                    url_for(
                        "edit_complaint",
                        complaint_id=complaint_id
                    )
                )

            if not specific_location:
                flash(
                    "Please enter a specific location or landmark.",
                    "error"
                )
                return redirect(
                    url_for(
                        "edit_complaint",
                        complaint_id=complaint_id
                    )
                )

            if priority not in ["Low", "Medium", "High"]:
                flash("Please select a valid priority.", "error")
                return redirect(
                    url_for(
                        "edit_complaint",
                        complaint_id=complaint_id
                    )
                )

            # Combine area and specific location
            location = f"{area} - {specific_location}"

            # Keep the existing image unless a new valid image is uploaded
            image_path = complaint.ImagePath
            image = request.files.get("image")

            if image and image.filename:

                filename = image.filename

                if "." not in filename:
                    flash("Please upload a JPG, JPEG, or PNG image.", "error")
                    return redirect(
                        url_for(
                            "edit_complaint",
                            complaint_id=complaint_id
                        )
                    )

                extension = filename.rsplit(".", 1)[-1].lower()

                if extension not in ["jpg", "jpeg", "png"]:
                    flash(
                        "Only JPG, JPEG, and PNG images are allowed.",
                        "error"
                    )
                    return redirect(
                        url_for(
                            "edit_complaint",
                            complaint_id=complaint_id
                        )
                    )

                upload_folder = os.path.join("static", "uploads")
                os.makedirs(upload_folder, exist_ok=True)

                new_filename = str(uuid.uuid4()) + "." + extension

                image.save(
                    os.path.join(upload_folder, new_filename)
                )

                image_path = "uploads/" + new_filename

            # Update only if the complaint still belongs to this citizen
            # and remains Pending
            cursor.execute("""
                UPDATE Complaints
                SET CategoryID = ?,
                    Description = ?,
                    Location = ?,
                    Priority = ?,
                    ImagePath = ?
                WHERE ComplaintID = ?
                  AND UserID = ?
                  AND Status = 'Pending'
            """, (
                int(category_id),
                description,
                location,
                priority,
                image_path,
                complaint_id,
                session["user_id"]
            ))

            if cursor.rowcount == 0:
                conn.rollback()
                flash(
                    "The complaint could not be updated. "
                    "It may no longer be pending.",
                    "error"
                )
                return redirect("/citizen/complaints")

            conn.commit()

            flash(
                f"Complaint #{complaint_id} updated successfully!",
                "success"
            )

            return redirect("/citizen/complaints")

        # Split the saved location into area and landmark
        saved_location = complaint.Location or ""

        if " - " in saved_location:
            saved_area, saved_specific_location = (
                saved_location.split(" - ", 1)
            )
        else:
            saved_area = ""
            saved_specific_location = saved_location

        return render_template(
            "citizen/edit_complaint.html",
            complaint=complaint,
            categories=categories,
            pune_areas=PUNE_AREAS,
            saved_area=saved_area,
            saved_specific_location=saved_specific_location
        )

    finally:
        cursor.close()
        conn.close()

@app.route("/citizen/track/<int:complaint_id>")
def track_complaint(complaint_id):

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can access
    if session.get("role") != "Citizen":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.ComplaintID,
            cat.CategoryName,
            c.Description,
            c.Location,
            c.Priority,
            c.Status,
            c.CreatedAt,
            c.ResolvedAt
        FROM Complaints c
        INNER JOIN Categories cat
            ON c.CategoryID = cat.CategoryID
        WHERE c.ComplaintID = ?
        AND c.UserID = ?
    """, (complaint_id, session["user_id"]))

    complaint = cursor.fetchone()

    cursor.close()
    conn.close()

    # Complaint not found
    if not complaint:
        flash("Complaint not found.", "error")
        return redirect("/citizen/complaints")

    return render_template(
        "citizen/track.html",
        complaint=complaint
    )

@app.route("/citizen/profile")
def citizen_profile():

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can access
    if session.get("role") != "Citizen":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            FullName,
            Email,
            Phone,
            City,
            Role,
            CreatedAt
        FROM Users
        WHERE UserID = ?
    """, (session["user_id"],))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "citizen/profile.html",
        user=user
    )

@app.route("/citizen/help")
def citizen_help():

    # Check login
    if "user_id" not in session:
        return redirect("/login")

    # Only citizens can access
    if session.get("role") != "Citizen":
        return redirect("/login")

    return render_template("citizen/help.html")


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)