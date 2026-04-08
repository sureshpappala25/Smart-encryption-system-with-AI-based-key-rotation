from flask import Blueprint, render_template, request, session, redirect, url_for, send_file
from encryption.encryption_utils import encrypt_data, decrypt_data, encrypt_file, decrypt_file
from encryption.key_manager import load_key, load_rsa_keys, generate_key, generate_rsa_keys, generate_file_specific_key
from encryption.ai_engine import get_risk_assessment
import sqlite3
import os
import uuid
import io
from werkzeug.utils import secure_filename
from database import init_db

init_db()   # ADD THIS LINE

enc_bp = Blueprint("enc", __name__)

import config
DB_NAME = config.DATABASE


@enc_bp.route("/encrypt", methods=["GET", "POST"])
def encrypt():

    if request.method == "POST":

        user_id = session.get("user_id", 101) # Default to a mock user_id if not in session
        pattern = request.form.get("pattern", "normal") # Simulated traffic pattern from UI

        file = request.files.get("file")

        if file and file.filename != '':
            # --- FILE UPLOAD LOGIC ---
            filename = secure_filename(file.filename)
            file_bytes = file.read()
            
            # Risk assessment based on file name/metadata or mock behavior
            analysis_result = get_risk_assessment(user_id, pattern, filename)
            risk_score = analysis_result['unified_risk']

            if risk_score < 0.3:
                algorithm = "aes"
            elif risk_score < 0.6:
                # RSA cannot encrypt bulk data (block size limit). We use AES with a unique key instead for file uploads.
                algorithm = "aes"
            else:
                algorithm = "ecc"

            # Generate unique key for this file
            file_key = generate_file_specific_key()

            # Encrypt the file content
            encrypted_data = encrypt_file(file_bytes, file_key, algorithm)

            # Save the encrypted file
            uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            encrypted_filename = f"enc_{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(uploads_dir, encrypted_filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(encrypted_data)

            # Save metadata to database
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO uploaded_files (user_id, original_filename, encrypted_filename, algorithm, file_key, risk_score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, filename, encrypted_filename, algorithm, file_key, risk_score))
            conn.commit()
            conn.close()

            return render_template("result.html", 
                                   result=file_key, 
                                   popup_message=f"File '{filename}' successfully encrypted and saved safely.\\n\\nKeep this High Security Key safe for decryption.",
                                   rotation_reason="File encryption complete. High Security Key generated.", 
                                   analysis=analysis_result)

        else:
            # --- TEXT ENCRYPTION LOGIC ---
            text = request.form.get("text", "")
            if not text:
                return render_template("encrypt.html", error="Please provide text or a file to encrypt.")

            # 🧠 ADVANCED AI RISK ASSESSMENT (Architecture's Engine)
            analysis_result = get_risk_assessment(user_id, pattern, text)
            risk_score = analysis_result['unified_risk']
            
            # DYNAMIC ALGORITHM SELECTION (Architecture's Dynamic Encryption)
            if risk_score < 0.3:
                algorithm = "aes"
            elif risk_score < 0.6:
                algorithm = "chacha"
            else:
                algorithm = "rsa"

            # AUTO KEY ROTATION ENGINE
            rotation_reason = ""
            if algorithm == "rsa":
                # High Sensitivity: Trigger auto key rotation for RSA
                public_key, _ = generate_rsa_keys()
                key = public_key
                rotation_reason = "♻️ AI Auto-Response: High sensitivity detected! System auto-rotated to new RSA keys."
            elif algorithm == "chacha":
                # Medium Sensitivity: Trigger auto key rotation for ChaCha20
                key = generate_key()
                rotation_reason = "♻️ AI Auto-Response: Moderate sensitivity. System auto-rotated to a new ChaCha20 key."
            else:
                # Low Sensitivity: Use optimal existing AES key
                key = load_key()

            encrypted = encrypt_data(text, key, algorithm)

            # ✅ STORE IN DATABASE WITH AI METRICS
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO history (user_id, input_text, algorithm, encrypted_text, risk_score, threat_pattern)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, text, algorithm, encrypted, risk_score, pattern))

            conn.commit()

        return render_template("result.html", 
                               result=encrypted, 
                               rotation_reason=rotation_reason, 
                               analysis=analysis_result)

    return render_template("encrypt.html")


