from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from gestures import predict_gesture

app = Flask(__name__)
CORS(app)

# Config
app.config["SECRET_KEY"] = "supersecretkey"

# In-memory storage
users = []
ADMIN_PASSWORD = "admin123"


# =========================
# Gesture Prediction
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    landmarks = data.get("landmarks")

    if not landmarks:
        return jsonify({"gesture": None, "confidence": 0})

    gesture, confidence = predict_gesture(landmarks)

    return jsonify({
        "gesture": gesture,
        "confidence": confidence
    })


# =========================
# Auth: Signup
# =========================
@app.route("/api/auth/signup", methods=["POST"])
def signup():
    data = request.json

    for u in users:
        if u["email"] == data["email"]:
            return jsonify({"message": "Email already exists"}), 400

    users.append({
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "created": str(datetime.datetime.utcnow())
    })

    return jsonify({"message": "User created"})


# =========================
# Auth: Login
# =========================
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json

    for u in users:
        if u["email"] == data["email"] and u["password"] == data["password"]:
            token = jwt.encode(
                {
                    "email": u["email"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
                },
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


# =========================
# Admin Login
# =========================
@app.route("/api/auth/admin-login", methods=["POST"])
def admin_login():
    if request.json.get("password") != ADMIN_PASSWORD:
        return jsonify({"message": "Access denied"}), 403

    token = jwt.encode(
        {
            "admin": True,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token": token})


# =========================
# Admin: View Users
# =========================
@app.route("/api/admin/users", methods=["GET"])
def admin_users():
    return jsonify(users)


# =========================
# App Runner
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

