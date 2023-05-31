from abc import ABCMeta, abstractmethod
import pymongo
import jwt
import re
from . import Constants


# Subject
class User(metaclass=ABCMeta):
    @abstractmethod
    def do_register(self):
        pass


# RealSubject
class Registration(User):
    def __init__(self, userName, fullName, email, password1, password2):
        self.userName = userName
        self.fullName = fullName
        self.email = email
        self.password1 = password1
        self.password2 = password2
        self.mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        self.email_message = None
        self.username_message = None
        self.success_message = None

    @property
    def jwtFunc(self):
        payload = {"username": self.userName, "email": self.email}
        secret_key = self.password1
        self.token = jwt.encode(payload, secret_key, algorithm="HS256")

    def checkData(self):
        Email = self.usercol.find_one({"email": self.email})
        userName = self.usercol.find_one({"userName": self.userName})

        if Email:
            self.email_message = Constants.EmailNOTValid

        else:
            self.email_message = Constants.EmailValid

        if userName:
            self.username_message = Constants.UserNOTValid

        else:
            self.username_message = Constants.UserValid

    def do_register(self):
        userdb = self.mongo["usersDB"]
        self.usercol = userdb["usersValid"]

        self.jwtFunc

        userdict = {
            "userName": self.userName,
            "fullName": self.fullName,
            "email": self.email,
            "password": self.password1,
            "token": self.token,
        }

        self.checkData()

        if (
            self.email_message == Constants.EmailValid
            and self.username_message == Constants.UserValid
        ):
            self.usercol.insert_one(userdict)
            self.success_message = Constants.success
        return True


# Proxy
class Validation(User):
    def __init__(self, registration):
        self.registration = registration

    @property
    def check_username(self):
        if re.match(Constants.username_pattern, self.registration.userName):
            return True
        return False

    @property
    def check_fullname(self):
        if re.match(Constants.fullName_pattern, self.registration.fullName):
            return True
        return False

    @property
    def check_email(self):
        if re.match(Constants.email_pattern, self.registration.email):
            return True
        return False

    @property
    def check_password(self):
        if re.match(Constants.password_pattern, self.registration.password1):
            return True
        return False

    def do_register(self):
        checking = (
            self.check_username
            and self.check_email
            and self.check_password
            and self.registration.password1 == self.registration.password2
        )
        if checking:
            return self.registration.do_register()
        return False
