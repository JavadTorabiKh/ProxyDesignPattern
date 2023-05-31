username_pattern = r"^[a-zA-Z0-9_-]{4,16}$"
fullName_pattern = r"^[A-Za-z]+(?:\s+[A-Za-z]+)+$"
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$"

EmailValid = {"message": "Your Email is Valid"}
EmailNOTValid = {"message": "Your Email is NOT Valid"}
UserValid = {"message": "Your User name is Valid"}
UserNOTValid = {"message": "Your User name is NOT Valid"}
success = {"message": "Your registeration was Success"}

