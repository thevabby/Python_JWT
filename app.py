from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config["secret_key"] = "thisissecretkey"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get(
            "token"
        )  # http://localhost:5000/route?token=edugdifuhrt.w45fgdrt3.45.fdd.rte4e.ggrf.dfg

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, app.config["secret_key"])
        except:
            return jsonify({"message": "Token is invalid"}), 403

        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return "Home Page"


@app.route("/login")
def login():
    auth = request.authorization

    if auth and auth.password == "password":
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["secret_key"],
        )
        return jsonify({"tokens": token.decode("UTF-8")})
    return make_response(
        "could not verify", 401, {"WWW-Authenticate": 'Basic Realm="Login Required"'}
    )


if __name__ == "__main__":
    app.run(debug=True)
