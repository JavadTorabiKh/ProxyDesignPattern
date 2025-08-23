from abc import ABCMeta, abstractmethod
import pymongo
import jwt
import re
from . import Constants


# Subject Interface - Defines the common interface for RealSubject and Proxy
class User(metaclass=ABCMeta):
    @abstractmethod
    def do_register(self):
        # Abstract method that must be implemented by all subclasses
        pass


# RealSubject - The actual object that performs user registration
class Registration(User):
    def __init__(self, userName, fullName, email, password1, password2):
        # Initialize with user registration data
        self.userName = userName
        self.fullName = fullName
        self.email = email
        self.password1 = password1
        self.password2 = password2

        # Establish MongoDB connection
        self.mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

        # Messages for response
        self.email_message = None
        self.username_message = None
        self.success_message = None

    def jwtFunc(self):
        # Create JWT token for authenticated user sessions
        payload = {"username": self.userName, "email": self.email}
        secret_key = (
            self.password1
        )  # Using password as secret key (note: security consideration)
        self.token = jwt.encode(payload, secret_key, algorithm="HS256")

    @property
    def checkData(self):
        # Check if email or username already exists in database

        # Query database for existing email
        Email = self.usercol.find_one({"email": self.email})

        # Query database for existing username
        userName = self.usercol.find_one({"userName": self.userName})

        # Set appropriate messages based on existence checks
        if Email:
            self.email_message = Constants.EmailNOTValid  # Email already exists
        else:
            self.email_message = Constants.EmailValid  # Email is available

        if userName:
            self.username_message = Constants.UserNOTValid  # Username already exists
        else:
            self.username_message = Constants.UserValid  # Username is available

    def do_register(self):
        # Main registration method - performs the actual user registration

        # Access users database and collection
        userdb = self.mongo["usersDB"]
        self.usercol = userdb["usersValid"]

        # Generate JWT token for the user
        self.jwtFunc()

        # Prepare user document for database insertion
        userdict = {
            "userName": self.userName,
            "fullName": self.fullName,
            "email": self.email,
            "password": self.password1,
            "token": self.token,
        }

        # Check if user data already exists
        self.checkData

        # If both email and username are available, register the user
        if (
            self.email_message == Constants.EmailValid
            and self.username_message == Constants.UserValid
        ):
            self.usercol.insert_one(userdict)  # Insert user into database
            self.success_message = Constants.success  # Set success message

        return (
            True  # Always returns True (consider returning False if registration fails)
        )


# Proxy - Controls access to the RealSubject and adds validation logic
class Validation(User):
    def __init__(self, registration):
        # Initialize with a Registration object (RealSubject)
        self.registration = registration

        # Validation error messages
        self.email_synErr = None
        self.fullname_synErr = None
        self.username_synErr = None
        self.pass_synErr = None
        self.confirmPass_synErr = None

    @property
    def check_username(self):
        # Validate username format using regex pattern
        if re.match(Constants.username_pattern, self.registration.userName):
            return True
        # Set error message if validation fails
        self.username_synErr = Constants.checkUsernameMessage
        return False

    @property
    def check_fullname(self):
        # Validate fullname format using regex pattern
        if re.match(Constants.fullName_pattern, self.registration.fullName):
            return True
        # Set error message if validation fails
        self.fullname_synErr = Constants.checkFullnameMessage
        return False

    @property
    def check_email(self):
        # Validate email format using regex pattern
        if re.match(Constants.email_pattern, self.registration.email):
            return True
        # Set error message if validation fails
        self.email_synErr = Constants.checkEmailMessage
        return False

    @property
    def check_password(self):
        # Validate password strength using regex pattern
        if re.match(Constants.password_pattern, self.registration.password1):
            return True
        # Set error message if validation fails
        self.pass_synErr = Constants.checkPasswordMessage
        return False

    @property
    def check_confirmpassword(self):
        # Check if password and confirmation password match
        if self.registration.password1 == self.registration.password2:
            return True
        # Set error message if passwords don't match
        self.confirmPass_synErr = Constants.checkConfirmpassMessage
        return False

    def do_register(self):
        # Proxy method that performs validation before delegating to RealSubject

        # Perform all validations
        checking = (
            self.check_username
            and self.check_email
            and self.check_password
            and self.check_confirmpassword
        )

        # If all validations pass, delegate to RealSubject's do_register method
        if checking:
            return self.registration.do_register()

        # Return False if any validation fails
        return False
