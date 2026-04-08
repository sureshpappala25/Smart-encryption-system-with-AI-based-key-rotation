from flask import Flask,session,redirect
import config
from routes.auth_routes import auth_bp
from routes.encryption_routes import enc_bp
from routes.ai_routes import ai_bp

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(enc_bp)
app.register_blueprint(ai_bp)
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")
if __name__ == "__main__":
    app.run(debug=True)