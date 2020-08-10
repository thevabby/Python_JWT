from flask import Flask, request, jsonify, make_response
import jwt
import datetime

app = Flask(__name__)

app.config["secret_key"] = "thisissecretkey"


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