@enc_bp.route("/decrypt", methods=["GET","POST"])
def decrypt():

    if request.method == "POST":

        text = request.form.get("text", "").strip()
        algorithm = request.form.get("algorithm", "ai_auto")
        file_key = request.form.get("file_key", "").strip()
        user_id = session.get("user_id", 101)
        pattern = request.form.get("pattern", "normal") # Optional context

        # 🧠 DYNAMIC AI DECRYPTION: Auto-select algorithm based on risk analysis
        if algorithm == "ai_auto":
            analysis_result = get_risk_assessment(user_id, pattern, text)
            risk_score = analysis_result['unified_risk']
            
            if risk_score < 0.3:
                algorithm = "aes"
            elif risk_score < 0.6:
                algorithm = "chacha" if not file_key else "aes"
            else:
                algorithm = "rsa"

        # LOAD APPROPRIATE KEYS
        if file_key:
            key = file_key
        elif algorithm == "rsa":
            _, private_key = load_rsa_keys()
            key = private_key
        else:
            key = load_key()

        try:
            decrypted = decrypt_data(text, key, algorithm)

            return render_template("result.html", result=decrypted)

        except Exception as e:
            error = f"❌ Invalid decryption! {str(e)}"

            return render_template("decrypt.html", error=error)

    return render_template("decrypt.html")


@enc_bp.route("/decrypt_file", methods=["POST"])
def decrypt_file_route():
    """Validates the High Security Key and confirms the original filename — download from Audit Logs."""
    file_key = request.form.get("file_key", "").strip()

    if not file_key:
        return render_template("decrypt.html", error="❌ Please provide your High Security Key.")

    # Lookup file record in DB by key
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT original_filename, encrypted_filename, algorithm
        FROM uploaded_files
        WHERE file_key = ?
        LIMIT 1
    """, (file_key,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return render_template("decrypt.html", error="❌ No file found for this key. Please check your High Security Key and try again.")

    original_filename, encrypted_filename, algorithm = row

    # Verify the encrypted file still exists on disk
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    encrypted_path = os.path.join(uploads_dir, encrypted_filename)

    if not os.path.exists(encrypted_path):
        return render_template("decrypt.html", error="❌ The encrypted file could not be found on the server. It may have been deleted.")

    # Show the decrypted filename on the result page
    return render_template("result.html",
                           result=original_filename,
                           rotation_reason=f"✅ Decryption successful! Your file '{original_filename}' is verified. Visit Audit Logs to download it.",
                           analysis=None)


@enc_bp.route("/download_file/<path:file_key>", methods=["GET"])
def download_file(file_key):
    """Serves the decrypted file as a download — accessible from Audit Logs."""
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT original_filename, encrypted_filename, algorithm, file_key
        FROM uploaded_files
        WHERE file_key = ? AND user_id = ?
        LIMIT 1
    """, (file_key, user_id))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return redirect(url_for("enc.history"))

    original_filename, encrypted_filename, algorithm, fkey = row

    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    encrypted_path = os.path.join(uploads_dir, encrypted_filename)

    if not os.path.exists(encrypted_path):
        return redirect(url_for("enc.history"))

    with open(encrypted_path, "r", encoding="utf-8") as f:
        encrypted_data_str = f.read()

    try:
        original_bytes = decrypt_file(encrypted_data_str, fkey, algorithm)
    except Exception:
        return redirect(url_for("enc.history"))

    file_stream = io.BytesIO(original_bytes)
    file_stream.seek(0)
    return send_file(file_stream, download_name=original_filename, as_attachment=True)

# ✅ NEW ROUTE (HISTORY)
@enc_bp.route("/history")
def history():

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history WHERE user_id=? ORDER BY id DESC", (user_id,))
    rows = cursor.fetchall()

    # Sanitize data: ensure risk_score is float
    data = []
    for row in rows:
        row_list = list(row)
        try:
            row_list[5] = float(row_list[5]) if row_list[5] is not None else 0.1
        except (ValueError, TypeError):
            row_list[5] = 0.1
        data.append(row_list)

    # Also fetch uploaded files for this user
    cursor.execute("SELECT id, original_filename, algorithm, risk_score, file_key, created_at FROM uploaded_files WHERE user_id=? ORDER BY id DESC", (user_id,))
    file_rows = cursor.fetchall()
    conn.close()

    return render_template("history.html", data=data, file_data=file_rows)

@enc_bp.route("/delete_history/<int:log_id>")
def delete_history(log_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ensure the user owns the record before deleting
    cursor.execute("DELETE FROM history WHERE id=? AND user_id=?", (log_id, user_id))
    
    conn.commit()
    conn.close()

    return redirect(url_for("enc.history"))


@enc_bp.route("/delete_file/<int:file_id>")
def delete_file(file_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch the encrypted filename first (to delete from disk), ensuring user owns the record
    cursor.execute(
        "SELECT encrypted_filename FROM uploaded_files WHERE id=? AND user_id=?",
        (file_id, user_id)
    )
    row = cursor.fetchone()

    if row:
        encrypted_filename = row[0]

        # Delete the physical encrypted file from the uploads directory
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        encrypted_path = os.path.join(uploads_dir, encrypted_filename)
        if os.path.exists(encrypted_path):
            os.remove(encrypted_path)

        # Remove the DB record
        cursor.execute("DELETE FROM uploaded_files WHERE id=? AND user_id=?", (file_id, user_id))
        conn.commit()

    conn.close()
    return redirect(url_for("enc.history"))