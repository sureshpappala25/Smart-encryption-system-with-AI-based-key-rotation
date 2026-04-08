# 🛡️ AI-Driven Secure Cloud Assets Management with Intelligen Key Rotation

An enterprise-grade, high-fidelity security platform that utilizes **Artificial Intelligence** to dynamically manage data encryption, analyze risk sensitivity, and automate cryptographic key lifecycles. 

---

## 🚀 Key Features

### 🧠 1. AI-Driven Smart Risk Management
*   **Predictive Sensitivity Analysis**: Real-time classification of data to identify high-risk strings (emails, credit cards, bank details) using advanced pattern matching and machine learning.
*   **Unified Risk Index**: A calculated security score (0.0 - 1.0) that determines the appropriate cryptographic strength required for each asset.
*   **Behavioral Pattern Simulation**: Detects 'Malware', 'Brute Force', or 'Unusual' activity to adjust security protocols on the fly.

### 🔐 2. Adaptive Cryptographic Engine
*   **Multi-Algorithm Support**: Seamlessly switch between **AES-256**, **RSA-4096**, **ECC-512**, **ChaCha20**, and **Fernet** based on AI risk assessments.
*   **Intelligent Metadata Tagging**: Every encrypted token includes a non-sensitive header (e.g., `AES256:`, `RSA4096:`) that allows the system to self-correct during decryption, ensuring 100% retrieval success even if the user forgets the settings.
*   **AI Auto-Select**: A "One-Click" encryption and decryption portal where the platform handles all cryptographic complexity automatically.

### 🔄 3. Smart Key Rotation Center
*   **Entropy-Driven Rotation**: Key rotation is recommended when the AI Risk Score exceeds critical thresholds (0.6).
*   **Unified Key Management**: Synchronized rotation of symmetric and asymmetric (RSA) keys to prevent data stale-out or breach persistence.
*   **Security Forensics**: Detailed audit logs tracking every rotation event, security scan, and user access pattern.

### 🎨 4. Premium Glassmorphic Dashboard
*   **AI Security Reporting**: Real-time data visualization of risk metrics using **Chart.js**.
*   **Global Theme Engine**: Persistent Light/Dark mode with high-contrast topography for optimal readability against vibrant backgrounds.
*   **Forensic Audit History**: ID-based record management allowing security operators to delete, refine, and update audit context.

---

## 🛠️ Technology Stack
*   **Backend**: Python / Flask
*   **AI Engine**: Scikit-Learn / Pandas (Behavior Analysis & Sensitivity)
*   **Database**: SQLite3 (Secure ACID storage)
*   **Cryptography**: `cryptography` library / `PyCryptodome`
*   **Frontend**: Vanilla JS / CSS3 (Dynamic UI with Glassmorphism)
*   **Charting**: Chart.js

---

## 📂 Project Structure
```bash
├── encryption/           # Core Cryptographic Utilities (AES, RSA, ECC, etc.)
├── routes/               # Modularized Auth and Encryption controllers
├── models/               # AI Engine and risk analysis training scripts
├── static/               # Premium CSS system and high-fidelity assets
├── templates/            # 10+ Responsive, theme-aware Jinja2 views
├── database.py           # Self-initializing secure DB schema
├── run.py                # Main application entry point
└── config.py             # System-wide security configurations
```

---

## 🚦 Quick Setup

1.  **Clone the Repository**:
    ```bash
    cd "BATCH-10 Smart encryption system with AI based key rotation"
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r req.txt
    ```

3.  **Initialize Security Database**:
    The system automatically initializes `encryption.db` and generates root keys on first run.

4.  **Launch the Security Center**:
    ```bash
    python run.py
    ```
    Visit `http://127.0.0.1:5000` to access the AI dashboard.

---

## ⚖️ License
This project is designed for enterprise-level cloud asset management and advanced cryptographic simulation. All rights reserved.

> [!IMPORTANT]
> This platform implements **Actual Cryptography**. Ensure all master keys (`current_key.key` and `.pem` files) are stored in a secure, hardware-isolated environment for production deployment.
