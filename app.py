from flask import Flask, request, jsonify
from utils.user import Validation, Registration

app = Flask(__name__)


@app.route("/api/v1/register", methods=["POST"])
def register():
    data = request.get_json()

    registration = Registration(
        data["userName"], data["email"], data["password1"], data["password2"]
    )
    validation = Validation(registration)

    if validation.do_register():
        return jsonify({"message": "Your validation was successful"})
    return jsonify({"message": "Your validation was unsuccessful"})


if __name__ == "__main__":
    app.run(debug=True)
