from flask import Flask, request, jsonify
from utils.register import Validation, Registration

app = Flask(__name__)


@app.route("/api/v1/register", methods=["POST"])
def register():
    data = request.get_json()

    registration = Registration(
        data["userName"],
        data["fullName"],
        data["email"],
        data["password1"],
        data["password2"],
    )
    validation = Validation(registration)

    if validation.do_register():
        if registration.success_message:
            return jsonify(
                [
                    registration.email_message,
                    registration.username_message,
                    registration.success_message,
                ]
            )
        return jsonify(
            [
                registration.email_message,
                registration.username_message,
            ]
        )
    else:
        listErr =[
            validation.username_synErr,
            validation.fullname_synErr,
            validation.email_synErr,
            validation.pass_synErr,
            validation.confirmPass_synErr,
        ]
        return jsonify(list(filter(None, listErr)))


if __name__ == "__main__":
    app.run(debug=True)
