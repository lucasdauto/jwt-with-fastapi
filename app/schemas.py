from pydantic import Basemodel, validator
import re

class User(Basemodel):
    username: str
    email: str
    password: str

    @validator("username")
    def username_must_be_unique(cls, value):
        if not re.match("^[a-z][0-9]|@)+$", value):
            raise ValueError("username format invalid")
        
        return value