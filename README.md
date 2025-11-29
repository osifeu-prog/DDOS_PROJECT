# DDOS: Digital Democratic Operating System - Global Recruitment Phase

## ✨ Vision: A Sovereign Digital Democracy
DDOS is designed to be the next generation of national governance, built on a secure, decentralized platform. Our goal is to enable **Liquid Democracy** and **Full Citizen Participation** through cryptographic proofs (ZKP). This site is our initial community hub for recruiting core developers, cryptographers, legal experts, and investors.

## 🤝 Strategic Partnerships & Existing Ecosystem
We are actively building our network and are pleased to announce existing operational bridges and partnerships:
* **Binance Smart Chain (BNB Chain):** We have existing technological connections and systems built on BNB Chain for preliminary testing and scalability solutions (Layer 2 bridge development).
* **TON (The Open Network):** We utilize TON's robust, decentralized infrastructure for secure, high-speed, and low-cost decentralized application layers, demonstrating our ability to integrate with high-throughput global blockchain networks.

## 🏗️ Core Architecture Highlights
1.  **Three-Layered Blockchain:** Layer 1 (Sovereignty), Layer 2 (Micro-Democracy), and Layer 3 (ZK-Rollup Aggregator) for unparalleled scale and security.
2.  **Zero-Knowledge Proofs (ZKP):** Ensuring **absolute voter anonymity** while guaranteeing one-vote-per-citizen legitimacy.
3.  **Automated Escalation Engine:** Smart Contracts automatically advance citizen proposals if bureaucracy fails to address them within defined timeframes.

## 🚀 Deployment Instructions (Server Setup)
To run the server, database, and admin panel:

### Prerequisites:
* Python 3.8+
* PostgreSQL 12+
* Nginx or similar web server (for production)
* Required Python libraries: `pip install -r deployment/requirements.txt`

### Step 1: Database Setup (PostgreSQL)
1.  Connect to your PostgreSQL server.
2.  Run the commands in `deployment/init_db.sql` to create the `registered_users`, `messages`, and `access_logs` tables.

### Step 2: Configure Environment
1.  **Crucial:** Create a `.env` file in the root directory to store sensitive data:
    ```
    # Database Configuration
    DB_HOST=localhost
    DB_NAME=ddos_project_db
    DB_USER=your_db_user
    DB_PASS=your_db_password
    
    # Twilio SMS Service (for Admin Alerts)
    TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=+15005550006  # Twilio number
    ADMIN_PHONE_NUMBER=0584203384    # Your actual phone number for alerts
    
    # Admin Credentials
    ADMIN_USERNAME=ddos_admin
    ADMIN_PASSWORD=strong_secure_password123 # CHANGE THIS IMMEDIATELY
    ```
2.  Install the required libraries: `pip install -r deployment/requirements.txt`

### Step 3: Run the Server
1.  Execute the backend: `python deployment/server.py`
    * *Note: For production, use Gunicorn or uWSGI behind Nginx.*

### Step 4: Access and Share
* **Frontend (Public Site):** Access at `http://localhost:5000/`
* **Admin Panel:** Access at `http://localhost:5000/admin` (Use credentials from `.env`)
* **To Share:** Once deployed to a public domain (e.g., `www.ddos.org`), share that **public URL**. The Open Graph tags will ensure the beautiful image is attached automatically.

## 📞 Contact Information
For urgent inquiries and direct communication with project leads: **0584203384** (This number is used for SMS alerts from the system).
