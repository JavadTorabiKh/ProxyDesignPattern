from flask import Flask, request, jsonify
from utils.register import Validation, Registration

# create flask app
app = Flask(__name__)


# registeration endpoint
@app.route("/api/v1/register", methods=["POST"])
def register():
    # Extract JSON data from request
    data = request.get_json()

    # Create Registration object (RealSubject) with user data
    registration = Registration(
        data["userName"],
        data["fullName"],
        data["email"],
        data["password1"],
        data["password2"],
    )

    # Create Validation object (Proxy) that wraps the Registration object
    validation = Validation(registration)

    # Attempt registration through proxy (which performs validation first)
    if validation.do_register():
        # If registration successful, return appropriate messages
        if registration.success_message:
            return jsonify(
                [
                    registration.email_message,
                    registration.username_message,
                    registration.success_message,
                ]
            )
        # Return email and username validation messages
        return jsonify(
            [
                registration.email_message,
                registration.username_message,
            ]
        )
    else:
        # If validation failed, compile all error messages
        listErr = [
            validation.username_synErr,
            validation.fullname_synErr,
            validation.email_synErr,
            validation.pass_synErr,
            validation.confirmPass_synErr,
        ]
        # Filter out None values and return error messages
        return jsonify(list(filter(None, listErr)))


if __name__ == "__main__":
    # Run Flask application in debug mode
    app.run(debug=True)
