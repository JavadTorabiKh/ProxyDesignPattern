username_pattern = r"^[a-zA-Z0-9_-]{4,16}$"
fullName_pattern = r"^[A-Za-z]+(?:\s+[A-Za-z]+)+$"
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$"

EmailValid = {"messageEmailValid": "Email is Valid"}
EmailNOTValid = {"messageEmailNOTValid": "This is a duplicate email"}

UserValid = {"messageUserValid": "Username is Valid"}
UserNOTValid = {"messageUserNOTValid": "This is a duplicate Username"}

success = {"messageSuccess": "Your registeration was Success"}

checkUsernameMessage = {"checkUsernameMessage": "Your Username is invalid"}
checkFullnameMessage = {"checkFullnameMessage": "Your Email is invalid"}

checkEmailMessage = {"checkEmailMessage": "Your Email is invalid"}
checkPasswordMessage = {"checkPasswordMessage": "Your Password is invalid"}

checkConfirmpassMessage = {
    "checkConfirmpassMessage": "Confirm password does not match"}
