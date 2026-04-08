from flask import Blueprint,render_template,request,redirect,url_for,session
import sqlite3
import config
from database import init_db

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/")
def index():
    return render_template("index.html")

@auth_bp.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":

        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn = sqlite3.connect(config.DATABASE)
        cur = conn.cursor()

        init_db()

        # insert data
        cur.execute("""
        INSERT INTO users(username,password,email,phone)
        VALUES(?,?,?,?)
        """,(username,password,email,phone))

        conn.commit()
        conn.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")



@auth_bp.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(config.DATABASE)
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """,(username,password))

        user = cur.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")
@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
        
    # --- REAL-TIME AI SECURITY ANALYTICS ---
    conn = sqlite3.connect(config.DATABASE)
    cursor = conn.cursor()

    # 1. Total Operations (Combined)
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM history WHERE user_id = ?) + 
            (SELECT COUNT(*) FROM uploaded_files WHERE user_id = ?)
    """, (session["user_id"], session["user_id"]))
    total_ops = cursor.fetchone()[0]

    # 2. Algorithm Distribution (Combined)
    cursor.execute("""
        SELECT algorithm, COUNT(*) FROM (
            SELECT algorithm FROM history WHERE user_id = ?
            UNION ALL
            SELECT algorithm FROM uploaded_files WHERE user_id = ?
        ) GROUP BY algorithm
    """, (session["user_id"], session["user_id"]))
    algo_counts = dict(cursor.fetchall())
    algo_dist = {
        "AES": algo_counts.get("aes", 0),
        "RSA": algo_counts.get("rsa", 0),
        "ECC": algo_counts.get("ecc", 0)
    }

    # 3. Risk Trend (Combined - Last 10 operations)
    cursor.execute("""
        SELECT risk_score FROM (
            SELECT risk_score, created_at FROM history WHERE user_id = ?
            UNION ALL
            SELECT risk_score, created_at FROM uploaded_files WHERE user_id = ?
        ) ORDER BY created_at DESC LIMIT 10
    """, (session["user_id"], session["user_id"]))
    raw_risks = cursor.fetchall()
    
    recent_risks = []
    for r in raw_risks:
        try:
            recent_risks.append(float(r[0]) if r[0] is not None else 0.1)
        except (ValueError, TypeError):
            recent_risks.append(0.1)
    
    recent_risks = recent_risks[::-1] # Reverse to chronological
    if not recent_risks: recent_risks = [0.1]

    # 4. Unified Risk Level
    avg_risk = sum(recent_risks) / len(recent_risks)
    if avg_risk < 0.3:
        threat_text = "Low"
    elif avg_risk < 0.6:
        threat_text = "Medium"
    else:
        threat_text = "High"

    # 5. Real-time Security Events (Dynamic)
    cursor.execute("""
        SELECT 'text' as type, input_text, algorithm, risk_score, created_at 
        FROM history WHERE user_id = ?
        UNION ALL
        SELECT 'file' as type, original_filename, algorithm, risk_score, created_at 
        FROM uploaded_files WHERE user_id = ?
        ORDER BY created_at DESC LIMIT 5
    """, (session["user_id"], session["user_id"]))
    events_raw = cursor.fetchall()
    
    recent_events = []
    from datetime import datetime
    for e in events_raw:
        # Simple relative time logic for the UI
        try:
            dt = datetime.strptime(e[4], '%Y-%m-%d %H:%M:%S')
            diff = datetime.now() - dt
            if diff.seconds < 60:
                time_str = "Just now"
            elif diff.seconds < 3600:
                time_str = f"{diff.seconds // 60} mins ago"
            else:
                time_str = f"{diff.seconds // 3600} hours ago"
        except:
            time_str = "Recently"

        recent_events.append({
            "type": e[0],
            "label": e[1][:30] + "..." if len(e[1]) > 30 else e[1],
            "algorithm": e[2].upper(),
            "risk": "High" if e[3] > 0.6 else "Normal",
            "time": time_str
        })

    security_metrics = {
        "threat_level": threat_text,
        "risk_trend": recent_risks,
        "algorithm_dist": algo_dist,
        "total_encrypted": total_ops,
        "key_health": 100 - int(avg_risk * 100),
        "recent_events": recent_events
    }
    
    conn.close()
    
    return render_template("dashboard.html", metrics=security_metrics)