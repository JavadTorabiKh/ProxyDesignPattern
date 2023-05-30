from abc import ABCMeta, abstractmethod
import pymongo
import jwt
import re

username_pattern = r"^[a-zA-Z0-9_-]{4,16}$"
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$"


# Subject
class User(metaclass=ABCMeta):
    @abstractmethod
    def do_register(self):
        pass


# RealSubject
class Registration(User):
    def __init__(self, userName, email, password1, password2):
        self.userName = userName
        self.email = email
        self.password1 = password1
        self.password2 = password2
        self.mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

    def do_register(self):
        userdb = self.mongo["usersDB"]
        usercol = userdb["usersValid"]

        # create JWT
        payload = {"username": self.userName, "email": self.email}
        secret_key = self.password1
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        userdict = {
            "userName": self.userName,
            "email": self.email,
            "password": self.password1,
            "token": token,
        }

        if usercol.find_one({"email": self.email}):
            return False
        x = usercol.insert_one(userdict)
        return True


# Proxy
class Validation(User):
    def __init__(self, registration):
        self.registration = registration

    @property
    def check_name(self):
        if self.registration.userName != "admin" and re.match(
            username_pattern, self.registration.userName
        ):
            return True
        return False

    @property
    def check_email(self):
        if re.match(email_pattern, self.registration.email):
            return True
        return False

    @property
    def check_password(self):
        if re.match(password_pattern, self.registration.password1):
            return True
        return False

    def do_register(self):
        if (
            self.check_name
            and self.check_email
            and self.check_password
            and self.registration.password1 == self.registration.password2
        ):
            return self.registration.do_register()
        return False
