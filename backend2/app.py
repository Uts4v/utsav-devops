
import os
import psycopg2
from flask import Flask, request, jsonify, session
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "development-only-change-this")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "signup_login"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD"),
        port=5432
    )

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, username, password_hash FROM users WHERE email = %s",
            (email,)
        )

        user = cur.fetchone()
        cur.close()

        if user is None or not check_password_hash(user[2], password):
            return jsonify({"error": "Invalid email or password"}), 401

        session.clear()
        session["user_id"] = user[0]

        return jsonify({
            "message": "Login successful",
            "user_id": user[0],
            "username": user[1]
        }), 200

    except Exception:
        app.logger.exception("Login failed")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if conn:
            conn.close()


@app.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Please log in first"}), 401

    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, username, email FROM users WHERE id = %s",
            (user_id,)
        )

        user = cur.fetchone()
        cur.close()

        if user is None:
            session.clear()
            return jsonify({"error": "User not found"}), 401

        return jsonify({
            "user_id": user[0],
            "username": user[1],
            "email": user[2]
        }), 200

    except Exception:
        app.logger.exception("Dashboard request failed")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if conn:
            conn.close()


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
